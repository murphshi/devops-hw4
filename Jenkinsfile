pipeline {
  agent any

  environment {
    VERSION = "0.1.${env.BUILD_NUMBER}"

    SONARQUBE_SERVER_NAME = 'SonarQube'
    SONAR_PROJECT_KEY     = 'devops-hw4'
    SONAR_PROJECT_NAME    = 'devops-hw4'
    SONAR_SCANNER_TOOL    = 'sonar-scanner'

    NOTIFY_EMAIL = 'murphshi0130@gmail.com'
  }

  stages {
    stage('Info') {
      steps {
        echo "Branch: ${env.BRANCH_NAME}"
        echo "Version: ${env.VERSION}"
        sh 'uname -a'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          def scannerHome = tool(env.SONAR_SCANNER_TOOL)

          withSonarQubeEnv(env.SONARQUBE_SERVER_NAME) {
            sh """
              set -eux
              "${scannerHome}/bin/sonar-scanner" \\
                -Dsonar.projectKey="${SONAR_PROJECT_KEY}" \\
                -Dsonar.projectName="${SONAR_PROJECT_NAME}" \\
                -Dsonar.projectVersion="${VERSION}" \\
                -Dsonar.sources=. \\
                -Dsonar.exclusions=dist/**,.git/**,**/*.tar.gz,**/*.zip,**/__pycache__/**,**/.venv/**,**/venv/**,perf/**,**/*.js
            """
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

          tar -czf "dist/app-${VERSION}.tar.gz" \
            --exclude=.git \
            --exclude=dist \
            .
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
    success {
      script {
        def subject = "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} (${env.BRANCH_NAME}) deployed"
        def body = """\
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Branch: ${env.BRANCH_NAME}
Version: ${env.VERSION}

Build URL: ${env.BUILD_URL}
Console URL: ${env.BUILD_URL}console
Artifacts: ${env.BUILD_URL}artifact/
"""

        emailext(
          to: env.NOTIFY_EMAIL,
          subject: subject,
          body: body,
          mimeType: 'text/plain'
        )
      }
    }

    failure {
      script {
        def subject = "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER} (${env.BRANCH_NAME})"
        def body = """\
Pipeline FAILED.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Branch: ${env.BRANCH_NAME}
Version: ${env.VERSION}

Build URL: ${env.BUILD_URL}
Console URL: ${env.BUILD_URL}console

Tip: Open the Console URL to see the exact error.
"""

        emailext(
          to: env.NOTIFY_EMAIL,
          subject: subject,
          body: body,
          mimeType: 'text/plain'
        )
      }
    }

    always {
      echo "Pipeline finished on branch: ${env.BRANCH_NAME}"
    }
  }
}
