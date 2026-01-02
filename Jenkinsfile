pipeline {
    agent any

    environment {
        APP_NAME   = 'devops-demo'
        IMAGE_NAME = 'shimi/devops-demo-app'
        IMAGE_TAG  = 'latest'
        CHART_PATH = 'helm/devops-demo'

        // Adjust if your binaries are elsewhere, but on mac usually these two cover:
        TOOLS_PATH = '/opt/homebrew/bin:/usr/local/bin'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                # Make sure Jenkins sees docker + minikube + kubectl + helm
                export PATH=$TOOLS_PATH:$PATH

                echo "Using docker      at: $(which docker || echo not-found)"
                echo "Using minikube    at: $(which minikube || echo not-found)"

                echo "Switching Docker client to Minikube..."
                eval "$(minikube docker-env)"

                echo "Building Docker image..."
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                export PATH=$TOOLS_PATH:$PATH

                echo "Running placeholder tests..."
                python3 - <<EOF
print("Tests placeholder – in a real project you would run pytest or unit tests here.")
EOF
                '''
            }
        }

        stage('Deploy with Helm') {
            steps {
                sh '''
                export PATH=$TOOLS_PATH:$PATH

                echo "Deploying application with Helm..."
                helm upgrade --install $APP_NAME $CHART_PATH \
                    --set image.repository=$IMAGE_NAME \
                    --set image.tag=$IMAGE_TAG

                echo "Current deployments:"
                kubectl get deploy
                echo "Current services:"
                kubectl get svc
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                export PATH=$TOOLS_PATH:$PATH

                echo "Finding pod for app: $APP_NAME"
                POD=$(kubectl get pods -l app.kubernetes.io/name=$APP_NAME -o jsonpath="{.items[0].metadata.name}")
                echo "Found pod: $POD"

                echo "Starting port-forward on 8082 -> 80"
                kubectl port-forward "$POD" 8082:80 >/tmp/port-forward.log 2>&1 &
                PF_PID=$!
                sleep 5

                echo "Calling /healthz..."
                RESPONSE=$(curl -s http://localhost:8082/healthz || echo '')

                echo "Response: $RESPONSE"

                STATUS=$(printf "%s" "$RESPONSE" | python3 -c "import sys, json; \
import traceback; \
data=sys.stdin.read().strip(); \
print(json.loads(data).get('status', 'missing')) if data else print('missing')" )

                echo "Parsed status: $STATUS"

                # Clean up port-forward
                kill $PF_PID || true

                if [ "$STATUS" != "ok" ]; then
                    echo "Smoke test failed! Expected status=ok"
                    exit 1
                fi

                echo "Smoke test passed."
                '''
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


              
