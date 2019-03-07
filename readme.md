# CICD_runner_adapter
![Here](./readme_image/AsiabotsCI_CD.png)

An adapter for virtual environment, to request api for update docker image, you should clone the adapter in your deploy location (e.g EC2, EBS) <br >
Demo video:https://www.youtube.com/watch?v=BXaibSEF5FU 

## Requirements
Gitlab account

## Adapter API:
[POST:GET] /update_docker <br >
[POST:GET] /run_docker <br >

## 1. add .gitlab-ci.yml in the project
1. .gitlab-ci.yml is a file for gitlab to kick start the CICD function, add to your project before doing the following step. 
2. Set up your .gitlab-ci.yml file in 3 stages : build for environment testing, test for unit testing, deploy for deployment testing. <br >
Build for build testing, such as install the requirement in differ vision <br >
Test for unit testing, such as run the server in code level, and test to build the docker image <br >
Deploy for deployment testing, deploy the docker image in to docker hub <br >

e.g NodeJS example
```
stages:
  - build
  - test
  - deploy

buildtest-node:
  image: node:latest
  stage: build
  script:
    - apt-get update -qy
    - npm install

unittest-node:
  image: node:latest

  stage: test
  script:
    - apt-get update -qy
    - npm install

docker-test:
  image: docker:latest
  services:
    - docker:dind
  stage: test
  script:
  - docker login registry.gitlab.com -u wilsonlo1997@gmail.com -p Vi26151851@
  - docker build -t registry.gitlab.com/asiabots/wilson/cantonese-nlp .
  - docker run -d -p 5000:8080 registry.gitlab.com/asiabots/wilson/cantonese-nlp

docker-deploy:
  image: docker:latest
  services:
      - docker:dind
  stage: deploy
  script:
      - docker login registry.gitlab.com -u wilsonlo1997@gmail.com -p Vi26151851@
      - docker build -t registry.gitlab.com/asiabots/wilson/cantonese-nlp .
      - docker push registry.gitlab.com/asiabots/wilson/cantonese-nlp
  only:
      - master
```

e.g Python example
```
stages:
  - build
  - test
  - deploy

buildtest-python:
  stage: build
  script:
    - apt-get update -qy
    - apt-get install -y python-dev python-pip
    - pip install -r requirements.txt
  tags:
    - python2.7

unittest-py27:
  stage: test
  script:
    - apt-get update -qy
    - apt-get install -y python-dev python-pip
    - pip install -r requirements.txt
    - nohup python Main.py &
    - pocha unittest.py
  tags:
    - python2.7

unittest-py34:
  stage: test
  script:
    - apt-get update -qy
    - apt-get install -y python-dev python-pip
    - pip install -r requirements.txt
    - nohup python Main.py &
    - pocha unittest.py
  tags:
    - python3/4

docker-test:
  image: docker:latest
  services:
    - docker:dind
  stage: test
  script:
    - docker login -u wilsonloltl -p Vi26151851@
    - docker build -t wilsonloltl/docker_cicd_testing:cicd-demo .
    - docker run -d -p 5000:8080 wilsonloltl/docker_cicd_testing:cicd-demo
  only:
    - master

docker-deploy:
  image: docker:latest
  services:
    - docker:dind
  stage: deploy
  script:
    - docker login -u wilsonloltl -p Vi26151851@
    - docker build -t wilsonloltl/docker_cicd_testing:cicd-demo .
    - docker push wilsonloltl/docker_cicd_testing:cicd-demo
  only:
    - master
    
eb-deploy:
  stage: deploy
  script:
    - bash eb-deploy.sh
    - eb init testing-env -r ap-southeast-1 -p docker
    - eb deploy testing-env2
  tags:
    - eb-deploy
    
```

*PS: You should regisiter a docker hub account and create a new repo for the project, also modify the following code in deploy stage to deploy
![Here](./readme_image/pic4.png)
```
docker-deploy:
  image: docker:latest
  services:
    - docker:dind
  stage: deploy
  script:
    - docker login -u USERNAME -p PASSWORD
    - docker build -t registry.gitlab.com/REPO_NAME
    - docker push registry.gitlab.com/REPO_NAME
  only:
    - master
```
3. update your project into gitlab, before push the project, you can check the format in gitlab, which locate in CI/CD -> Pipeline -> CI Lint
![Here](./readme_image/pic1.png)
4. If the file follow format,git CI will start running, you can take a look in CI/CD Pipeline, for more detail,just click it :D
![Here](./readme_image/pic2.png)

## 2. Set up the adapter in your locate environment (docker vision)
For sure, enter to your EC2 or EBS by ssh, clone and cd the adapter

1. Install the following requirements
```
cd cicd_adapter
sudo bash config_setting.sh
```
2. Modify update.sh file and run_docker.sh
```
line2: Your docker hub account and password
line3: Pull the docker image -> registry.gitlab.com/REPO_NAME
line4: The port connect to docker exposed port -> LOCATEPORT:DOCKERPORT
```
3. Auto setting
```
cd /usr/sbin
sudo touch api.sh
sudo chown root:root api.sh
sudo chmod +x api.sh
sudo nano api.sh
code in api.sh:
    cd /home/$USER/cicd_adapter
    python Main.py
crontab -e
add in the last line: @reboot /usr/sbin/api.sh
For EBS: press ESC, :wq to leave
For ec2: press control+x , y to leave
sudo reboot
```
The adapter should be auto kick start after reboot in port 8080

### Detail for update.sh
```
#!/usr/bin/env bash
sudo docker login registry.gitlab.com -u wilsonlo1997@gmail.com -p Vi26151851@  -- Login the Gitlab account
sudo docker pull registry.gitlab.com/asiabots/wilson/cantonese-nlp  --  Pull th image
sudo docker stop $(sudo docker ps -aq)  -- Stop all container
sudo docker rm $(sudo docker ps -aq)  -- Remove all container
sudo docker run -d -p 5000:5000 registry.gitlab.com/asiabots/wilson/cantonese-nlp  -- Run the container again
```

## 2.Set up the adapter in your locate environment (code vision)
For sure, enter to your EC2 or EBS by ssh, clone and cd the adapter <br >
To cloen the gitlab project with out SSH, you need to generate a access_token in gitlab:
"Setting" -> "Access Token" -> Enter the name and Expire date -> Tick all the Scopes (except api) -> create and copy the access_token <br >
And then change your clone code to :git clone https://USERNAME:ACCESS_TOKEN@gitlab.com/xxx/xxx/xxx.git/ <br >
e.g: git clone https://WilsonLTL:QxSC_AAhGbVH5BQyYvTC@gitlab.com/asiabots/wilson/cantonese-nlp.git
![Here](./readme_image/pic5.png)

1. Install the following requirements
```
cd cicd_adapter
sudo bash config_setting.sh
```
2. Modify code_init file
```
line3: clone your target project (if user_name and password are needed, please enter it too)
e.g git clone 
```
3. Modify update_code file
```
Line2: cd to the project location
```
4. Autosetting in cicd_adapter
```
cd /usr/sbin
sudo touch api.sh
sudo chown root:root api.sh
sudo chmod +x api.sh
sudo nano api.sh
code in api.sh:
    cd /home/$USER/cicd_adapter
    python Main.py
crontab -e
add in the last line: @reboot /usr/sbin/api.sh
For EBS: press ESC, :wq to leave
For ec2: press control+x , y to leave
sudo reboot
```
The adapter should be auto kick start after reboot in port 8080

5. Auto setting in your project
```
cd /usr/sbin
sudo touch server.sh
sudo chown root:root server.sh
sudo chmod +x server.sh
sudo nano api.sh
code in api.sh:
    cd /home/$USER/PROJECT
    -- for python: python Main.py
    -- for node: http-server -p 80 , or as you want (remeber to install it too)
crontab -e
add in the last line: @reboot /usr/sbin/server.sh
For EBS: press ESC, :wq to leave
For ec2: press control+x , y to leave
sudo reboot
```

### 3. CD part
There are two type of CD : Manual CD and Auto CD :<br >
1. Manual CD, after the Pipeline is finish, then you can send a request to the adapter server to update the docker dile: <br >
 HOSTADDRESS:PORT/update_docker, POST or GET is ok too.<br >
 If your ec2/ebs restart, you should call the server to run the docker: <br >
 HOSTADDRESS:PORT/run_docker, POST or GET is ok too. <br >
 If you are using code vision : <br>
 
the system will auto pull the latest vision of docker hub and restart the container.
3. Auto CD, you can modify the code in .gitlab-ci.yml - deploy part, to curl a request to adapter after push the image into docker hub.

### 3.1 CD to EBS
To deploy the docker file to EBS, please follow the following step
```
1. Install EB CLI in your localhost, finish the init (eb init)
2. Create a new deploy env for the project (eb create $envname)
3. If the init successful, Please modify EB-deploy stage in CI tags to your target deploy runner
```

EB-Deploy runner setting
```
1. sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
2. sudo chmod +x /usr/local/bin/gitlab-runner
3. curl -sSL https://get.docker.com/ | sh
4. sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash
5. sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
6. sudo gitlab-runner regisiter
7. In your gitlab project, go to CICD -> Environment variables -> set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from credentials.csv (IAM account in aws,full permission)
8. In eb-eploy, modify CI file, add tags to point to your runner (if u need).
```

To deploy your app to EBS, please make sure that is docker
```
eb-deploy:
  stage: deploy
  script:
    - apt-get update
    - apt-get install -y -qq python python-dev python-pip ca-certificates
    - pip install awsebcli --upgrade --ignore-installed
    - mkdir ~/.aws/
    - touch ~/.aws/credentials
    - printf "[eb-cli]\naws_access_key_id = %s\naws_secret_access_key = %s\n" "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials
    - touch ~/.aws/config
    - printf "[profile eb-cli]\nregion=us-west-2\noutput=json" >> ~/.aws/config
    - eb init application_name -r ap-southeast-1 -p docker
    - eb deploy env_name
```

### 4. Unittest - Mocha & Pocha
You also can run unittest in your project by using mocha or pocha(python vision mocha) <br >
To run the script, just enter "pocha test.py / mocha test.js" <br >
```
from pocha import it,describe
import requests


@describe('routing testing')
def _():
    @it('routing:api system check')
    def test_init():
        url = "http://127.0.0.1:8080/"
        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "7759277d-6293-49e5-b194-5b0a2085b1e1"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        # assert (response.text == "...")

    @it('routing:get_player_card_data')
    def test1():
        url = "http://127.0.0.1:8080/get_player_card_data"
        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "7759277d-6293-49e5-b194-5b0a2085b1e1"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        # assert (response.text == "...")

    @it('routing:get_mission_card_data')
    def test2():
        url = "http://127.0.0.1:8080/get_mission_card_data"
        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "7759277d-6293-49e5-b194-5b0a2085b1e1"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        # assert (response.text == "...")
```


## Option: setup your own gitlab runner
Gitlab Runner is a part for your CI Pipeline, and can assign the Runner to doing differ jobs of Pipeline by "Tags",also,you can deploy your own Runner too.
### 1. set up in EC2 or EBS
```
apt-get update -qy
apt install python-pip
apt install docker.io
sudo docker pull gitlab/gitlab-runner
sudo docker run -d \
--name gitlab-runner-docker \
--restart always \
-v /run/docker.sock:/var/run/docker.sock \
-v /host/path/for/runner:/etc/gitlab-runner \
gitlab/gitlab-runner:latest
sudo docker exec -it gitlab-runner-docker gitlab-runner register
```
PS: Run as sudo if permission denied 
### 2. Register your runner
To register your runner, you need to visit your gitlab project by setting -> CI/CD -> Runners
![Here](./readme_image/pic3.png)
```
Please enter the gitlab-ci coordinator URL:
 - If the project not host in locate gitlab, it should be always https://gitlab.com
Please enter the gitlab-ci token for this runner:
 - Your project CI token, just copy it
Please enter the gitlab-ci description for this runner
 - Write somethings you like 
Please enter the gitlab-ci tags for this runner (comma separated):
 - Improtant: the tags name og Runner will affect you to assign the job to it in .gitlab-ci.yml, give it a "good" tag name
```
After registered, you should able to view the runner in the panel 
