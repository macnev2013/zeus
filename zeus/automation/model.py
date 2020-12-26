from jinja2 import Template

jenkins_template = """
{% for key, value in env.items() %}def {{ key }} = {{ value }}
{% endfor %}
Pipeline {
    agent {
        docker {
            image '{{ build_image }}'
            {% if build_args != None %}args '{{ build_args }}'{% endif %}
        }
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '7'))
    }
    stages {
        stage('Build') {
            steps{
                script {
                    if (env.BRANCH_NAME == "${production_branch}" ) {
                        sshagent(["${sshagent_name}"]) {

                            {% for command in prod_build_stage_commands %}sh "{{ command }}"
                            {% endfor %}
                        }
                    } else if (env.BRANCH_NAME == "${development_branch}") {

                        {% for command in dev_build_stage_commands %}sh "{{ command }}"
                        {% endfor %}
                    }
                }
            }
        }
        stage('Deploy) {
            steps {
                script {
                    if (env.BRANCH_NAME == "${production_branch}") {
                        sshagent(["${sshagent_name}"]) {

                            {% for command in prod_deploy_stage_commands %}sh "{{ command }}"
                            {% endfor %}
                        }
                    } else if (env.BRANCH_NAME == "${development_branch}") {

                        {% for command in dev_deploy_stage_commands %}sh "{{ command }}"
                        {% endfor %}
                    }
                }
            }
        }
    }
    post { 
        always { 
            cleanWs()
        }
    }
}"""

nodejs_data = {
    "env": {
        "project_name": None,
        "service_name":  None,
        "dirName": "${project_name}-env.BRANCH_NAME",
        "production_branch":  None,
        "development_branch":  None,
        "system_port":  None,
        "cont_port":  None,
        "sshagent_name":  None,
        "ip_address":  None,
        "image_name": "${project_name}-${service_name}-${env.BRANCH_NAME}",
        "container_name":  "${image_name}-${env.BRANCH_NAME}" + "-cont"
    },
    "build_image": "node:8",
    "build_args": "-v /var/www/html:/var/www/html",
    "prod_build_stage_commands": [
        "zip -r ${dirName}.zip . -x *.git*",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'mkdir /home/ubuntu/${dirName}/ || ls'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && sudo rm -r * || ls'",
        "scp -o StrictHostKeyChecking=no ${dirName}.zip ubuntu@${ip_address}:/home/ubuntu/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'mv /home/ubuntu/${dirName}.zip /home/ubuntu/${dirName}/'",
        "rm -r ${dirName}.zip || ls"
    ],
    "dev_build_stage_commands": [
        "docker build -t ${project_name} ."
    ],
    "prod_deploy_stage_commands": [
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'sudo apt-get update && sudo apt-get install unzip'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && unzip -o ${dirName}.zip'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && sudo rm -r ${dirName}.zip'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${project_name} && sudo docker build -t ${project_name} .'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'sudo docker rm -f ${container_name} || date'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'sudo docker run -d --restart always -m ${memory}M -p ${system_port}:${cont_port} --name ${container_name} ${project_name}:latest'"
    ],
    "dev_deploy_stage_commands": [
        "docker rm -f ${container_name} || ls",
        "docker run -d --restart always -m ${memory}M --name ${container_name} -p ${system_port}:${cont_port} ${project_name}",
        "docker ps | grep ${container_name}"
    ]
}

nodejs_dockerfile_template = """FROM keymetrics/pm2:latest-jessie
WORKDIR /work
COPY package.json .
RUN npm install
COPY .env .env
COPY . .
CMD [ "pm2-runtime", "start", "app.js"]"""

java_data = {
    "env": {
        "project_name": None,
        "service_name":  None,
        "production_branch":  None,
        "development_branch":  None,
        "system_port":  None,
        "cont_port":  None,
        "sshagent_name":  None,
        "ip_address":  None,
        "memory": None,
        "jar_name":  None,
        "image_name": "${project_name}-${service_name}-${env.BRANCH_NAME}",
        "container_name": "${image_name}-${env.BRANCH_NAME}" + "-cont"
    },
    "javaopts": "",
    "build_image": "gradle:5.2.1",
    "build_args": "-v /root/dcompose/${project_name}-${production_branch}:/var/empty-${production_branch} -v /root/dcompose/${project_name}-${development_branch}:/var/empty-${development_branch}",
    "prod_build_stage_commands": [
        "gradle buildNeeded -x test",
        "ls build/libs/",
        "cp build/libs/${jar_name} /var/empty-${production_branch}/",
        "cp Dockerfile /var/empty-${production_branch}/",
        "ls /var/empty-${production_branch}"
    ],
    "dev_build_stage_commands": [
        "gradle buildNeeded -x test",
        "ls build/libs/",
        "cp build/libs/${jar_name} /var/empty-${development_branch}/",
        "cp Dockerfile /var/empty-${development_branch}/"
    ],
    "prod_deploy_stage_commands": [
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo mkdir -p /home/ubuntu/${project_name}/",
        "scp  /root/dcompose/${project_name}-${production_branch}/${jar_name} ubuntu@${ip_address}:/home/ubuntu/",
        "scp  /root/dcompose/${project_name}-${production_branch}/Dockerfile ubuntu@${ip_address}:/home/ubuntu/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo mv /home/ubuntu/${jar_name} /home/ubuntu/${project_name}/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo mv /home/ubuntu/Dockerfile /home/ubuntu/${project_name}/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo docker build --build-arg jar_name=${jar_name} -t ${image_name} /home/ubuntu/${project_name}/.",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo docker rm -f ${container_name} || echo 'no containers to delete'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo docker run --name ${container_name} -d -m ${memory}M --restart always -p ${system_port}:${cont_port} ${image_name}"
    ],
    "dev_deploy_stage_commands": [
        "cd /root/dcompose/${project_name}-${development_branch} && docker build --build-arg jar_name=${jar_name} -t ${image_name} .",
        "docker rm -f ${container_name} || ls",
        "docker run --name ${container_name} -d --restart always -m ${memory}M -p ${system_port}:${cont_port} ${image_name}",
        "docker ps | grep ${container_name}"
    ]
}

java_dockerfile_template = """FROM openjdk:12-oracle
ENV profile development
ADD {{ jar_name }} app.jar
ENV JAVA_OPTS="{{javaopts}}"
EXPOSE 9875
ENTRYPOINT exec java $JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -Dspring.profiles.active=$profile -jar /app.jar"""


react_host_data = {
    "env": {
        "project_name": None,
        "dirName":  "${project_name}-env.BRANCH_NAME",
        "production_branch":  None,
        "development_branch":  None,
        "sshagent_name":  None,
        "ip_address":  None,
    },
    "build_image": "node:8",
    "build_args": "-v /usr/share/nginx/html/${dirName}:/var/empty2 -v /root/dcompose/${dirName}:/var/empty",
    "prod_build_stage_commands": [
        "npm install",
        "npm run build",
        "cp -a build/. /var/empty/"

    ],
    "dev_build_stage_commands": [
        "npm install",
        "npm run build"
    ],
    "prod_deploy_stage_commands": [
        "cd  /root/dcompose/${dirName} && ls" ,
        "apt-get update && apt-get install zip",
        "cd  /root/dcompose/${dirName} && zip -r latest.zip .",
        "scp -o StrictHostKeyChecking=no /root/dcompose/${dirName}/latest.zip ubuntu@${ip_address}:/home/ubuntu/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} ls -la /home/ubuntu",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} sudo unzip  -o /home/ubuntu/latest.zip -d /usr/share/nginx/html/"
    ],
    "dev_deploy_stage_commands": [
        "rm -r /var/empty2/* || ls",
        "cp -a build/. /var/empty2/"
    ]
}

nextjs_data = {
    "env": {
        "project_name": None,
        "service_name":  None,
        "production_branch":  None,
        "development_branch":  None,
        "dirName":  "${project_name}-env.BRANCH_NAME",
        "system_port":  None,
        "cont_port":  None,
        "sshagent_name":  None,
        "ip_address":  None,
        "image_name": "${project_name}-${service_name}-${env.BRANCH_NAME}",
        "container_name": "${image_name}-${env.BRANCH_NAME}" + "-cont"
    },
    "build_image": "node:8",
    "build_args": "-v /root/dcompose/${dirName}:/var/empty2 -v /root/dcompose/${dirName}:/var/empty",
    "prod_build_stage_commands": [
        "npm install",
        "rm -r /var/empty/* || ls"
        "cp -a . /var/empty/"
    ],
    "dev_build_stage_commands": [
        "npm install",
        "rm -r /var/empty2/* || ls"
        "cp -a . /var/empty2/"
    ],
    "prod_deploy_stage_commands": [
        "cd root/dcompose/${dirName} && zip -r ${dirName}.zip .",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && sudo rm -r * || ls'",
        "scp -o StrictHostKeyChecking=no /root/dcompose/${dirName}/${dirName}.zip ubuntu@${ip_address}:/home/ubuntu/",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'mkdir /home/ubuntu/${dirName} || ls'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'mv /home/ubuntu/${dirName}.zip /home/ubuntu/${dirName}/${dirName}.zip || ls'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && unzip -o ${dirName}.zip'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${dirName} && sudo rm -r ${dirName}.zip'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'cd /home/ubuntu/${project_name} && sudo docker build -t ${image_name} .'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'sudo docker rm -f ${container_name} || date'",
        "ssh -o StrictHostKeyChecking=no ubuntu@${ip_address} 'sudo docker run --restart always -d -p ${system_port}:${cont_port} --name ${container_name} ${image_name}:latest'"
    ],
    "dev_deploy_stage_commands": [
        "cd /root/dcompose/${dirName} && docker build -t ${image_name} ."
        "docker rm -f ${container_name} || ls"
        "cd /root/dcompose/${dirName} && docker run --name ${container_name} -p ${system_port}:${cont_port} -d ${image_name}"
    ]
}

nextjs_dockerfile_template = """FROM node:13-alpine
WORKDIR /tmp
COPY . .
RUN npm run build
CMD ["npm","run","start"]"""

jenkinsfile = Template(jenkins_template)
dockerfile = Template(nodejs_dockerfile_template)
print(dockerfile.render())
