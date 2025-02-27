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