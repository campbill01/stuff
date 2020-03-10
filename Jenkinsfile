pipeline {
  agent any
  stages {
    stage('Buzz Buzz') {
      parallel {
        stage('Buzz Buzz') {
          steps {
            echo 'Bees Buzz!'
          }
        }

        stage('Parallel') {
          steps {
            echo 'I\'m running!'
          }
        }

      }
    }

  }
}