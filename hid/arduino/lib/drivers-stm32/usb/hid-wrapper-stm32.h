#pragma once

#include <USBComposite.h>


namespace DRIVERS {
	class HidWrapper {
		public:
			void begin() {
				if (_init) {
					return;
				}
				_init = true;

				_report_descriptor_length = 0;
				for (unsigned index = 0; index < _count; ++index) {
					_report_descriptor_length += _descriptors_size[index];
				}

				_report_descriptor = new uint8[_report_descriptor_length];

				size_t offset = 0;
				for (unsigned index = 0; index < _count; ++index) {
					memcpy(_report_descriptor + offset, _report_descriptors[index], _descriptors_size[index]);
					offset += _descriptors_size[index];
				}

				usbHid.begin(_report_descriptor, _report_descriptor_length);
			}
			
			void addReportDescriptor(const uint8_t *report_descriptor, uint16_t report_descriptor_length) {
				_report_descriptors[_count] = report_descriptor;
				_descriptors_size[_count] = report_descriptor_length;
				++_count;
			}

			USBHID usbHid;
		
		private:
			bool _init = false;

			static constexpr uint8_t MAX_USB_DESCRIPTORS = 2;
			const uint8_t *_report_descriptors[MAX_USB_DESCRIPTORS];
			uint8_t _descriptors_size[MAX_USB_DESCRIPTORS];

			uint8_t _count = 0;
			uint8_t *_report_descriptor;
			uint16_t _report_descriptor_length;
	};
}
