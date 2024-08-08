#include "pico/stdlib.h"
#include "hardware/gpio.h"

#include "ph_types.h"


#define _UART		uart0
#define _SPEED		3000000
#define _RX_PIN		-1 // 1 - No stdin
#define _TX_PIN		0
#define _ACT_PIN	25


void ph_debug_uart_init(void) {
	stdio_uart_init_full(_UART, _SPEED, _TX_PIN, _RX_PIN);
}

void ph_debug_act_init(void) {
	gpio_init(_ACT_PIN);
	gpio_set_dir(_ACT_PIN, GPIO_OUT);
}

void ph_debug_act(bool flag) {
	gpio_put(_ACT_PIN, flag);
}

void ph_debug_act_pulse(u64 delay_ms) {
	static bool flag = false;
	static u64 next_ts = 0;
	const u64 now_ts = time_us_64();
	if (now_ts >= next_ts) {
		ph_debug_act(flag);
		flag = !flag;
		next_ts = now_ts + (delay_ms * 1000);
	}
}
