#pragma once

#include "driver.h"
#include "stdlib.h"


namespace DRIVERS {
	struct Storage : public Driver {
		using Driver::Driver;
		virtual void readBlock(void *dest, const void *src, size_t size) {}
		virtual void updateBlock(const void *src, void *dest, size_t size) {}
	};
}
