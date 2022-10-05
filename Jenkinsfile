pipeline {
    agent any
    parameters {
        choice(name: 'ENV', choices: ['prod'], description: 'Prod env')
    }
    environment {
        ENV="${params.ENV}"
        PACKER_LOG="${env.WORKSPACE}/terraform-common-infra/packer.log"
        ssh_key_path="/var/lib/jenkins/.ssh/toptal"
    }
    stages {
        stage('Infra clone') {
            steps {
                dir('terraform-common-infra') {
                    deleteDir()
                    git credentialsId: 'infra360-pem', poll: false, url: 'git@github.com:infra360io/terraform-common-infra.git', branch: "master"
                }
            }
        }
        stage('Build Packer') {
            steps {
                ansiColor('xterm') {
                    script {
                        sh 'export ssh_key_path=${ssh_key_path}'
                        sh 'packer build terraform-common-infra/packer/backend.json | tee "${PACKER_LOG}"  || { echo "packer build step failed" ; exit 1; }'
                        sh './terraform-common-infra/init/copy_ami_id.sh realworld-be-app'
                    }
                }
            }
        }
        stage('Terraform Apply & Deployment') {
            steps {
                ansiColor('xterm') {
                    script {
                        IMAGE_ID = readFile(file: './image_id.txt')
                        echo "${IMAGE_ID}"
                    }
                    dir("${env.WORKSPACE}/terraform-common-infra") {
                        echo "${IMAGE_ID}"
                        sh "terraform init -reconfigure"
                        sh "terraform apply -auto-approve -target=module.backend -var instance_refresh_backend=\"[1]\" -var image_id_backend=${IMAGE_ID}"
                    }
                }
            }
        }
        stage('API Regression') {
            steps {
                ansiColor('xterm') {
                    dir("${env.WORKSPACE}/terraform-common-infra/api-regression") {
                        sh "chmod 755 ./run-api-tests.sh && ./run-api-tests.sh"
                    }
                }
            }
        }        
    }
}
