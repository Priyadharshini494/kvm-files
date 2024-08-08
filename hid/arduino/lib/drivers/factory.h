#pragma once

#include "keyboard.h"
#include "mouse.h"
#include "storage.h"
#include "board.h"
#include "connection.h"


namespace DRIVERS {
	struct Factory {
		static Keyboard *makeKeyboard(type _type);
		static Mouse *makeMouse(type _type);
		static Storage *makeStorage(type _type);
		static Board *makeBoard(type _type);
		static Connection *makeConnection(type _type);
	};
}
