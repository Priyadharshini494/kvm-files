#pragma once

#ifdef CMD_SERIAL
#include "connection.h"


namespace DRIVERS {
#ifdef Serial
#	undef Serial
#endif
	struct Serial : public Connection {
		Serial() : Connection(CONNECTION) {}

		void begin() override {
			CMD_SERIAL.begin(CMD_SERIAL_SPEED);
		}

		void periodic() override {
			if (CMD_SERIAL.available() > 0) {
				_buffer[_index] = (uint8_t)CMD_SERIAL.read();
				if (_index == 7) {
					_data_cb(_buffer, 8);
					_index = 0;
				} else {
					_last = micros();
					++_index;
				}
			} else if (_index > 0) {
				if (is_micros_timed_out(_last, CMD_SERIAL_TIMEOUT)) {
					_timeout_cb();
					_index = 0;
				}
			}
		}

		void write(const uint8_t *data, size_t size) override {
			CMD_SERIAL.write(data, size);
		}

		private:
			unsigned long _last = 0;
			uint8_t _index = 0;
			uint8_t _buffer[8];
	};
}
#endif
