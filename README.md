# Nginx Domain Manager

## Summary

This project is used for auto-configuring domain names and providing free Certbot SSL for a multi-tenant system.

## Features

- Create, update, and delete specific domains

## Tech Stack

- **Backend:** Python, Flask, Gunicorn server
- **Infrastructure services:** Nginx, Certbot

## Prerequisites

- Nginx installed and configured
- Certbot installed for SSL certificates
- Python 3.10 or higher

## Folder Structure

```
nginx-domain-manager/
|-- controllers/
|-- services/
|-- .env
|-- .env.sample
|-- app.py
|-- wsgi.py
|-- README.md
```

## Integrations

The Nginx Domain Manager exposes a simple and robust HTTP-based API for managing domain configurations. Below are the available endpoints and their usage examples.



### CNAME Record Integrations

#### Get TXT info
Request certbot to generate an TXT record

```json
Endpoint: GET /cname/get-txt

Request:

curl -X DELETE http://{SERVER_IP}:{SERVER_PORT}/cname/get-txt \
     -H "Content-Type: application/json" \
     -d '{"domain": {DOMAIN_NAME}}'

Response:

{
    "message": "",
    "data": {
        "domain": "",
        "value": "",
        "ttl": "",
        "": ""
    }
}
```

#### Verify the TXT record
Request a verification for ensuring TXT record added correctly.

```json
Endpoint: GET /cname/verify-txt

Request:

curl -X DELETE http://{SERVER_IP}:{SERVER_PORT}/cname/verify-txt \
     -H "Content-Type: application/json" \
     -d '{"domain": {DOMAIN_NAME}}'

Response:

{
  "message": "Domain removed successfully",
  "domain": {DOMAIN_NAME}
}
```

### Environment Variables

## Environment Variables

| Variable      | Description              |
| ------------- | ------------------------ |
| `SERVER_IP`   | IP address of the server |
| `SERVER_PORT` | Port number for the API  |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a pull request

## License

This project is licensed under the [MIT License](LICENSE).

# Install requirements
sudo apt update
sudo apt install nginx python3 python3.10-venv

# -> built source code
sudo adduser application
sudo mkdir -p /home/application/web/application.local/public_html/ 
sudo chown application:application /home/application/web/application.local/public_html/ -R
sudo usermod -aG application www-data
sudo usermod -aG www-data application

# -> nginx conf for multi tenants
sudo adduser nginx-manager
sudo mkdir /home/nginx-manager/conf.d/
sudo chown nginx-manager:nginx-manager /home/nginx-manager/conf.d/ -R
sudo usermod -aG nginx-manager www-data
sudo usermod -aG www-data nginx-manager
sudo usermod -aG nginx-manager application

# -> include config to nginx.conf
sudo vi /etc/nginx/nginx.conf
{
    ...
    include include /home/nginx-manager/conf.d/**/*.conf;
}

# Dựng trang web gốc
su application

mkdir -p /home/application/web/application.local/public_html/application.local
vi /home/application/web/application.local/public_html/index.html

```html
<h1>Running</h1>
```

exit

# -> Config trang web gốc
su nginx-manager
vi /home/nginx-manager/conf.d/application.local.conf

server {
    listen 80;
    server_name application.local;

    root /home/application/web/application.local/public_html/;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

exit

# -> reload nginx
sudo nginx -t
sudo systemctl reload nginx

# -> Test first config
# Add host to local computer hosts file
# Open browser -> application.local

# Set up nginx manager server with sudo permission
sudo visudo
nginx-manager ALL=NOPASSWD: /usr/sbin/nginx -t, /usr/sbin/nginx -s reload
sudo chmod +x /home/nginx-manager

# Install
su nginx-manager
curl https://get.acme.sh | sh
export PATH="~/.acme.sh:$PATH"
exit

sudo certbot --nginx -d test4.levincitest.com --agree-tos --email tung.le@levincigroup.com --dry-run

server {
    listen 80;
    server_name test4.levincitest.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Các cấu hình khác của server
}


# Clone project
su nginx-manager
source ~/.bashrc
cd /home/nginx-manager
git clone git@github.com:tunglq-levincigroup/nginx-domain-manager.git

# edit file .evn
cd /home/nginx-manager/nginx-domain-manager
cp .env.sample .env

# Set up project
### For production
cd /home/nginx-manager/nginx-domain-manager
python3 -m venv .venv
./.venv/bin/pip3 install -r requirements.txt
./.venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app

exit

### Run with systemd and auto restart on failure
sudo vi /etc/systemd/system/nginx-manager.service

```ini
[Unit]
Description=Nginx Domain Manager
After=network.target

[Service]
User=nginx-manager
Group=nginx-manager
WorkingDirectory=/home/nginx-manager/nginx-domain-manager
ExecStart=/home/nginx-manager/nginx-domain-manager/.venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable nginx-manager
sudo systemctl start nginx-manager
sudo systemctl status nginx-manager
```


# Test project run local
curl http://localhost:8000
-> Result: {"status":"running"}

# Test
curl -X POST http://192.168.68.84:8000/domain/add -H "Content-Type: application/json" -d '{"domain": "example.com"}'
curl -X PUT http://192.168.68.84:8000/domain/edit -H "Content-Type: application/json" -d '{"new_domain": "example.com", "old_domain": "old.example.com"}'
curl -X DELETE http://192.168.68.84:8000/domain/remove -H "Content-Type: application/json" -d '{"domain": "example.com"}'