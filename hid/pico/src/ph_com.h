#pragma once

#include "ph_types.h"


void ph_com_init(void (*data_cb)(const u8 *), void (*timeout_cb)(void));
void ph_com_task(void);
void ph_com_write(const u8 *data);
