def generate_nginx_conf(base_domain: str, domain: str) -> str:
    """
    Generates an Nginx configuration for a given domain.

    Args:
        base_domain (str): The base domain or upstream server.
        domain (str): The domain for which the config is generated.

    Returns:
        str: The generated Nginx configuration.
    """
    return f"""# Generated for {domain} from the {base_domain} config template

server {{
    listen 80;
    server_name {domain};

    access_log /var/log/nginx/{domain}.log;
    error_log /var/log/nginx/{domain}.error.log;

    location / {{
        proxy_pass https://{base_domain};
        try_files $uri $uri/ =404;
    }}
}}
"""

def generate_nginx_ssl_conf(base_domain: str, domain: str) -> str:
    """
    Generates an Nginx configuration for a given domain.

    Args:
        base_domain (str): The base domain or upstream server.
        domain (str): The domain for which the config is generated.

    Returns:
        str: The generated Nginx configuration.
    """
    return f"""# Generated for {domain} from the {base_domain} config template

server {{
    listen 443 ssl;
    server_name {domain};

    access_log /var/log/nginx/{domain}.log;
    error_log /var/log/nginx/{domain}.error.log;

    ssl_trusted_certificate /etc/letsencrypt/live/{domain}/cert.pem;
    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_protocols             TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers               "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
    ssl_ecdh_curve            secp384r1;
    ssl_session_cache         shared:SSL:10m;
    ssl_session_tickets       off;
    ssl_stapling              on;
    ssl_stapling_verify       on;

    location / {{
        proxy_ssl_server_name on;
        proxy_pass https://{base_domain};

        location / {{
            proxy_pass https://{base_domain};
        }}
        try_files $uri $uri/ =404;
    }}
}}


server {{
    if ($host = {domain}) {{
        return 301 https://$host$request_uri;
    }}

    listen 80;
    server_name {domain};
    return 404;
}}
"""