#pragma once

#include "ph_types.h"


extern u8 ph_g_ps2_kbd_leds;
extern bool ph_g_ps2_kbd_online;
extern bool ph_g_ps2_mouse_online;


void ph_ps2_init(void);
void ph_ps2_task(void);

void tuh_kb_set_leds(u8 leds);
void kb_init(u8 gpio_out, u8 gpio_in);
bool kb_task();
void kb_send_key(u8 key, bool state, u8 modifiers);
void ph_ps2_kbd_send_key(u8 key, bool state);

void ms_init(u8 gpio_out, u8 gpio_in);
bool ms_task();
void ms_send_movement(u8 buttons, s8 x, s8 y, s8 z);
void ph_ps2_mouse_send_button(u8 button, bool state);
void ph_ps2_mouse_send_rel(s8 x, s8 y);
void ph_ps2_mouse_send_wheel(s8 h, s8 v);

void ph_ps2_send_clear(void);
