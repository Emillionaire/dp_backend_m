Create new OS user:
ssh root@<server_ip>
adduser <username>
usermod <username> -aG sudo
usermod www-data -aG <username>
su <username>
cd ~

- Configurate Ubuntu:
  - sudo apt update
  - sudo apt install python3-venv python3-pip postgresql nginx expect -y
  - sudo systemctl status postgresql
  - sudo systemctl start postgresql

- Configurate Postgresql:
  - sudo su postgres
  - psql
  - CREATE USER <username> WITH SUPERUSER;
  - ALTER USER <username> WITH PASSWORD <password>;
  - CREATE DATABASE <username>;
  - exit
  - su <username>
  - psql
  - CREATE DATABASE <database_name>;
  - exit

- Clone the project:
  - d ~
  - git clone https://github.com/Emillionaire/dp_backend_m.git
  - cd dp_backend_m/dp_backend_m/
  - sudo nano .env

- .env file:
```
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
ENGINE=
NAME=
HOST=
PORT=
USER=
PASSWORD=
CORS_ALLOWED_ORIGINS=
```

Create virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Project migrations:
python manage.py makemigrations
python manage.py makemigrations cloud
python manage.py migrate

Create admin user for app:
python manage.py createsuperuser

Nginx:
sudo systemctl start nginx
sudo systemctl enable nginx

[project in /etc/nginx/sites-available/]
server {
        listen 80;
        server_name <server_ip>;
        client_max_body_size 100M;

        root  /usr/share/nginx/html;
        index index.html;

        location / {
                try_files $uri /index.html;
}

        location ~  \.(js|css)$ {
                rewrite ^.+?(/assets/.*) $1 break;
}

        location /backend/ {
                include proxy_params;
                rewrite ^/backend(.*) $1 break;
                proxy_pass http://unix:/home/<username>/dp_backend_m/dp_backend_m/dp_backend_m/project.sock;
        }
}

sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/
sudo systemctl restart nginx

[Gunicorn]
sudo apt install gunicorn -y
pip install gunicorn

[gunicorn.service in /etc/systemd/system/]
[Unit]
Description=service for gunicorn
After=network.target

[Service]
User=eveline
Group=www-data
WorkingDirectory=/home/eveline/dp_backend_m
ExecStart=/home/eveline/dp_backend_m/venv/bin/gunicorn --access-logfile - --workers=3 -b unix:/home/eveline/dp_backend_m/dp_backend_m/dp_backend_m/project.sock NetoCloud.wsgi:application

[Install]
WantedBy=multi-user.target


sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn