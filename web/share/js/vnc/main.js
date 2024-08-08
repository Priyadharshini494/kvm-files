"use strict";


import {$, tools} from "../tools.js";


export function main() {
	__loadRutomatrixInfo();
}

function __loadRutomatrixInfo() {
	let http = tools.makeRequest("GET", "/api/info", function() {
		if (http.readyState === 4) {
			if (http.status === 200) {
				let vnc_port = JSON.parse(http.responseText).result.extras.vnc.port;
				$("vnc-text").innerHTML = `
					<span class="code-comment"># How to connect using the Linux terminal:<br>
					$</span> vncviewer ${window.location.hostname}::${vnc_port}
				`;
			} else if (http.status === 401 || http.status === 403) {
				document.location.href = "/login";
			} else {
				setTimeout(__loadRutomatrixInfo, 1000);
			}
		}
	});
}
