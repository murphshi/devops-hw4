pipeline {
  agent any

  stages {
    stage('Info') {
      steps {
        echo "Branch: ${env.BRANCH_NAME}"
        sh 'uname -a'
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
