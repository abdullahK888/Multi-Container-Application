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
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=Multi-container-app \
                        -Dsonar.sources=./backend_project \
                        -Dsonar.host.url=http://172.17.0.3:9000 \
                        -Dsonar.login=sqp_7daddd0975ca38f54c689d91591bdc64de68023c
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d --build'
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