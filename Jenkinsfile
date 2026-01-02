pipeline {
    agent any

    environment {
        APP_NAME = "devops-demo"
        IMAGE_NAME = "shimi/devops-demo-app"
        IMAGE_TAG = "latest"
        CHART_PATH = "helm/devops-demo"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Minikube Docker Env') {
            steps {
                sh 'echo "Switching Docker client to Minikube..."'
                sh 'eval $(minikube docker-env)'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Building Docker image..."
                eval $(minikube docker-env)
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                echo "Running basic tests..."
                python3 - <<EOF
import requests
print("No real tests implemented, but placeholder exists.")
EOF
                '''
            }
        }

        stage('Deploy with Helm') {
            steps {
                sh '''
                echo "Deploying application with Helm..."
                helm upgrade --install ${APP_NAME} ${CHART_PATH} \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${IMAGE_TAG}
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                echo "Running smoke test via port-forward..."
                POD=$(kubectl get pods -l app.kubernetes.io/name=${APP_NAME} -o jsonpath="{.items[0].metadata.name}")
                kubectl port-forward $POD 8082:80 &

                # Sleep to give port-forward time to bind
                sleep 5

                STATUS=$(curl -s http://localhost:8082/healthz | jq -r .status)

                echo "Health check response: $STATUS"

                if [ "$STATUS" != "ok" ]; then
                    echo "Smoke test failed!"
                    exit 1
                fi

                echo "Smoke test passed."
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}

