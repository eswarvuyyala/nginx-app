pipeline {
    agent any

    environment {
        IMAGE_NAME = 'nginx-app'
        IMAGE_TAG = "v1.0.${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/eswarvuyyala/nginx-app.git', branch: 'main'
            }
        }

        stage('Maven Build') {
            steps {
                echo "🔧 Running Maven clean and verify..."
                sh 'mvn clean verify'
            }
        }

        stage('SonarQube Scan') {
            environment {
                SONAR_HOST_URL = 'http://13.201.203.112:9000'
            }
            steps {
                withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                    echo "🔍 Running SonarQube scan..."
                    sh '''
                        mvn sonar:sonar \
                          -Dsonar.projectKey=nginx-app \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo "🔎 Running Trivy scan on Docker image..."
                    sh "trivy image --format table --output trivy-report.txt ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Send Trivy Scan Report') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GMAIL_SMTP_CREDENTIALS', usernameVariable: 'GMAIL_USER', passwordVariable: 'GMAIL_APP_PASSWORD')]) {
                    writeFile file: 'send_trivy_report.py', text: '''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

sender_email = os.environ.get("GMAIL_USER")
receiver_email = os.environ.get("GMAIL_USER")  # send to self
password = os.environ.get("GMAIL_APP_PASSWORD")

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "🛡️ Trivy Report for nginx-app"

body = "Hi,\n\nPlease find the attached Trivy security scan report.\n\nRegards,\nJenkins"
msg.attach(MIMEText(body, 'plain'))

filename = "trivy-report.txt"
with open(filename, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()
'''
                    sh 'python3 send_trivy_report.py'
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up workspace...'
            cleanWs()
        }
    }
}
