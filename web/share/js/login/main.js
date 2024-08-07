"use strict";


import {tools, $} from "../tools.js";
import {checkBrowser} from "../bb.js";
import {wm, initWindowManager} from "../wm.js";


export function main() {
	if (checkBrowser(null, null)) {
		initWindowManager();

		tools.el.setOnClick($("login-button"), __login);
		$("user-input").onkeyup = $("passwd-input").onkeyup = $("code-input").onkeyup = function(event) {
			if (event.code === "Enter") {
				event.preventDefault();
				$("login-button").click();
			}
		};

		$("user-input").focus();
	}
}

function __login() {
	let user = $("user-input").value;
	if (user.length === 0) {
		$("user-input").focus();
	} else {
		let passwd = $("passwd-input").value + $("code-input").value;
		let body = `user=${encodeURIComponent(user)}&passwd=${encodeURIComponent(passwd)}`;
		let http = tools.makeRequest("POST", "/api/auth/login", function() {
			if (http.readyState === 4) {
				if (http.status === 200) {
					document.location.href = "/";
				} else if (http.status === 403) {
					wm.error("Invalid credentials").then(__tryAgain);
				} else {
					let error = "";
					if (http.status === 400) {
						try { error = JSON.parse(http.responseText)["result"]["error"]; } catch (_) { /* Nah */ }
					}
					if (error === "ValidatorError") {
						wm.error("Invalid characters in credentials").then(__tryAgain);
					} else {
						wm.error("Login error:<br>", http.responseText).then(__tryAgain);
					}
				}
			}
		}, body, "application/x-www-form-urlencoded");
		__setEnabled(false);
	}
}

function __setEnabled(enabled) {
	tools.el.setEnabled($("user-input"), enabled);
	tools.el.setEnabled($("passwd-input"), enabled);
	tools.el.setEnabled($("code-input"), enabled);
	tools.el.setEnabled($("login-button"), enabled);
}

function __tryAgain() {
	__setEnabled(true);
	let el = ($("code-input").value.length ? $("code-input") : $("passwd-input"));
	el.focus();
	el.select();
}
