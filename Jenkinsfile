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
                sh 'docker tag multi-container-app:${BUILD_NUMBER} multi-container-app:latest'
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
                        -Dsonar.login=sqp_7daddd0975ca38f54c689d91591bdc64de68023c \
                        -Dsonar.python.version=3
                    '''
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/configmap.yaml'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/multi-container-app'
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