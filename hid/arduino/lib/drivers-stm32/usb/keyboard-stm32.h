#pragma once

#include <USBComposite.h>

#include "tools.h"
#include "keyboard.h"
#include "usb-keymap.h"
#include "hid-wrapper-stm32.h"


namespace DRIVERS {
	const uint8_t reportDescriptionKeyboard[] = {
		HID_KEYBOARD_REPORT_DESCRIPTOR(),
	};

	class UsbKeyboard : public Keyboard {
		public:
			UsbKeyboard(HidWrapper& _hidWrapper) : Keyboard(USB_KEYBOARD),
				_hidWrapper(_hidWrapper), _keyboard(_hidWrapper.usbHid) {
				_hidWrapper.addReportDescriptor(reportDescriptionKeyboard, sizeof(reportDescriptionKeyboard));
			}

			void begin() override {
				_hidWrapper.begin();
				_keyboard.begin();
			}

			void clear() override {
				_keyboard.releaseAll();
			}

			void sendKey(uint8_t code, bool state) override {
				uint16_t usb_code = keymapUsb(code);
				if (usb_code == 0) {
					return;
				}

				// 0xE0 is a prefix from HID-Project keytable
				if (usb_code >= 0xE0 && usb_code <= 0xE7) {
					usb_code = usb_code - 0xE0 + 0x80;
				} else {
					usb_code += KEY_HID_OFFSET;
				}

				if (state) {
					_keyboard.press(usb_code);
				} else {
					_keyboard.release(usb_code);
				}
			}

			bool isOffline() override {
				return (USBComposite == false);
			}

			KeyboardLedsState getLeds() override {
				uint8_t leds = _keyboard.getLEDs();
				KeyboardLedsState result = {
					.caps = leds & 0b00000010,
					.scroll = leds & 0b00000100,
					.num = leds & 0b00000001,
				};
				return result;
			}

		private:
			HidWrapper& _hidWrapper;
			HIDKeyboard _keyboard;
	};
}
