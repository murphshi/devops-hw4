pipeline {
  agent any

  environment {
    VERSION = "0.1.${env.BUILD_NUMBER}"

    SONARQUBE_SERVER_NAME = 'SonarQube'
    SONAR_TOKEN_CRED_ID   = 'sonar-token'
    SONAR_PROJECT_KEY     = 'devops-hw4'
    SONAR_PROJECT_NAME    = 'devops-hw4'
  }

  stages {

    stage('Info') {
      steps {
        echo "Branch: ${env.BRANCH_NAME}"
        echo "Version: ${env.VERSION}"
        sh 'uname -a'
      }
    }

    stage('Check Docker') {
      steps {
        sh '''
          set -eux
          docker version
        '''
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv("${env.SONARQUBE_SERVER_NAME}") {
          withCredentials([string(credentialsId: "${env.SONAR_TOKEN_CRED_ID}", variable: 'SONAR_TOKEN')]) {
            sh '''
              set -eux
              docker run --rm \
                -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                -e SONAR_LOGIN="$SONAR_TOKEN" \
                -v "$PWD:/usr/src" \
                sonarsource/sonar-scanner-cli:latest \
                -Dsonar.projectKey="$SONAR_PROJECT_KEY" \
                -Dsonar.projectName="$SONAR_PROJECT_NAME" \
                -Dsonar.projectVersion="$VERSION" \
                -Dsonar.sources=. \
                -Dsonar.exclusions=dist/**,.git/**,**/*.tar.gz
            '''
          }
        }
      }
    }

    stage('Quality Gate') {
      steps {
        timeout(time: 5, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Build & Package') {
      steps {
        sh '''
          set -eux
          rm -rf dist
          mkdir -p dist
          tar -czf "dist/app-${VERSION}.tar.gz" --exclude=.git --exclude=dist .
          ls -lah dist
        '''
      }
    }

    stage('Archive Artifacts') {
      steps {
        archiveArtifacts artifacts: 'dist/*', fingerprint: true
      }
    }

    stage('Main-only') {
      when { branch 'main' }
      steps {
        echo 'Running main-only stage'
      }
    }

    stage('Non-main (feature)') {
      when { not { branch 'main' } }
      steps {
        echo 'Running non-main stage'
      }
    }
  }

  post {
    always {
      echo "Pipeline finished on branch: ${env.BRANCH_NAME}"
    }
  }
}
