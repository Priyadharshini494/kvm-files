#include "tools.h"


bool is_micros_timed_out(unsigned long start_ts, unsigned long timeout) {
	unsigned long now = micros();
	return (
		(now >= start_ts && now - start_ts > timeout)
		|| (now < start_ts && ((unsigned long)-1) - start_ts + now > timeout)
	);
}
