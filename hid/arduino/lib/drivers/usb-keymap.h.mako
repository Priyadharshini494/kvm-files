#pragma once

<%! import operator %>
uint8_t keymapUsb(uint8_t code) {
	switch (code) {
% for km in sorted(keymap, key=operator.attrgetter("mcu_code")):
	% if km.usb_key.is_modifier:
		case ${km.mcu_code}: return ${km.usb_key.arduino_modifier_code}; // ${km.web_name}
	% else:
		case ${km.mcu_code}: return ${km.usb_key.code}; // ${km.web_name}
	% endif
% endfor
		default: return 0;
	}
}
