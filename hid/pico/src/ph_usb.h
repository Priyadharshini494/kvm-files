#pragma once

#include "ph_types.h"


extern u8 ph_g_usb_kbd_leds;
extern bool ph_g_usb_kbd_online;
extern bool ph_g_usb_mouse_online;


void ph_usb_init(void);
void ph_usb_task(void);

void ph_usb_kbd_send_key(u8 key, bool state);

void ph_usb_mouse_send_button(u8 button, bool state);
void ph_usb_mouse_send_abs(s16 x, s16 y);
void ph_usb_mouse_send_rel(s8 x, s8 y);
void ph_usb_mouse_send_wheel(s8 h, s8 v);

void ph_usb_send_clear(void);
