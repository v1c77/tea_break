pipeline {
  agent any
  triggers {
          cron('H 15 * * *')
  }
  stages {
    stage('I wanta tea break') {
      steps {
        sh 'pyenv local 3.9.5 & python --version && python yincha.py'
      }
    }
  }
}
