# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

# My config for web server
package "nginx"
# Use nginx default config as VM config
cookbook_file "nginx-default" do
  path "/etc/nginx/sites-available/default"
end
service "nginx" do
	action :reload
end

# My config for database
package "postgresql"
execute "init_database" do
  command  'echo "CREATE DATABASE mydb; CREATE USER ubuntu; GRANT ALL PRIVILEGES ON DATABASE mydb TO ubuntu;" | sudo -u postgres psql'
end

# Initialize python dependencies
package "python3"
package "python3-pip"

execute "pip_upgrade" do
	command "pip3 install -U pip"
end

execute "install_denpendencies" do
	command "pip3 install -r requirements.txt"
	cwd "/home/ubuntu/project/webroot"
end

# install redis
package "redis-server"
execute "start_redis" do
	command "redis-server &"
end

# start service
execute "start_service" do
    user "ubuntu"
    command "python3 manage.py &"
    cwd "/home/ubuntu/project/webroot"
end
