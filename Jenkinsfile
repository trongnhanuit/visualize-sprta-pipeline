//  a JenkinsFile to build iqtree
// paramters
//  1. git branch
// 2. git url


properties([
    parameters([
    	booleanParam(defaultValue: false, description: 'Re-build CMAPLE?', name: 'BUILD_CMAPLE'),
        string(name: 'CMAPLE_BRANCH', defaultValue: 'main', description: 'Branch to build CMAPLE'),
        booleanParam(defaultValue: false, description: 'Download testing data?', name: 'DOWNLOAD_DATA'),
        booleanParam(defaultValue: false, description: 'Infer ML trees?', name: 'INFER_TREE'),
        booleanParam(defaultValue: false, description: 'Compute SPRTA by CMAPLE?', name: 'COMPUTE_SPRTA_CMAPLE'),
        booleanParam(defaultValue: false, description: 'Compute SPRTA by MAPLE?', name: 'COMPUTE_SPRTA_MAPLE'),
    ])
])
pipeline {
    agent any
    environment {
        NCI_ALIAS = "gadi"
        WORKING_DIR = "/scratch/dx61/tl8625/cmaple/ci-cd"
        DATA_DIR = "${WORKING_DIR}/data"
        TREE_DIR = "${DATA_DIR}/tree"
        OUT_DIR = "${DATA_DIR}/output"
        SCRIPTS_DIR = "${WORKING_DIR}/scripts"
        MAPLE_SPRTA_TREE_PREFIX = "SPRTA_MAPLE_tree_"
        PYTHON_SCRIPT_PATH = "${SCRIPTS_DIR}/extract_visualize_results.py"
    }
    stages {
    	stage("Build CMAPLE") {
            steps {
                script {
                	if (params.BUILD_CMAPLE) {
                        echo 'Building CMAPLE'
                        // trigger jenkins cmaple-build
                        build job: 'cmaple-build', parameters: [string(name: 'BRANCH', value: CMAPLE_BRANCH)]

                    }
                    else {
                        echo 'Skip building CMAPLE'
                    }
                }
            }
        }
        stage("Download testing data & Infer ML trees") {
            steps {
                script {
                	if (params.DOWNLOAD_DATA || params.INFER_TREE) {
                        // trigger jenkins cmaple-tree-inference
                        build job: 'cmaple-tree-inference', parameters: [booleanParam(name: 'DOWNLOAD_DATA', value: DOWNLOAD_DATA),
                        booleanParam(name: 'INFER_TREE', value: INFER_TREE),
                        ]
                    }
                    else {
                        echo 'Skip inferring ML trees'
                    }
                }
            }
        }
        stage('Compute SPRTA by CMAPLE') {
            steps {
                script {
                	if (params.COMPUTE_SPRTA_CMAPLE) {
                        echo 'Compute SPRTA by CMAPLE'
                        // trigger jenkins cmaple-build
                        build job: 'cmaple-compute-sprta', parameters: []

                    }
                    else {
                        echo 'Skip computing SPRTA by CMAPLE'
                    }
                }
            }
        }
        stage('Compute SPRTA by MAPLE') {
            steps {
                script {
                	if (params.COMPUTE_SPRTA_MAPLE) {
                        echo 'Compute SPRTA by MAPLE'
                        // trigger jenkins maple-compute-sprta
                        build job: 'maple-compute-sprta', parameters: []

                    }
                    else {
                        echo 'Skip computing SPRTA by MAPLE'
                    }
                }
            }
        }
        stage('Visualize SPRTA scores computed by CMAPLE vs MAPLE') {
            steps {
                script {
                	sh """
                        ssh ${NCI_ALIAS} << EOF
                        mkdir -p ${SCRIPTS_DIR}
                        exit
                        EOF
                        """
                	sh "scp -r scripts/* ${NCI_ALIAS}:${SCRIPTS_DIR}"
                    sh """
                        ssh ${NCI_ALIAS} << EOF
                                              
                        sh ${SCRIPTS_DIR}/extract_visualize_results.sh ${PYTHON_SCRIPT_PATH} ${TREE_DIR} ${OUT_DIR} ${MAPLE_SPRTA_TREE_PREFIX} 
                        
                        exit
                        EOF
                        """
                }
            }
        }
        stage ('Verify') {
            steps {
                script {
                	sh """
                        ssh ${NCI_ALIAS} << EOF
                        cd  ${WORKING_DIR}
                        echo "Files in ${WORKING_DIR}"
                        ls -ila ${WORKING_DIR}
                        echo "Files in ${TREE_DIR}"
                        ls -ila ${TREE_DIR}
                        echo "Files in ${OUT_DIR}"
                        ls -ila ${OUT_DIR}
                        exit
                        EOF
                        """
                }
            }
        }


    }
    post {
        always {
            echo 'Cleaning up workspace'
            cleanWs()
        }
    }
}

def void cleanWs() {
    // ssh to NCI_ALIAS and remove the working directory
    // sh "ssh ${NCI_ALIAS} 'rm -rf ${REPO_DIR} ${BUILD_SCRIPTS}'"
}