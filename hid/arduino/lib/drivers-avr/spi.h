#pragma once

#include <Arduino.h>

#include "connection.h"


namespace DRIVERS {
	struct Spi : public Connection {
		Spi() : Connection(CONNECTION) {}

		void begin() override;

		void periodic() override;

		void write(const uint8_t *data, size_t size) override;
	};
}
