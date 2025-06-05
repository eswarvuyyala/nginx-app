pipeline {
    agent any

    environment {
        IMAGE_NAME = 'nginx'
        IMAGE_TAG = 'latest'
        AWS_REGION = 'ap-south-1'
        ECR_REPO = '923687682884.dkr.ecr.ap-south-1.amazonaws.com/nginx'
        EKS_CLUSTER = 'mycluster'
        RECIPIENT = 'nageswara@logusims.com'
    }

    stages {
        stage('Notify Build Start') {
            steps {
                mail to: "${RECIPIENT}",
                     subject: "🚀 Jenkins Build Started: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: "The build has started.\n\nJob: ${env.JOB_NAME}\nBuild: #${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
            }
        }

        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/eswarvuyyala/nginx-app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    sh "trivy image --format table --output trivy-report.txt ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        // Optional Email Report Sending - Uncomment when needed
        /*
        stage('Send Trivy Scan Report') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GMAIL_SMTP_CREDENTIALS', usernameVariable: 'GMAIL_USER', passwordVariable: 'GMAIL_APP_PASSWORD')]) {
                    writeFile file: 'send_trivy_report.py', text: '''...'''
                    sh 'python3 send_trivy_report.py'
                }
            }
        }
        */

        stage('Configure AWS CLI') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'AWS_CREDENTIALS', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                        aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                        aws configure set region ${AWS_REGION}
                    """
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}"
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                sh """
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }

        stage('Create Namespace') {
            steps {
                sh """
                    aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER}
                    kubectl get namespace app-nginx || kubectl create namespace nginx-nginx
                """
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh """
                    aws eks --region ${AWS_REGION} update-kubeconfig --name ${EKS_CLUSTER}
                    #kubectl apply -f nginx.deployment.yaml -n app-nginx
					kubectl apply -f nginx-servive.yaml -n app-nginx
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            mail to: "${RECIPIENT}",
                 subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The Jenkins pipeline completed successfully.\n\nDetails: ${env.BUILD_URL}"
        }

        failure {
            echo '❌ Pipeline failed!'
            mail to: "${RECIPIENT}",
                 subject: "❌ FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "The Jenkins pipeline failed.\n\nDetails: ${env.BUILD_URL}"
        }
    }
}
