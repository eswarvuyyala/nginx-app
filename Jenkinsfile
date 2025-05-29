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

        // Commented out for now
        /*
        stage('Send Trivy Scan Report') {
            steps {
                script {
                    def scriptContent = '''\
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

gmail_user = 'vuyyala6@gmail.com'
gmail_app_password = 'gpxekuxbssuqwope'
to = 'nageswara@logusims.com'
subject = 'Trivy Scan Report'
body = 'Please find the attached Trivy scan report.'

msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

filename = 'trivy-report.txt'
with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(gmail_user, gmail_app_password)
    server.sendmail(gmail_user, to, msg.as_string())

print('Email sent!')
'''
                    writeFile file: 'send_trivy_report.py', text: scriptContent
                    sh 'python3 send_trivy_report.py'
                }
            }
        }
        */

        stage('Configure AWS CLI') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'AWS_CLI', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region $AWS_REGION
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
