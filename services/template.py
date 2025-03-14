
############################# latest function to config ssl
def generate_nginx_ssl_conf_with_redirect(base_domain: str, redirect_domain: str, target_domain: str) -> str:
    """
    Generates an Nginx configuration for a given domain.

    Args:
        base_domain         (str): The base domain or upstream server.
        redirect_domain:    (str): The domain that redirect to target_domain when accessing.
        target_domain       (str): The domain for which the config is generated.

    Returns:
        str: The generated Nginx configuration.
    """
    return f"""# Generated for {target_domain} from the {base_domain} config template
# Domain {redirect_domain} with redirect to {target_domain}

# Main config
server {{
    listen 443 ssl;
    server_name {target_domain};

    access_log /var/log/nginx/{target_domain}.log;
    error_log /var/log/nginx/{target_domain}.error.log;

    ssl_trusted_certificate /etc/letsencrypt/live/{target_domain}/cert.pem;
    ssl_certificate /etc/letsencrypt/live/{target_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{target_domain}/privkey.pem;
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

# Redirect from http://{target_domain} to https://{target_domain}
server {{
    listen 80;
    server_name {target_domain};
    return 301 https://{target_domain}$request_uri;
}}

# Redirect from http://{redirect_domain} to https://{target_domain}
server {{
    listen 80;
    server_name {redirect_domain};
    return 301 https://{target_domain}$request_uri;
}}

# Redirect from https://{redirect_domain} to https://{target_domain}
server {{
    listen 443 ssl;
    server_name {redirect_domain};

    ssl_certificate /etc/letsencrypt/live/{redirect_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{redirect_domain}/privkey.pem;

    return 301 https://{target_domain}$request_uri;
}}
"""

############################# for domain controller, not up to date
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

############################# for domain controller, not up to date
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