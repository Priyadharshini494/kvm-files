import {wm2} from "../wm.js";
import {tools, $} from "../tools.js";

export function Camera(){

    var __init__ = function() {

        tools.el.setOnClick($("zoomInButton"), __clickZoominButton);
        tools.el.setOnClick($("zoomOutButton"), __clickZoomoutButton);
        tools.el.setOnClick($("Right"), __clickRightButton);
        tools.el.setOnClick($("Left"), __clickLeftButton);
        tools.el.setOnClick($("Up"), __clickUpButton);
        tools.el.setOnClick($("Down"), __clickDownButton);
	tools.el.setOnClick($("focus-In"), __clickFocusinButton);
	tools.el.setOnClick($("focus-Out"), __clickFocusoutButton);

	$("zoomInButton").title = "Zoom-In";
	$("zoomOutButton").title = "Zoom-Out";
        $("Right").title = "Right";
	$("Left").title = "Left";
	$("Up").title = "Up";
	$("Down").title = "Down";
        $("Auto-focus").title = "Auto-focus";
	$("focus-In").title = "focus-In";
        $("focus-Out").title = "focus-Out";
    }
    var __clickZoominButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/zoomin", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't Zoom-In:<br>", http.responseText);
                }
            }
        });
    };
    var __clickFocusinButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/focusin", function () {
             if (http.readyState === 4) {
		 if (http.status !== 200){
			 wm2.error("Can't Focus-In:<br>", http.responseText);
					 }
			            }
			            });
	        };

    var __clickFocusoutButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/focusout", function () {
             if (http.readyState === 4) {
                 if (http.status !== 200){
                         wm2.error("Can't Focus-Out:<br>", http.responseText);
                                         }
                                    }
                                    });
                };

    var __clickZoomoutButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/zoomout", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't Zoom-Out:<br>", http.responseText);
                }
            }
        });
    };

    var __clickRightButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/right", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't move Right:<br>", http.responseText);
                }
            }
        });
    };

    var __clickLeftButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/left", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't move Left:<br>", http.responseText);
                }
            }
        });
    };

    var __clickUpButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/up", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't move Up", http.responseText);
                }
            }
        });
    };

    var __clickDownButton = function () {
        let http = tools.makeRequest("GET", "/api/camera/down", function () {
            if (http.readyState === 4) {
                if (http.status !== 200) {
                    wm2.error("Can't move Down", http.responseText);
                }
            }
        });
    };

    __init__();
}
