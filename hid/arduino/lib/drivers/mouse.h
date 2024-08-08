#pragma once

#include <stdint.h>

#include "driver.h"


namespace DRIVERS {
	struct Mouse : public Driver {
		using Driver::Driver;
		virtual void begin() {}
		
		/**
		 * Release all keys
		 */
		virtual void clear() {}
		virtual void sendButtons(
			bool left_select, bool left_state,
			bool right_select, bool right_state,
			bool middle_select, bool middle_state,
			bool up_select, bool up_state,
			bool down_select, bool down_state) {}
		virtual void sendMove(int x, int y) {}
		virtual void sendRelative(int x, int y) {}
		virtual void sendWheel(int delta_y) {}
		virtual bool isOffline() { return false; }
		virtual void periodic() {}
	};
}
