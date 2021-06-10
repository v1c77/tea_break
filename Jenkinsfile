pipeline {
  agent any
  triggers {
          cron('H/7 * * * *')
  }
  stages {
    stage('I wanta tea break') {
      steps {
        sh 'source  ~/.bashrc &&  source ~/.bash_profile  &&  pyenv local 3.9.5 &&  python --version && python yincha.py'
      }
    }
  }
}
