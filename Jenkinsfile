pipeline {
    agent any

    environment {
        IMAGE_NAME = 'nginx'
        IMAGE_TAG = 'latest'
        AWS_REGION = 'ap-south-1'
        ECR_REPO = '923687682884.dkr.ecr.ap-south-1.amazonaws.com/nginx'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/eswarvuyyala/nginx-app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'trivy image --format table --output trivy-report.txt $IMAGE_NAME:$IMAGE_TAG'
            }
        }

        stage('Send Trivy Scan Report') {
            steps {
                script {
                    writeFile file: 'send_trivy_report.py', text: '''(your script here)'''
                    sh 'python3 send_trivy_report.py'
                }
            }
        }

        stage('Configure AWS CLI') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'AWS_CLI', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        mkdir -p $HOME/.aws
                        echo "[default]" > $HOME/.aws/credentials
                        echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> $HOME/.aws/credentials
                        echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> $HOME/.aws/credentials
                    '''
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO'
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                sh '''
                    docker tag $IMAGE_NAME:$IMAGE_TAG $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                    aws eks --region $AWS_REGION update-kubeconfig --name mycluster
                    kubectl apply -f nginx.deployment.yaml
                '''
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
