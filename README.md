# Install requirements
sudo apt update
sudo apt install nginx certbot python3 python3-certbot-nginx python3.10-venv

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
    include /home/nginx-manager/conf.d/*.conf;
}

# -> add sample html for test
su application

mkdir -p /home/application/web/application.local/public_html/application.local
vi /home/application/web/application.local/public_html/index.html

```html
<h1>Running</h1>
```

exit

# -> add sample nginx conf for application.local
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
nginx-manager ALL=NOPASSWD: /usr/sbin/nginx -t, /usr/sbin/nginx -s reload, /usr/bin/certbot, /usr/bin/certbot-auto
sudo chmod +x /home/nginx-manager

# Clone project
su nginx-manager
cd /home/nginx-manager
git clone git@github.com:tunglq-levincigroup/nginx-domain-manager.git .

# edit file .evn
cd nginx-domain-manager
cp .env.sample .env

# Set up project
python3 -m venv .venv
./.venv/bin/pip3 install -r requirements.txt
./.venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app

# Test project run local
curl http://localhost:8000
-> Result: {"status":"running"}

# Test
curl -X POST http://192.168.68.84:8000/domain/add -H "Content-Type: application/json" -d '{"domain": "example.com"}'
curl -X PUT http://192.168.68.84:8000/domain/edit -H "Content-Type: application/json" -d '{"new_domain": "example.com", "old_domain": "old.example.com"}'
curl -X DELETE http://192.168.68.84:8000/domain/remove -H "Content-Type: application/json" -d '{"domain": "example.com"}'