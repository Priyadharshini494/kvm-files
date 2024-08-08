#pragma once

#include <stdint.h>

#include "driver.h"


namespace DRIVERS {
	typedef struct {
		bool caps;
		bool scroll;
		bool num;
	} KeyboardLedsState;

	struct Keyboard : public Driver {
		using Driver::Driver;
		
		virtual void begin() {}
	
		/**
		* Release all keys
		*/
		virtual void clear() {}
	
		/**
		* Sends key
		* @param code ???
		* @param state true pressed, false released
		*/
		virtual void sendKey(uint8_t code, bool state) {}
	
		virtual void periodic() {}
	
		/**
		* False if online or unknown. Otherwise true.
		*/
		virtual bool isOffline() {
			return false;
		}
	
		virtual KeyboardLedsState getLeds() {
			KeyboardLedsState result = {0};
			return result;
		}
	};
}
