#include <avr/eeprom.h>

#include "storage.h"


namespace DRIVERS {
	struct Eeprom : public Storage {
		using Storage::Storage;

		void readBlock(void *dest, const void *src, size_t size) override {
			eeprom_read_block(dest, src, size);
		}

		void updateBlock(const void *src, void *dest, size_t size) override {
			eeprom_update_block(src, dest, size);
		}
	};
}
