# Project installation guide (backend)
- Create new OS user:
  - ssh root@<server_ip>
  - adduser <username>
  - usermod <username> -aG sudo
  - usermod www-data -aG <username>
  - su <username>
  - cd ~

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

- .env file, with some parameters for example:
```
SECRET_KEY=<secret_key>
DEBUG=<1 or 0>
ALLOWED_HOSTS=<server_ip>,127.0.0.1,localhost,0.0.0.0>
ENGINE=<django.db.backends.postgresql>
NAME=<database_name>
HOST=<localhost>
PORT=<5432>
USER=<username>
PASSWORD=<password>
CORS_ALLOWED_ORIGINS=<http://<server_ip>,https://<server_ip>>
```

- Create virtual environment:
  - python3 -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

- Project migrations:
  - python manage.py makemigrations
  - python manage.py makemigrations cloud
  - python manage.py migrate

- Create admin user for app:
  - python manage.py createsuperuser

- Nginx:
  - sudo systemctl start nginx
  - sudo systemctl enable nginx
  - Create file [project in /etc/nginx/sites-available/]
```
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

        location /api/v1/ {
                include proxy_params;
                proxy_pass http://unix:/home/<username>/dp_backend_m/dp_backend_m/dp_backend_m/project.sock;
        }
}
```

  - sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/
  - sudo systemctl restart nginx

- Gunicorn:
  - sudo apt install gunicorn -y
  - pip install gunicorn

- Create file [gunicorn.service in /etc/systemd/system/]
```
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
```

- Start gunicorn:
  - sudo systemctl start gunicorn
  - sudo systemctl enable gunicorn
  - sudo systemctl daemon-reload
  - sudo systemctl restart gunicorn

- Frontend: 