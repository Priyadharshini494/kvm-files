#pragma once

#include <USBComposite.h>

#include "mouse.h"
#include "hid-wrapper-stm32.h"


namespace DRIVERS {
	const uint8_t reportDescriptionMouseRelative[] = {
		HID_MOUSE_REPORT_DESCRIPTOR()
	};

	class UsbMouseRelative : public Mouse {
		public:
			UsbMouseRelative(HidWrapper& _hidWrapper) : Mouse(USB_MOUSE_RELATIVE),
			_hidWrapper(_hidWrapper), _mouse(_hidWrapper.usbHid) {
				_hidWrapper.addReportDescriptor(reportDescriptionMouseRelative, sizeof(reportDescriptionMouseRelative));
			}

			void begin() override {
				_hidWrapper.begin();
			}

			void clear() override {
				_mouse.release(0xFF);
			}

			void sendButtons (
				bool left_select, bool left_state,
				bool right_select, bool right_state,
				bool middle_select, bool middle_state,
				bool up_select, bool up_state,
				bool down_select, bool down_state) override {

#				define SEND_BUTTON(x_low, x_up) { \
						if (x_low##_select) { \
							if (x_low##_state) _mouse.press(MOUSE_##x_up); \
							else _mouse.release(MOUSE_##x_up); \
						} \
					}
				SEND_BUTTON(left, LEFT);
				SEND_BUTTON(right, RIGHT);
				SEND_BUTTON(middle, MIDDLE);
#				undef SEND_BUTTON
			}

			void sendRelative(int x, int y) override {
				_mouse.move(x, y);
			}

			void sendWheel(int delta_y) override {
				_mouse.move(0, 0, delta_y);
			}

			bool isOffline() override {
				return (USBComposite == false);
			}

		private:
			HidWrapper& _hidWrapper;
			HIDMouse _mouse;
	};
}
