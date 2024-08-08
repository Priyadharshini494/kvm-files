#pragma once

#include "ph_types.h"


inline u16 ph_crc16(const u8 *buf, uz len) {
	const u16 polinom = 0xA001;
	u16 crc = 0xFFFF;

	for (uz byte_count = 0; byte_count < len; ++byte_count) {
		crc = crc ^ buf[byte_count];
		for (uz bit_count = 0; bit_count < 8; ++bit_count) {
			if ((crc & 0x0001) == 0) {
				crc = crc >> 1;
			} else {
				crc = crc >> 1;
				crc = crc ^ polinom;
			}
		}
	}
	return crc;
}

inline s16 ph_merge8_s16(u8 a, u8 b) {
	return (((int)a << 8) | (int)b);
}

inline u16 ph_merge8_u16(u8 a, u8 b) {
	return (((u16)a << 8) | (u16)b);
}

inline void ph_split16(u16 from, u8 *to_a, u8 *to_b) {
	*to_a = (u8)(from >> 8);
	*to_b = (u8)(from & 0xFF);
}
