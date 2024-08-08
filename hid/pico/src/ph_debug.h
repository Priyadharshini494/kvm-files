#pragma once

#include "ph_types.h"


void ph_debug_uart_init();
void ph_debug_act_init();
void ph_debug_act(bool flag);
void ph_debug_act_pulse(u64 delay_ms);
