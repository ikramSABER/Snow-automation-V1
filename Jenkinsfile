pipeline {
    agent any

    environment {
        ROBOT_RESULTS_DIR = "${WORKSPACE}/robot_results"
        VENV_DIR = "${WORKSPACE}/.venv"
        PYTHON_BIN = "${VENV_DIR}/bin/python"
        PIP_BIN = "${VENV_DIR}/bin/pip"
        ROBOT_BIN = "${VENV_DIR}/bin/robot"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Riad', url: 'https://github.com/ElMouddenRiad/ProjetAlten.git'
            }
        }

        stage('Setup VirtualEnv') {
            steps {
                sh "python3 -m venv ${VENV_DIR}"
                sh "${PYTHON_BIN} -m pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "${PIP_BIN} install -r requirements.txt"
                sh "${PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
            }
        }

        stage('Debug: Check Installed Packages') {
            steps {
                sh "${PIP_BIN} list"
            }
        }

        stage('Cleanup Old Browsers') {
            steps {
                sh 'pkill -f chrome || true'
                sh 'pkill -f chromedriver || true'
            }
        }

        stage('Run Robot Tests - ServiceNow') {
            steps {
                sh "mkdir -p ${ROBOT_RESULTS_DIR}"
                sh "${ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}/tests/test_servicenowSAV.robot"
            }
        }

        stage('Convert Robot Results to JUnit Format') {
            steps {
                sh "${PYTHON_BIN} -m robot.rebot -d ${ROBOT_RESULTS_DIR} --xunit ${ROBOT_RESULTS_DIR}/xunit_result.xml ${ROBOT_RESULTS_DIR}/output.xml"
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'robot_results/xunit_result.xml'
            }
        }
    }
}
