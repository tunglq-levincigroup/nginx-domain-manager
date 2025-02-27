def generate_nginx_conf(base_domain: str, domain: str):
    return f'''# Generated for {domain} from the {base_domain} config template

server {{
    listen 80;
    server_name {domain};

    access_log /var/log/nginx/{domain}.log;
    error_log /var/log/nginx/{domain}.error.log;

    location / {{
        proxy_pass {base_domain}
        try_files $uri $uri/ =404;
    }}
}}
'''
