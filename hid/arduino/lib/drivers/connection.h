#pragma once

#include "driver.h"
#include "stdint.h"


namespace DRIVERS {
	typedef void (*DataHandler)(const uint8_t *data, size_t size);
	typedef void (*TimeoutHandler)();

	struct Connection : public Driver {
		using Driver::Driver;

		virtual void begin() {}
		
		virtual void periodic() {}

		void onTimeout(TimeoutHandler cb) {
			_timeout_cb = cb;
		}

		void onData(DataHandler cb) {
			_data_cb = cb;
		}

		virtual void write(const uint8_t *data, size_t size) = 0;
		
		protected:
			TimeoutHandler _timeout_cb = nullptr;
			DataHandler _data_cb = nullptr;
	};
}
