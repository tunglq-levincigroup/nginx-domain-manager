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

See [APIS](https://github.com/tunglq-levincigroup/nginx-domain-manager/tree/main/docs/apis)

## License

This project is licensed under the [MIT License](LICENSE).

# Installation
```bash
sudo apt update
sudo apt install nginx python3 python3.10-venv certbot python3-certbot-nginx
```

## Install base source
```bash
sudo adduser application
sudo mkdir -p /home/application/web/test4.test88.info/public_html/ 
sudo chown application:application /home/application/web/test4.test88.info/public_html/ -R
sudo usermod -aG application www-data
sudo usermod -aG www-data application
```

## Install user for nginx manager
```bash
sudo adduser nginx-manager
sudo mkdir /home/nginx-manager/conf.d/
sudo chown nginx-manager:nginx-manager /home/nginx-manager/conf.d/ -R
sudo usermod -aG nginx-manager www-data
sudo usermod -aG www-data nginx-manager
sudo usermod -aG nginx-manager application
```

## Dựng trang web gốc
```bash
su application

mkdir -p /home/application/web/test4.test88.info/public_html/test4.test88.info
vi /home/application/web/test4.test88.info/public_html/index.html
```

```html
<h1>Running</h1>
```

```bash
exit
```

## Include config folder
```bash
sudo vi /etc/nginx/nginx.conf
```

```
# /etc/nginx/nginx.conf
{
    ...
    include include /home/nginx-manager/conf.d/**/*.conf;
}
```

## Add config for base domain

```bash
su nginx-manager
vi /home/nginx-manager/conf.d/test4.test88.info.conf
```

```
# /home/nginx-manager/conf.d/test4.test88.info.conf
server {
    listen 80;
    server_name test4.test88.info;

    root /home/application/web/test4.test88.info/public_html/;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
exit
```

## Eeload nginx
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Test first config
Add host to local computer hosts file
Open browser -> test4.test88.info

## Set up nginx manager server with sudo permission
```bash
sudo visudo
nginx-manager ALL=NOPASSWD: /usr/sbin/nginx -t, /usr/sbin/nginx -s reload, /usr/bin/certbot, /usr/bin/certbot-auto
sudo chmod +x /home/nginx-manager
```

## Config ssl for base domain
```bash
sudo certbot --nginx -d test4.test88.info --agree-tos --email alert@levincigroup.com
```

## Clone nginx manager
```bash
su nginx-manager
cd /home/nginx-manager
git clone git@github.com:tunglq-levincigroup/nginx-domain-manager.git
```

# edit file .evn
```bash
cd /home/nginx-manager/nginx-domain-manager
cp .env.sample .env
```

## Set up project
### For production
```bash
cd /home/nginx-manager/nginx-domain-manager
python3 -m venv .venv
./.venv/bin/pip3 install -r requirements.txt
./.venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app

exit
```

### Run with systemd and auto restart on failure
```bash
sudo vi /etc/systemd/system/nginx-manager.service
```

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
```bash
curl http://localhost:8000
```