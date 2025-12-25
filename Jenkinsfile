pipeline {
    agent any
    
    environment {
        // Tên image và container
        IMAGE_NAME = 'flask-demo'
        CONTAINER_NAME = 'flask-app'
        APP_PORT = '5000'
        // Tạo tag với timestamp để track versions
        IMAGE_TAG = "${env.BUILD_NUMBER}-${new Date().format('yyyyMMdd-HHmmss')}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    // Build image với tag mới
                    sh """
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Stop Old Container') {
            steps {
                script {
                    echo 'Stopping and removing old container if exists...'
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo "Deploying new container: ${CONTAINER_NAME}"
                    sh """
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p ${APP_PORT}:5000 \
                            -e APP_VERSION=${IMAGE_TAG} \
                            --restart unless-stopped \
                            ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo 'Verifying deployment...'
                    // Đợi container khởi động
                    sleep(time: 5, unit: 'SECONDS')
                    
                    // Health check
                    sh """
                        curl -f http://localhost:${APP_PORT}/health || exit 1
                    """
                    
                    echo 'Deployment successful! ✓'
                }
            }
        }
        
        stage('Cleanup Old Images') {
            steps {
                script {
                    echo 'Cleaning up old Docker images...'
                    // Giữ lại 3 images gần nhất, xóa các images cũ
                    sh """
                        docker images ${IMAGE_NAME} --format '{{.Tag}}' | grep -v latest | tail -n +4 | xargs -r -I {} docker rmi ${IMAGE_NAME}:{} || true
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo '✓ Pipeline completed successfully!'
            echo "Application is running at: http://localhost:${APP_PORT}"
            echo "Version: ${IMAGE_TAG}"
        }
        failure {
            echo '✗ Pipeline failed!'
            // Rollback nếu cần
            sh """
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
            """
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
