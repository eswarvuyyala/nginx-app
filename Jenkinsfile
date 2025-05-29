pipeline {
    agent any

    environment {
        IMAGE_NAME = 'nginx'
        IMAGE_TAG = 'latest'
        AWS_REGION = 'ap-south-1'
        ECR_REPO = '923687682884.dkr.ecr.ap-south-1.amazonaws.com/nginx'
        EKS_CLUSTER = 'mycluster'
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

        // Email stage commented out for now
        // stage('Send Trivy Scan Report') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'GMAIL_SMTP_CREDENTIALS', usernameVariable: 'GMAIL_USER', passwordVariable: 'GMAIL_APP_PASSWORD')]) {
        //             writeFile file: 'send_trivy_report.py', text: ''' ... '''
        //             sh 'python3 send_trivy_report.py'
        //         }
        //     }
        // }

        stage('Configure AWS CLI') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'AWS_CLI', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        echo "Configuring AWS CLI..."
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION

                        echo "Verifying AWS Identity..."
                        aws sts get-caller-identity
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

        stage('Create Namespace') {
            steps {
                sh '''
                    aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER
                    kubectl get namespace app-nginx || kubectl create namespace app-nginx
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                    aws eks --region $AWS_REGION update-kubeconfig --name $EKS_CLUSTER
                    kubectl apply -f nginx.deployment.yaml -n app-nginx
                '''
            }
        }
    }
