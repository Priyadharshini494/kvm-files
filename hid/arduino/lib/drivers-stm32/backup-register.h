# pragma once


#include <stm32f1_rtc.h>

#include "storage.h"


namespace DRIVERS {
	struct BackupRegister : public Storage {
		BackupRegister() : Storage(NON_VOLATILE_STORAGE) {
			_rtc.enableClockInterface();
		}

		void readBlock(void *dest, const void *src, size_t size) override {
			uint8_t *dest_ = reinterpret_cast<uint8_t*>(dest);
			for(size_t index = 0; index < size; ++index) {
				dest_[index] = _rtc.getBackupRegister(reinterpret_cast<uintptr_t>(src) + index + 1);
			}
		}

		void updateBlock(const void *src, void *dest, size_t size) override {
			const uint8_t *src_ = reinterpret_cast<const uint8_t*>(src);
			for(size_t index = 0; index < size; ++index) {
				_rtc.setBackupRegister(reinterpret_cast<uintptr_t>(dest) + index + 1, src_[index]);
			}
		}

		private:
			STM32F1_RTC _rtc;
	};
}
