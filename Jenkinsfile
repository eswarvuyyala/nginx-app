pipeline {
    agent any

    environment {
        RECIPIENT = 'nageswara@logusims.com'
        IMAGE_NAME = 'nginx-app'
        IMAGE_TAG = 'V1.0.0'
    }

    stages {
        stage('Notify Build Start') {
            steps {
                mail to: "${RECIPIENT}",
                     subject: "🚀 Jenkins Build Started: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: """The build has started.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
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
                    echo "🔧 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo "🔍 Running Trivy scan..."
                    sh "trivy image --format table --output trivy-report.txt ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Notify Build Success') {
            steps {
                mail to: "${RECIPIENT}",
                     subject: "✅ Jenkins Build Succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: """The build completed successfully.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
            }
        }

        // Optional stage to send Trivy scan report via custom script
        
        stage('Send Trivy Scan Report') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'GMAIL_SMTP_CREDENTIALS', usernameVariable: 'GMAIL_USER', passwordVariable: 'GMAIL_APP_PASSWORD')]) {
                    writeFile file: 'send_trivy_report.py', text: '''...'''
                    sh 'python3 send_trivy_report.py'
                }
            }
        }
        */
    }

    post {
        failure {
            mail to: "${RECIPIENT}",
                 subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """The build has failed.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
URL: ${env.BUILD_URL}
"""
        }
    }
}
