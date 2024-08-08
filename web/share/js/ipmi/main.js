"use strict";


import {$, tools} from "../tools.js";


export function main() {
	__loadRutomatrixInfo();
}

function __loadRutomatrixInfo() {
	let http = tools.makeRequest("GET", "/api/info", function() {
		if (http.readyState === 4) {
			if (http.status === 200) {
				let ipmi_port = JSON.parse(http.responseText).result.extras.ipmi.port;
				let make_item = (comment, ipmi, api) => `
					<span class="code-comment"># ${comment}:<br>$</span>
					ipmitool -I lanplus -U admin -P admin -H ${window.location.hostname} -p ${ipmi_port} ${ipmi}<br>
					<span class="code-comment">$</span> curl -XPOST -HX-Rutomatrix-User:admin -HX-Rutomatrix-Passwd:admin -k \\<br>
					&nbsp;&nbsp;&nbsp;&nbsp;${window.location.protocol}//${window.location.host}/api/atx${api}<br>
				`;
				$("ipmi-text").innerHTML = `
					${make_item("Power on the server if it's off", "power on", "/power?action=on")}
					<br>
					${make_item("Soft power off the server if it's on", "power soft", "/power?action=off")}
					<br>
					${make_item("Hard power off the server if it's on", "power off", "/power?action=off_hard")}
					<br>
					${make_item("Hard reset the server if it's on", "power reset", "/power?action=reset_hard")}
					<br>
					${make_item("Check the power status", "power status", "")}
				`;
			} else if (http.status === 401 || http.status === 403) {
				document.location.href = "/login";
			} else {
				setTimeout(__loadRutomatrixInfo, 1000);
			}
		}
	});
}
