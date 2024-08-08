#include "factory.h"
#include "usb/keyboard-stm32.h"
#include "usb/hid-wrapper-stm32.h"
#include "usb/mouse-absolute-stm32.h"
#include "usb/mouse-relative-stm32.h"
#include "backup-register.h"
#include "board-stm32.h"
#include "serial.h"

#ifndef __STM32F1__
#	error "Only STM32F1 is supported"
#endif
#ifdef SERIAL_USB
#	error "Disable random USB enumeration"
#endif


namespace DRIVERS {
	HidWrapper _hidWrapper;

	Keyboard *Factory::makeKeyboard(type _type) {
		switch (_type) {
#			ifdef HID_WITH_USB
			case USB_KEYBOARD:
				return new UsbKeyboard(_hidWrapper);
#			endif
			default:
				return new Keyboard(DUMMY);
		}
	}

	Mouse *Factory::makeMouse(type _type) {
		switch(_type) {
#			ifdef HID_WITH_USB
			case USB_MOUSE_ABSOLUTE:
				return new UsbMouseAbsolute(_hidWrapper);
			case USB_MOUSE_RELATIVE:
				return new UsbMouseRelative(_hidWrapper);
#			endif
			default:
				return new Mouse(DRIVERS::DUMMY);
		}
	}

	Storage *Factory::makeStorage(type _type) {
		switch (_type) {
#			ifdef HID_DYNAMIC
			case NON_VOLATILE_STORAGE:
				return new BackupRegister();
#			endif
			default:
				return new Storage(DRIVERS::DUMMY);
		}
	}

	Board *Factory::makeBoard(type _type) {
		switch (_type) {
			case BOARD:
				return new BoardStm32();
			default:
				return new Board(DRIVERS::DUMMY);
        }
	}
  
	Connection *Factory::makeConnection(type _type) {
#		ifdef CMD_SERIAL
		return new Serial();
#		else
#		error CMD phy is not defined
#		endif		
	}
}
