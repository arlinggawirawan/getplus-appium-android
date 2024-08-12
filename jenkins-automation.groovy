//On the mac, command must full path :). Or it will error command not found
pipeline {
    agent any

    environment {
        ANDROID_HOME = '/Users/ibrahim/Library/Android/sdk'  // Set the path Android SDK
    }

    stages {
        stage('Checkout the Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/jenkins-fix']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    submoduleCfg: [],
                    userRemoteConfigs: [[credentialsId: 'jenkins-secret-bitbucket', url: 'https://ibrahimgpi@bitbucket.org/gpitech-getplus/android-app-automation.git']]
                ])
            }
        }

        stage('Run the Test Login Automation') {
            steps {
                script {
                    // Run your Appium test script 
                    sh '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 GetPlus_login_rebuild.py'
                }
            }
        }
        stage('Run the Test Register Automation') {
            steps {
                script {
                    // Run your Appium test script 
                    sh '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 GetPlus_register_rebuild.py'
                }
            }
        }
    }
}