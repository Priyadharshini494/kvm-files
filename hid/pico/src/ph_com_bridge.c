#include "ph_com_bridge.h"

#include "pico/stdlib.h"

#include "tusb.h"

#include "ph_types.h"


#define _TIMEOUT_US	100000


static u8 _buf[8] = {0};
static u8 _index = 0;
static u64 _last_ts = 0;

static void (*_data_cb)(const u8 *) = NULL;
static void (*_timeout_cb)(void) = NULL;


void ph_com_bridge_init(void (*data_cb)(const u8 *), void (*timeout_cb)(void)) {
	_data_cb = data_cb;
	_timeout_cb = timeout_cb;
}

void ph_com_bridge_task(void) {
	if (!tud_cdc_connected()) {
		tud_cdc_write_clear();
		return;
	}

	if (tud_cdc_available() > 0) {
		const s32 ch = tud_cdc_read_char();
		if (ch < 0) {
			goto no_data;
		}
		_buf[_index] = (u8)ch;
		if (_index == 7) {
			_data_cb(_buf);
			_index = 0;
		} else {
			_last_ts = time_us_64();
			++_index;
		}
		return;
	}

	no_data:
	if (_index > 0) {
		if (_last_ts + _TIMEOUT_US < time_us_64()) {
			_timeout_cb();
			_index = 0;
		}
	}
}

void ph_com_bridge_write(const u8 *data) {
	if (tud_cdc_connected()) {
		tud_cdc_write(data, 8);
		tud_cdc_write_flush();
	}
}
