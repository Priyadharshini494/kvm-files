#pragma once

#include "driver.h"


namespace DRIVERS {
	enum status {
		RX_DATA = 0,
		KEYBOARD_ONLINE,
		MOUSE_ONLINE,
	};

	struct Board : public Driver {
		using Driver::Driver;
		virtual void reset() {}
		virtual void periodic() {}
		virtual void updateStatus(status status) {}
	};
}
