pipeline {
  agent any

  environment {
    // Simple versioning: build number
    VERSION = "0.1.${env.BUILD_NUMBER}"
  }

  stages {
    stage('Info') {
      steps {
        echo "Branch: ${env.BRANCH_NAME}"
        echo "Version: ${env.VERSION}"
        sh 'uname -a'
      }
    }

    stage('Build & Package') {
      steps {
        sh '''
          set -eux

          rm -rf dist
          mkdir -p dist

          # Write version file
          echo "${VERSION}" > dist/VERSION.txt

          # Package repo content into a zip artifact (exclude .git and dist itself)
          zip -r "dist/app-${VERSION}.zip" . -x ".git/*" -x "dist/*"
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
}
