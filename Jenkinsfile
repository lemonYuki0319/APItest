pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Pipeline script from SCM 会自动 checkout，这里保留也无妨
                checkout scm
            }
        }

        stage('Run API Tests') {
            steps {
                // Windows 节点用 bat；确保 reports 目录存在并输出 junit 报告
                bat 'if not exist reports mkdir reports && pytest tests\\single\\test_login.py -s --junitxml=reports\\results.xml'
            }
        }
    }

    post {
        always {
            junit 'reports/results.xml'
        }
    }
}
