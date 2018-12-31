# CICD_runner_adapter
A adapter for virtual environment, to request api for update docker image, you should clone the adapter in your deploy location (e.g EC2, EBS)

# set up
1. Install the following requirements
```
apt-get update -qy
apt install python-pip
pip install -r requirements.txt
```
2. Modify update.sh file 
```
line2: Your docker hub account and password
line3: Pull the docker image -> username/repo_name:tagname
line4: The port connect to docker exposed port -> localport:dockerport
```
3. Auto setting
```
cd ~/usr/sbin
sudo touch api.sh
sudo chown root:root api.sh
sudo chmod +x api.sh
sudo nano api.sh
code in api.sh:
    cd /home/USERNAME/CICD_Adapter
    python3 Main.py
crontab -e
add in the last line: @reboot /usr/sbin/api.sh
For EBS: press ESC, :wq to leave
For ec2: press control+x , y to leave
sudo reboot
```
The adapter should be auto kick start after reboot in port 8080