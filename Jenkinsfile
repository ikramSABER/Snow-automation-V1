pipeline {
    agent any

    environment {
        ROBOT_RESULTS_DIR = "${WORKSPACE}/robot_results"
        VENV_DIR = "${WORKSPACE}/.venv"
        PYTHON_BIN = "${WORKSPACE}/.venv/Scripts/python.exe"
        PIP_BIN = "${WORKSPACE}/.venv/Scripts/pip.exe"
        ROBOT_BIN = "${WORKSPACE}/.venv/Scripts/robot.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Riad', url: 'https://github.com/ElMouddenRiad/ProjetAlten.git'
            }
        }

        stage('Setup VirtualEnv') {
            steps {
                bat "python -m venv ${VENV_DIR}"
                bat "${PYTHON_BIN} -m pip install --upgrade pip"
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "${PIP_BIN} install -r ${WORKSPACE}/requirements.txt"
                bat "${PIP_BIN} install robotframework-requests robotframework-jsonlibrary"
            }
        }

        stage('Debug: Check Installed Packages') {
            steps {
                bat "${PIP_BIN} list"
            }
        }

        stage('Run Robot Tests - ServiceNow') {
            steps {
                bat "if not exist \"${ROBOT_RESULTS_DIR}\" mkdir \"${ROBOT_RESULTS_DIR}\""
                bat "${ROBOT_BIN} -d ${ROBOT_RESULTS_DIR} ${WORKSPACE}/tests/test_Demande_Mainteneur.robot"
            }
        }

        stage('Convert Robot Results to JUnit Format') {
            steps {
                bat "${PYTHON_BIN} -m robot.rebot -d \"${ROBOT_RESULTS_DIR}\" --xunit \"${ROBOT_RESULTS_DIR}\\xunit_result.xml\" \"${ROBOT_RESULTS_DIR}\\output.xml\""
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'robot_results/xunit_result.xml'
            }
        }
    }
}