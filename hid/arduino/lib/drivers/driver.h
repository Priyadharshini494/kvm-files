#pragma once

#include <stdint.h>


namespace DRIVERS {
	enum type {
		DUMMY = 0,
		USB_MOUSE_ABSOLUTE,
		USB_MOUSE_RELATIVE,
		USB_MOUSE_ABSOLUTE_WIN98,
		USB_KEYBOARD,
		PS2_KEYBOARD,
		NON_VOLATILE_STORAGE,
		BOARD,
		CONNECTION,
	};

	class Driver {
	public:
		Driver(type _type) : _type(_type) {}
		uint8_t getType() { return _type; }

	private:
		type _type;
	};
}
