import pandas
import argparse

full_keymap_file_template = """
/*
 * Copyright (c) 2020 The ZMK Contributors
 *
 * SPDX-License-Identifier: MIT
 */

#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/rgb.h>
#include <dt-bindings/zmk/ext_power.h> 
#include <dt-bindings/zmk/outputs.h>

#define ZMK_MOUSE_DEFAULT_MOVE_VAL 8000//800
#define ZMK_MOUSE_DEFAULT_SCRL_VAL 100//10

#include <dt-bindings/zmk/mouse.h>

#define BASE 0
#define LOWER 1
#define RAISE 2
#define ADJUST 3


&sl {
    release-after-ms = <500>;
    /delete-property/ quick-release;
};


&soft_off {
    hold-time-ms = <1500>; // Only turn off it the key is held for these milliseconds or longer.
    /delete-property/ split-peripheral-off-on-press;
};

/ {

    behaviors {
        vol_encoder: behavior_vol_encoder {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&kp C_VOL_UP>, <&kp C_VOL_DN>;
        };

        rgb_encoder: behavior_rgb_encoder {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&rgb_ug RGB_BRI>, <&rgb_ug RGB_BRD>;
        };

        mouse_up_down: behavior_mouse_up_down {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&mmv MOVE_UP>, <&mmv MOVE_DOWN>;
            tap-ms = < 25 >;
        };

        mouse_left_right: behavior_mouse_left_right {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&mmv MOVE_RIGHT>, <&mmv MOVE_LEFT>;
            tap-ms = < 25 >;
        };

        mouse_scroll_up_down: behavior_mouse_scroll_up_down {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&msc SCRL_UP>, <&msc SCRL_DOWN>;
            tap-ms = < 250 >;
        };

        mouse_scroll_left_right: behavior_mouse_scroll_left_right {
            compatible = "zmk,behavior-sensor-rotate";
            #sensor-binding-cells = <0>;
            bindings = <&msc SCRL_RIGHT>, <&msc SCRL_LEFT>;
            tap-ms = < 250 >;
        };


        tdrshiftcaps: tap_dance_caps_r {
            compatible = "zmk,behavior-tap-dance";
            #binding-cells = <0>;
            tapping-term-ms = <200>;
            bindings = <&kp RSHIFT>, <&kp RSHIFT>, <&kp CAPSLOCK>;
        };


        tdlshiftcaps: tap_dance_caps_l {
            compatible = "zmk,behavior-tap-dance";
            #binding-cells = <0>;
            tapping-term-ms = <200>;
            bindings = <&kp LSHIFT>, <&kp LSHIFT>, <&kp CAPSLOCK>;
        };
    };

   // Activate ADJUST layer by pressing raise and lower
    conditional_layers {
        compatible = "zmk,conditional-layers";
        adjust_layer {
            if-layers = <LOWER RAISE>;
            then-layer = <ADJUST>;
        };
    };

    keymap {

        compatible = "zmk,keymap";

{[(keymaps)]}

    };
};

"""[1:-1].replace('{', '{{').replace('}', '}}').replace('{{[(', '{').replace(')]}}', '}')
# the replaces above change the {[( )]} set to { }, and { } to {{ }}
# so that it matches what .format wants

map_template = """
        {layernm}_layer {{
            display-name = "{layernm}";

            bindings = <
{keybindings}
            >;

            {sensor_bindings}
        }};
"""[1:-1]

sensor_bindings = { None: 'sensor-bindings = <&mouse_up_down &mouse_left_right>;',
                    'adjust': 'sensor-bindings = <&rgb_encoder &vol_encoder>;',
                    'raise': 'sensor-bindings = <&mouse_scroll_up_down &mouse_scroll_left_right>;'}

def make_map_str(infn, template=map_template):
    ss = []
    allsheets = pandas.read_excel(infn, sheet_name=None)

    # for some reason zmq cares that the default/lower/raise be in a particular order...
    allsheets_ordered = []
    for layernm in ['default', 'lower', 'raise']:
        if layernm in allsheets:
            allsheets_ordered.append((layernm, allsheets.pop(layernm)))
    for layernm, df in allsheets.items():
        allsheets_ordered.append((layernm, df))

    for layernm, df in allsheets_ordered:
        if layernm == 'TEMPLATE':
            continue
        key_bindings = []
        for irow, row in df.iterrows():
            for colnm, val in row.items():
                if not (pandas.isna(val) or val.strip() == ''):
                    vs = val.strip()
                    key_bindings.append(f'&{vs} ')
            key_bindings.append('\n')
        
        ss.append(template.format(layernm=layernm,
                                      sensor_bindings=sensor_bindings.get(layernm, sensor_bindings[None]),
                                      keybindings=''.join(key_bindings)
        ))
        ss.append('\n\n')
    return ''.join(ss)  

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infn')
    parser.add_argument('--full', '-f', action='store_true')
    args = parser.parse_args()

    mapstr = make_map_str(args.infn)
    
    if args.full:
        mapstr = full_keymap_file_template.format(keymaps=mapstr)
    
    print(mapstr)
