#pragma once

#include "ph_types.h"


u8 ph_cmd_kbd_get_leds(void);
u8 ph_cmd_get_offlines(void);

void ph_cmd_set_kbd(const u8 *args);
void ph_cmd_set_mouse(const u8 *args);

void ph_cmd_send_clear(const u8 *args);
void ph_cmd_kbd_send_key(const u8 *args);
void ph_cmd_mouse_send_button(const u8 *args);
void ph_cmd_mouse_send_abs(const u8 *args);
void ph_cmd_mouse_send_rel(const u8 *args);
void ph_cmd_mouse_send_wheel(const u8 *args);
