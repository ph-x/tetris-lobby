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
package "sqlite"

# Initialize python dependencies
package "python3"
package "python3-pip"

execute "pip_upgrade" do
	command "pip3 install -U pip"
end

# script "setup_venv" do
# 	interpreter "bash"
# 	cwd "/home/ubuntu/project/webroot"
# 	code <<-EOH
# 	pip3 install virtualenv
# 	virtualenv venv
# 	EOH
# end

execute "install_denpendencies" do
	command "pip3 install -r requirements.txt"
	cwd "/home/ubuntu/project/webroot"
end
# script "install_denpendencies" do
# 	interpreter "bash"
# 	cwd "/home/ubuntu/project/webroot"
# 	code <<-EOH
# 	python3 venv/bin/activate_this.py
# 	pip3 install -r requirements.txt
# 	EOH
# end


# # setup WSGI
execute "install_uwsgi" do
	command "pip3 install uwsgi"
end
cookbook_file "rc.local" do
	path "/etc/rc.local"
end
execute "start-uwsgi" do
	command "bash /etc/rc.local"
end
#execute "start-uwsgi" do
#	command "/usr/local/bin/uwsgi --ini /home/ubuntu/project/webroot/uwsgi.ini --daemonize /var/log/mysite.log"
#end
# execute "setup_uwsgi" do
# 	command "uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app"
# 	cwd "/home/ubuntu/project/webroot"
# end
# execute "start_uwsgi" do
# 	command "/usr/local/bin/uwsgi --ini /home/ubuntu/project/webroot/uwsgi.ini --daemonize /var/log/mysite.log"
# end

# execute "install_gunicorn" do
# 	command "pip3 install gunicorn"
# end
# execute "activate_gunicorn" do
# 	command "gunicorn manage:manager -b localhost:8000 &"
# 	cwd "/home/ubuntu/project/webroot"
# end

# start web service
# execute "start_webapp" do
# 	command "python3 manage.py runserver --host localhost --port 8000 &"
# 	cwd "/home/ubuntu/project/webroot"
# end
