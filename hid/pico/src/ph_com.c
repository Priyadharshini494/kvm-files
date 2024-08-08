#include "ph_com.h"

#include "pico/stdlib.h"
#include "hardware/gpio.h"

#include "ph_types.h"
#include "ph_outputs.h"
#include "ph_com_bridge.h"
#include "ph_com_spi.h"
#include "ph_com_uart.h"


#define _USE_SPI_PIN 22


static bool _use_spi = true;


#define _COM(x_func, ...) { \
		if (ph_g_is_bridge) { \
			ph_com_bridge_##x_func(__VA_ARGS__); \
		} else if (_use_spi) { \
			ph_com_spi_##x_func(__VA_ARGS__); \
		} else { \
			ph_com_uart_##x_func(__VA_ARGS__); \
		} \
	}


void ph_com_init(void (*data_cb)(const u8 *), void (*timeout_cb)(void)) {
	gpio_init(_USE_SPI_PIN);
	gpio_set_dir(_USE_SPI_PIN, GPIO_IN);
	gpio_pull_up(_USE_SPI_PIN);
	sleep_ms(10); // Нужен небольшой слип для активации pull-up
	_use_spi = gpio_get(_USE_SPI_PIN);
	_COM(init, data_cb, timeout_cb);
}

void ph_com_task(void) {
	_COM(task);
}

void ph_com_write(const u8 *data) {
	_COM(write, data);
}
