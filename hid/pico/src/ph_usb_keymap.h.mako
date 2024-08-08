#pragma once

#include "ph_types.h"

<%! import operator %>
inline u8 ph_usb_keymap(u8 key) {
	switch (key) {
% for km in sorted(keymap, key=operator.attrgetter("mcu_code")):
	% if km.usb_key.is_modifier:
		case ${km.mcu_code}: return ${km.usb_key.arduino_modifier_code}; // ${km.web_name}
	% else:
		case ${km.mcu_code}: return ${km.usb_key.code}; // ${km.web_name}
	% endif
% endfor
	}
	return 0;
}
