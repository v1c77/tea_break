pipeline {
  agent any
  triggers {
          cron('H H(15) * * *')
  }
  stages {
    stage('I wanta tea break') {
      steps {
        sh 'python3 yincha.py'
      }
    }
  }
}