pipeline {
  agent {
    dockerfile true
  }

  stages {
    stage('Build') {
      steps {
        echo 'Building...'
      }
    }

    stage('Test') {
      steps {
        echo 'Testing...'
        sh 'bash ./test'
      }
    }

    stage('Deploy') {
      when { branch 'master' }
      steps {
        echo 'Deploying...'
      }
    }

  }
}
