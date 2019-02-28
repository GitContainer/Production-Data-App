*Updates*

#  V1.1:
    - Chagend machines and record icon
    - Changed the order of the production record so the first rows of the table corresponds to the closest date
    - Added pagination in prodcution record so it display only the last week production
    - Added new section: Production per hour, which shows every pph graph and a total pph graph
    - Repaired PLC so in case of power failure the data remains as it was
    - Added production line graph for every machine, restyled information and added work efficiency
    - Modified velocity graph so it can display up to 2800 points, with a scroll bar and a play/pause button.
    - Added Stops histogram
    - Added production and stops records to csv buttons





## Instructions

1. Install snap7 library and nginx:
    $ sudo add-apt-repository ppa:gijzelaar/snap7
    $ sudo apt-get update
    $ sudo apt-get install libsnap7-1 libsnap7-dev
    $ sudo apt-get install nginx
2. Configure nginx:
    $ sudo /etc/init.d/nginx start
    $ sudo rm /etc/nginx/sites-enabled/default
    $ sudo touch /etc/nginx/sites-available/flask_settings
    $ sudo ln -s /etc/nginx/sites-available/flask_settings /etc/nginx/sites-enabled/flask_settings
    $ vi /etc/nginx/sites-enabled/flask_settings
        server {
        listen 80;
        server_name 192.168.8.139;

        location /static {
                alias /home/ubntuadmin/applications/Production-Data-App/production_data_app/static;
        }

        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }

        location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.0.1:8000/socket.io;
        }
}
    $ sudo /etc/init.d/nginx restart
3. Install and configure postgresql
4. Install pip:
    $ sudo apt-get install python3-pip
5. Install python's virtualenv:
    $ pip3 install virtualenv
6. Clone Project:
    $ git clone https://github.com/JulioSanchezD/Production-Data-App.git
7. On your main folder, run the following command:
    $ virtualenv venv
8. Create alias for virtualenv's activation:
    $ cd
    $ alias activate='source venv/bin/activate' > ~/.bashrc
    $ source ~/.bashrc
9. Activate virtualenv on main folder:
    $ activate
10. Install libraries:
    $ pip install -r requirements.txt
11. Modify __init__.py line: app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql                  +psycopg2://postgres:username@host/production_data'
12. Modify /data_acquisition/create.py paths
13. Create data base tables:
    $ cd /data_base/
    $ python create.py
14. Create users for login:
    $ python userRegister.py
15. Run the application for testing:
    $ gunicorn --worker-class eventlet -w 1 run:app
16. Install and configure supervisor:
    $ sudo apt install supervisor
    $ sudo nano /etc/supervisor/conf.d/applications.conf
        [program:flaskWebServer]
        directory=/home/ubuntuadmin/applications/Production-Data-App
        command=/home/ubuntuadmin/applications/Production-Data-App/venv/bin/gunicorn --worker-class eventlet -w 1 run:app
        user=ubntuadmin
        autostart=true
        autorestart=true
        stopasgroup=true
        killasgroup=true
        stderr_logfile=/var/log/applications/production_data_app.err.log
        stdout_logfile=/var/log/applications/production_data_app.out.log
        [program:opcServer]
        directory=/home/ubuntuadmin/applications/Production-Data-App/
        command=/home/ubuntuadmin/venv/bin/python data_acquisition/opcServer.py
        user=ubntuadmin
        autostart=true
        autorestart=true
        stopasgroup=true
        killasgroup=true
        stderr_logfile=/var/log/applications/opcServer.err.log
        stdout_logfile=/var/log/applications/opcServer.out.log
17. Create log files (main folder):
    $ sudo mkdir -p /var/log/production_data_app
    $ sudo touch /var/log/applications/production_data_app.err.log
    $ sudo touch /var/log/applications/production_data_app.out.log
    $ sudo touch /var/log/applications/opcServer.err.log
    $ sudo touch /var/log/applications/opcServer.out.log
18. Run server:
    $ sudo supervisorctl reload
19. Verify:
    $ sudo service supervisor status