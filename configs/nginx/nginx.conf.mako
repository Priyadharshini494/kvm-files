worker_processes 4;

# error_log /tmp/rutomatrix-nginx.error.log;
error_log stderr;

include /usr/share/rutomatrix/extras/*/nginx.ctx-main.conf;

events {
	worker_connections 1024;
	use epoll;
	multi_accept on;
}

http {
	types_hash_max_size 4096;
	server_names_hash_bucket_size 128;

	access_log off;

	include /etc/rutomatrix/nginx/mime-types.conf;
	default_type application/octet-stream;
	charset utf-8;

	sendfile on;
	tcp_nodelay on;
	tcp_nopush on;
	keepalive_timeout 10;
	client_max_body_size 4k;

	client_body_temp_path	/tmp/rutomatrix-nginx/client_body_temp;
	fastcgi_temp_path		/tmp/rutomatrix-nginx/fastcgi_temp;
	proxy_temp_path			/tmp/rutomatrix-nginx/proxy_temp;
	scgi_temp_path			/tmp/rutomatrix-nginx/scgi_temp;
	uwsgi_temp_path			/tmp/rutomatrix-nginx/uwsgi_temp;

	include /etc/rutomatrix/nginx/rutomatrix.ctx-http.conf;
	include /usr/share/rutomatrix/extras/*/nginx.ctx-http.conf;

	% if https_enabled:

	server {
		listen ${http_port};
		% if ipv6_enabled:
		listen [::]:${http_port};
		% endif
		include /etc/rutomatrix/nginx/certbot.ctx-server.conf;
		location / {
			% if https_port == 443:
			return 301 https://$host$request_uri;
			% else:
			return 301 https://$host:${https_port}$request_uri;
			% endif
		}
	}

	server {
		listen ${https_port} ssl;
		% if ipv6_enabled:
		listen [::]:${https_port} ssl;
		% endif
		http2 on;
		include /etc/rutomatrix/nginx/ssl.conf;
		include /etc/rutomatrix/nginx/rutomatrix.ctx-server.conf;
		include /usr/share/rutomatrix/extras/*/nginx.ctx-server.conf;
	}

	% else:

	server {
		listen ${http_port};
		% if ipv6_enabled:
		listen [::]:${http_port};
		% endif
		include /etc/rutomatrix/nginx/certbot.ctx-server.conf;
		include /etc/rutomatrix/nginx/rutomatrix.ctx-server.conf;
		include /usr/share/rutomatrix/extras/*/nginx.ctx-server.conf;
	}

	% endif
}
