pipeline {
    agent any

    environment {
        ROBOT_RESULTS_DIR = "${WORKSPACE}/robot_results"
        VENV_DIR = "${WORKSPACE}/.venv"
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
                        env.PYTHON_BIN = "${VENV_DIR}/bin/python3"
                        env.PIP_BIN    = "${VENV_DIR}/bin/pip3"
                        env.ROBOT_BIN  = "${VENV_DIR}/bin/robot"
                        sh "${env.PYTHON_BIN} -m pip install --upgrade pip"
                    } else {
                        bat "python -m venv ${VENV_DIR}"
                        env.PYTHON_BIN = "${VENV_DIR}\\Scripts\\python.exe"
                        env.PIP_BIN    = "${VENV_DIR}\\Scripts\\pip.exe"
                        env.ROBOT_BIN  = "${VENV_DIR}\\Scripts\\robot.exe"
                        bat "${env.PYTHON_BIN} -m pip install --upgrade pip"
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${env.PIP_BIN} install -r ${WORKSPACE}/requirements.txt"
                        sh "${env.PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
                    } else {
                        bat "${env.PIP_BIN} install -r ${WORKSPACE}\\requirements.txt"
                        bat "${env.PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
                    }
                }
            }
        }

        stage('Debug: Check Installed Packages') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${env.PIP_BIN} list"
                    } else {
                        bat "${env.PIP_BIN} list"
                    }
                }
            }
        }

        stage('Run Robot Tests - ServiceNow') {
            steps {
                script {
                    if (isUnix()) {
                        sh "mkdir -p ${ROBOT_RESULTS_DIR}"
                        sh "${env.ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}/tests/test_servicenowSAV.robot"
                    } else {
                        bat "if not exist \"${ROBOT_RESULTS_DIR}\" mkdir \"${ROBOT_RESULTS_DIR}\""
                        bat "${env.ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}\\tests\\test_servicenowSAV.robot"
                    }
                }
            }
        }

        stage('Convert Robot Results to JUnit Format') {
            steps {
                script {
                    if (isUnix()) {
                        sh "${env.PYTHON_BIN} -m robot.rebot -d \"${ROBOT_RESULTS_DIR}\" --xunit \"${ROBOT_RESULTS_DIR}/xunit_result.xml\" \"${ROBOT_RESULTS_DIR}/output.xml\""
                    } else {
                        bat "${env.PYTHON_BIN} -m robot.rebot -d \"${ROBOT_RESULTS_DIR}\" --xunit \"${ROBOT_RESULTS_DIR}\\xunit_result.xml\" \"${ROBOT_RESULTS_DIR}\\output.xml\""
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
