#pragma once

#include <digitalWriteFast.h>


inline void aumInit() {
	pinModeFast(AUM_IS_USB_POWERED_PIN, INPUT);
	pinModeFast(AUM_SET_USB_VBUS_PIN, OUTPUT);
	pinModeFast(AUM_SET_USB_CONNECTED_PIN, OUTPUT);
	digitalWriteFast(AUM_SET_USB_CONNECTED_PIN, HIGH);
}

inline void aumProxyUsbVbus() {
	bool vbus = digitalReadFast(AUM_IS_USB_POWERED_PIN);
	if (digitalReadFast(AUM_SET_USB_VBUS_PIN) != vbus) {
		digitalWriteFast(AUM_SET_USB_VBUS_PIN, vbus);
	}
}

inline void aumSetUsbConnected(bool connected) {
	digitalWriteFast(AUM_SET_USB_CONNECTED_PIN, connected);
}

inline bool aumIsUsbConnected() {
	return digitalReadFast(AUM_SET_USB_CONNECTED_PIN);
}
