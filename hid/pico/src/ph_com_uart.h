#pragma once

#include "ph_types.h"


void ph_com_uart_init(void (*data_cb)(const u8 *), void (*timeout_cb)(void));
void ph_com_uart_task(void);
void ph_com_uart_write(const u8 *data);
