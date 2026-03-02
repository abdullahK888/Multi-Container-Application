pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('File Scan') {
            steps {
                sh 'trivy fs . --exit-code 0 --severity HIGH,CRITICAL'
            }
        }
        
        stage('Build Image') {
            steps {
                sh 'docker build -t multi-container-app:${BUILD_NUMBER} ./backend_project'
            }
        }
        
        stage('Image Scan') {
            steps {
                sh 'trivy image multi-container-app:${BUILD_NUMBER} --exit-code 0'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker compose up -d --build'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
