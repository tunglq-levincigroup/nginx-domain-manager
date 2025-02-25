def generate_http(domain: str):
    return f'''
server {{
    listen 80;
    server_name {domain};

    access_log /var/log/nginx/{domain}.log;
    error_log /var/log/nginx/{domain}.error.log;

    root /home/application/web/application.local/public_html/;
    index index.html;

    location / {{
        try_files $uri $uri/ =404;
    }}
}}
'''
