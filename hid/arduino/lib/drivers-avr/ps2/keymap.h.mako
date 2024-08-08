#pragma once


enum Ps2KeyType : uint8_t {
	PS2_KEY_TYPE_UNKNOWN = 0,
	PS2_KEY_TYPE_REG = 1,
	PS2_KEY_TYPE_SPEC = 2,
	PS2_KEY_TYPE_PRINT = 3,
	PS2_KEY_TYPE_PAUSE = 4,
};

<%! import operator %>
void keymapPs2(uint8_t code, Ps2KeyType *ps2_type, uint8_t *ps2_code) {
	*ps2_type = PS2_KEY_TYPE_UNKNOWN;
	*ps2_code = 0;

	switch (code) {
% for km in sorted(keymap, key=operator.attrgetter("mcu_code")):
		case ${km.mcu_code}: *ps2_type = PS2_KEY_TYPE_${km.ps2_key.type.upper()}; *ps2_code = ${km.ps2_key.code}; return; // ${km.web_name}
% endfor
	}
}
