from collections import defaultdict
import pynput
import uinput
import time

pad = True
std = False

keymap = {
    ('left',      std): (uinput.ABS_X,        127,   0, "Zero X"     ),
    ('right',     std): (uinput.ABS_X,        128, 255, "Max X"      ),
    ('down',      std): (uinput.ABS_Y,        127,   0, "Max Y"      ),
    ('up',        std): (uinput.ABS_Y,        128, 255, "Zero Y"     ),
    ('delete',    std): (uinput.ABS_RX,       127,   0, "R Zero X"   ),
    ('page_down', std): (uinput.ABS_RX,       128, 255, "R Max X"    ),
    ('home',      std): (uinput.ABS_RY,       127,   0, "R Max Y"    ),
    ('end',       std): (uinput.ABS_RY,       128, 255, "R Zero Y"   ),
    ('/',         pad): (uinput.BTN_A,          0,   1, "A"          ),
    ('*',         pad): (uinput.BTN_B,          0,   1, "B"          ),
    ('-',         pad): (uinput.BTN_X,          0,   1, "X"          ),
    ('+',         pad): (uinput.BTN_Y,          0,   1, "Y"          ),
    ('ctrl_r',    std): (uinput.BTN_TL,         0,   1, "TL"         ),
    ('0',         pad): (uinput.BTN_TR,         0,   1, "TR"         ),
    ('insert',    std): (uinput.BTN_TL2,        0,   1, "TL2"        ),
    ('page_up',   std): (uinput.BTN_TR2,        0,   1, "TR2"        ),
    ('7',         pad): (uinput.BTN_THUMBL,     0,   1, "Thumb L"    ),
    ('9',         pad): (uinput.BTN_THUMBR,     0,   1, "Thumb R"    ),
    ('4',         pad): (uinput.BTN_DPAD_LEFT,  0,   1, "DPad Left"  ),
    ('6',         pad): (uinput.BTN_DPAD_RIGHT, 0,   1, "DPad Right" ),
    (None,        std): (uinput.BTN_DPAD_DOWN,  0,   1, "DPad Down"  ),
    ('8',         pad): (uinput.BTN_DPAD_UP,    0,   1, "DPad Up"    ),
}

events = [x[0] if x[1] == 0 else x[0] + (0, 255, 0, 0) for x in list(keymap.values())]
device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad",
)

# Center joystick
# syn=False to emit an "atomic" (128, 128) event.
device.emit(uinput.ABS_X,  128, syn=False)
device.emit(uinput.ABS_Y,  128)
device.emit(uinput.ABS_RX, 128, syn=False)
device.emit(uinput.ABS_RY, 128)

def get_key_tuple(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    return (k, hasattr(key, 'vk') and key.vk == None)


def on_press(key):
    kt = get_key_tuple(key)
    lookup_res = keymap.get(kt)
    if (lookup_res != None):
        uk, _, press_val, name = lookup_res
        device.emit(uk, press_val)
        print(str(kt) + " => " + name)

    return True


def on_release(key):
    kt = get_key_tuple(key)
    lookup_res = keymap.get(kt)
    if (lookup_res != None):
        uk, release_val, _, name = lookup_res
        device.emit(uk, release_val)

    return True


if True:
    listener = pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        )
    listener.start()  # start to listen on a separate thread
    print("virtual gamepad launch")
    listener.join()  # remove if main thread is polling self.keys
