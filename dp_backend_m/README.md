Create new OS user:
ssh root@<server_ip>
adduser <username>
usermod <username> -aG sudo
usermod www-data -aG <username>
su <username>
cd ~

Configurate Ubuntu:
sudo apt update
sudo apt install python3-venv python3-pip postgresql nginx expect -y
sudo systemctl status postgresql
sudo systemctl start postgresql

Configurate Postgresql:
sudo su postgres
psql
CREATE USER <username> WITH SUPERUSER;
ALTER USER <username> WITH PASSWORD <password>;
CREATE DATABASE <username>;
exit
su <username>
psql
CREATE DATABASE <database_name>;
exit

Clone the project:
cd ~