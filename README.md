# -> built source code
sudo adduser application
sudo mkdir -p /home/application/web/application.local/public_html/ 
sudo chown application:application /home/application/web/application.local/public_html/ -R
sudo usermod -aG application www-data
sudo usermod -aG www-data application

# -> nginx conf for multi tenants
sudo adduser nginx-manager
sudo mkdir /home/nginx-manager/conf.d/*
sudo chown application:application /home/nginx-manager/conf.d/ -R
sudo usermod -aG nginx-manager www-data
sudo usermod -aG www-data nginx-manager

# -> include config to nginx.conf
sudo vi /etc/nginx/nginx.conf
{
    ...
    include /home/nginx-manager/conf.d/*.conf;
}

# -> add sample nginx conf for application.local
su nginx-manager
vi conf.d/application.local.conf

server {
    listen 80;
    server_name application.local;

    root /home/application/web/application.local/public_html/;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# -> reload nginx
nginx -t
systemctl reload nginx

# -> Test first config
# Add host to local computer hosts file
# Open browser -> application.local

# Set up nginx manager server
sudo visudo
nginx-manager ALL=NOPASSWD: /usr/sbin/nginx -t, /usr/sbin/nginx -s reload
sudo chmod +x /home/nginx-manager

# Install certbot 
sudo apt install certbot python3-certbot-nginx

# Test command
sudo certbot --nginx -d application.local

# Clone project
git clone ...
# edit file .evn

# Set up project
python -m venv .venv
./venv/bin/pip install -r requirements.txt
./venv/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app

# Test project run local
curl http://localhost:8000
-> Result: {"status":"running"}

# Test
curl -X POST http://192.168.68.84:8000/domain/add -H "Content-Type: application/json" -d '{"domain": "example.com"}'
curl -X PUT http://192.168.68.84:8000/domain/edit -H "Content-Type: application/json" -d '{"new_domain": "example.com", "old_domain": "old.example.com"}'
curl -X DELETE http://192.168.68.84:8000/domain/remove -H "Content-Type: application/json" -d '{"domain": "example.com"}'