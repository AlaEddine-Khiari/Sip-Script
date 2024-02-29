pipeline {
    agent any

    stages {
        stage('Getting project from Git') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'https://github.com/AlaEddine-Khiari/Sip-Script']]])
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh "pip3 install Flask psycopg2-binary unittest"

                    // For script.py unit test
                    sh "python3 -m unittest Test/test_script.py"

                    // For app.py unit test
                    sh "python3 -m unittest Test/test_app.py"
                }
            }
        }
      
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t alaeddinekh/sip-add:latest ."
                }
            }
        }

        stage('Push Image To Dockerhub') {
            steps {
                script {
                    sh 'docker login -u alaeddinekh --password dckr_pat_EkLSF6l04M02rFWSzu3WjP_QL48'
                    sh 'docker push alaeddinekh/sip-add:latest'
                }
            }
        }
        
        stage('Cleanup Up') {
            steps {
                cleanWs()  
            }
        }
    }

    post {
        success {
            mail to: 'khiarialaa@gmail.com',
                 from: 'zizoutejdin02@gmail.com',
                 subject: 'Build Finished - Success',
                 body: '''Dear Mr Ala, 
                         We are happy to inform you that your pipeline build was successful. 
                         Great work! 
                                         
                         Best regards,
                         -Jenkins Team-'''
        }
        
        failure {
            mail to: 'khiarialaa@gmail.com',
                 from: 'zizoutejdin02@gmail.com',
                 subject: 'Build Finished - Failure',
                 body: '''Dear Mr Ala, 
                         We are sorry to inform you that your pipeline build failed. 
                         Keep working! 

                         Best regards,
                         -Jenkins Team-'''
        }
    }
}
