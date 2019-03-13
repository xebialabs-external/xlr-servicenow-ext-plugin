#!groovy
@Library('jenkins-pipeline-libs@master')

import groovy.transform.Field

@Field def slackRoom = '#team-integration-jobs'

pipeline {
    agent none

    environment {
        GRADLE_OPTS = '-XX:MaxPermSize=256m -Xmx1024m  -Djsse.enableSNIExtension=false'
        SELENIUM_TEST_ADDR = 'http://selenium-3-hub:4444/wd/hub'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        skipDefaultCheckout()
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('End-To-End Tests') {
            parallel {
                stage('Linux Chrome') {
                    agent {
                        label 'linux || xlp'
                    }

                    environment {
                        SELENIUM_TEST_BROWSER = 'firefox'
                        SELENIUM_TEST_PLATFORM = 'linux'
                        XL_RELEASE_LICENSE = credentials('xl-release-license')
                        XL_RELEASE_PORT = allocatePort()
                        HTTP_SERVER_PORT = allocatePort()
                    }

                    tools {
                        jdk 'JDK 8u60'
                    }

                    steps {
                        checkout scm
                        throttle(["selenium-grid-${env.SELENIUM_TEST_PLATFORM}-${env.SELENIUM_TEST_BROWSER}"]) {
                            sh "./gradlew clean build testEnd2End -PxlReleaseLicense=${env.XL_RELEASE_LICENSE} -PxlReleasePort=${env.XL_RELEASE_PORT} -PhttpServerPort=${HTTP_SERVER_PORT}"
                        }
                    }
                }
                stage('Linux Firefox') {
                    agent {
                        label 'linux || xlp'
                    }

                    environment {
                        SELENIUM_TEST_BROWSER = 'chrome'
                        SELENIUM_TEST_PLATFORM = 'linux'
                        XL_RELEASE_LICENSE = credentials('xl-release-license')
                        XL_RELEASE_PORT = allocatePort()
                        HTTP_SERVER_PORT = allocatePort()
                    }

                    tools {
                        jdk 'JDK 8u60'
                    }

                    steps {
                        checkout scm
                        throttle(["selenium-grid-${env.SELENIUM_TEST_PLATFORM}-${env.SELENIUM_TEST_BROWSER}"]) {
                            sh "./gradlew clean build testEnd2End -PxlReleaseLicense=${env.XL_RELEASE_LICENSE} -PxlReleasePort=${env.XL_RELEASE_PORT} -PhttpServerPort=${HTTP_SERVER_PORT}"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend (color: "good", message: "End-To-End Testing finished : xlr-servicenow-plugin (<${env.BUILD_URL}|${env.JOB_NAME} [${env.BUILD_NUMBER}]>)",
                    channel: slackRoom, tokenCredentialId: "slack-token")
        }
        failure {
            slackSend (color: "danger", message: "End-To-End Testing failed : xlr-servicenow-plugin (<${env.BUILD_URL}|${env.JOB_NAME} [${env.BUILD_NUMBER}]>)",
                    channel: slackRoom, tokenCredentialId: "slack-token")
        }
    }
}
