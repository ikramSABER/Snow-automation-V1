pipeline {
    agent any

    environment {
        ROBOT_RESULTS_DIR = "${WORKSPACE}/robot_results"
        VENV_DIR = "${WORKSPACE}/.venv"
        PYTHON_BIN = isUnix() ? "${WORKSPACE}/.venv/bin/python3" : "${WORKSPACE}/.venv/Scripts/python.exe"
        PIP_BIN    = isUnix() ? "${WORKSPACE}/.venv/bin/pip3"    : "${WORKSPACE}/.venv/Scripts/pip.exe"
        ROBOT_BIN  = isUnix() ? "${WORKSPACE}/.venv/bin/robot"   : "${WORKSPACE}/.venv/Scripts/robot.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Riad', url: 'https://github.com/ElMouddenRiad/ProjetAlten.git'
            }
        }

        stage('Setup VirtualEnv') {
            steps {
                script {
                    if (isUnix()) {
                        sh "python3 -m venv ${VENV_DIR}"
                        sh "${PYTHON_BIN} -m pip install --upgrade pip"
                    } else {
                        bat "python -m venv ${VENV_DIR}"
                        bat "${PYTHON_BIN} -m pip install --upgrade pip"
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${PIP_BIN} install -r ${WORKSPACE}/requirements.txt"
                        sh "${PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
                    } else {
                        bat "${PIP_BIN} install -r ${WORKSPACE}/requirements.txt"
                        bat "${PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
                    }
                }
            }
        }

        stage('Debug: Check Installed Packages') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${PIP_BIN} list"
                    } else {
                        bat "${PIP_BIN} list"
                    }
                }
            }
        }

        stage('Run Robot Tests - ServiceNow') {
            steps {
                script {
                    if (isUnix()) {
                        sh "mkdir -p ${ROBOT_RESULTS_DIR}"
                        sh "${ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}/tests/test_servicenowSAV.robot"
                    } else {
                        bat "if not exist \"${ROBOT_RESULTS_DIR}\" mkdir \"${ROBOT_RESULTS_DIR}\""
                        bat "${ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}/tests/test_servicenowSAV.robot"
                    }
                }
            }
        }

        stage('Convert Robot Results to JUnit Format') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${PYTHON_BIN} -m robot.rebot -d \"${ROBOT_RESULTS_DIR}\" --xunit \"${ROBOT_RESULTS_DIR}/xunit_result.xml\" \"${ROBOT_RESULTS_DIR}/output.xml\""
                    } else {
                        bat "${PYTHON_BIN} -m robot.rebot -d \"${ROBOT_RESULTS_DIR}\" --xunit \"${ROBOT_RESULTS_DIR}\\xunit_result.xml\" \"${ROBOT_RESULTS_DIR}\\output.xml\""
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'robot_results/xunit_result.xml'
            }
        }
    }
}
