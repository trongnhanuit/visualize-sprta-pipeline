//  a JenkinsFile to build iqtree
// paramters
//  1. git branch
// 2. git url


properties([
    parameters([
    	booleanParam(defaultValue: true, description: 'Re-build CMAPLE?', name: 'BUILD_CMAPLE'),
        string(name: 'CMAPLE_BRANCH', defaultValue: 'sprta', description: 'Branch to build CMAPLE'),
        booleanParam(defaultValue: false, description: 'Download testing data?', name: 'DOWNLOAD_DATA'),
        booleanParam(defaultValue: false, description: 'Infer ML trees?', name: 'INFER_TREE'),
        booleanParam(defaultValue: true, description: 'Compute SPRTA by CMAPLE?', name: 'COMPUTE_SPRTA_CMAPLE'),
        booleanParam(defaultValue: true, description: 'Compute SPRTA by MAPLE?', name: 'COMPUTE_SPRTA_MAPLE'),
        string(name: 'MODEL', defaultValue: 'JC', description: 'Substitution model'),
        booleanParam(defaultValue: false, description: 'Blengths fixed?', name: 'BLENGTHS_FIXED'),
        booleanParam(defaultValue: true, description: 'Compute supports for branches with a length of zero?', name: 'ZERO_LENGTH_BRANCHES'),
        booleanParam(defaultValue: true, description: 'Remove all exiting output files?', name: 'REMOVE_OUTPUT'),
        booleanParam(defaultValue: false, description: 'Use CIBIV cluster?', name: 'USE_CIBIV'),
    ])
])
pipeline {
    agent any
    environment {
        NCI_ALIAS = "gadi"
        SSH_COMP_NODE = " "
        WORKING_DIR = "/scratch/dx61/tl8625/cmaple/ci-cd"
        DATA_DIR = "${WORKING_DIR}/data"
        TREE_DIR = "${DATA_DIR}/tree"
        OUT_DIR = "${DATA_DIR}/output"
        LOCAL_OUT_DIR = "/Users/nhan/DATA/tmp/visualize-sprta-pipeline/output"
        SCRIPTS_DIR = "${WORKING_DIR}/scripts"
        MAPLE_SPRTA_TREE_PREFIX = "SPRTA_MAPLE_tree_"
        PYTHON_SCRIPT_PATH = "${SCRIPTS_DIR}/extract_visualize_results.py"
    }
    stages {
        stage('Init variables') {
            steps {
                script {
                    if (params.USE_CIBIV) {
                        NCI_ALIAS = "eingang"
                        SSH_COMP_NODE = " ssh -tt cox "
                        WORKING_DIR = "/project/AliSim/cmaple"
                        
                        DATA_DIR = "${WORKING_DIR}/data"
                        TREE_DIR = "${DATA_DIR}/tree"
                        OUT_DIR = "${DATA_DIR}/output"
                        LOCAL_OUT_DIR = "/Users/nhan/DATA/tmp/visualize-sprta-pipeline/output"
                        SCRIPTS_DIR = "${WORKING_DIR}/scripts"
                        PYTHON_SCRIPT_PATH = "${SCRIPTS_DIR}/extract_visualize_results.py" 
                    }
                }
            }
        }
    	stage("Build CMAPLE") {
            steps {
                script {
                	if (params.BUILD_CMAPLE) {
                        echo 'Building CMAPLE'
                        // trigger jenkins cmaple-build
                        build job: 'cmaple-build', parameters: [string(name: 'BRANCH', value: CMAPLE_BRANCH),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),]

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
                        string(name: 'MODEL', value: MODEL),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),
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
                        build job: 'cmaple-compute-sprta', parameters: [string(name: 'MODEL', value: MODEL),
                        booleanParam(name: 'BLENGTHS_FIXED', value: BLENGTHS_FIXED),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),
                        booleanParam(name: 'ZERO_LENGTH_BRANCHES', value: ZERO_LENGTH_BRANCHES),]
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
                        build job: 'maple-compute-sprta', parameters: [string(name: 'MODEL', value: MODEL),
                        booleanParam(name: 'BLENGTHS_FIXED', value: BLENGTHS_FIXED),
                        booleanParam(name: 'USE_CIBIV', value: USE_CIBIV),
                        booleanParam(name: 'ZERO_LENGTH_BRANCHES', value: ZERO_LENGTH_BRANCHES),]

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
                        ssh -tt ${NCI_ALIAS} << EOF
                        mkdir -p ${SCRIPTS_DIR}
                        exit
                        EOF
                        """
                	sh "scp -r scripts/* ${NCI_ALIAS}:${SCRIPTS_DIR}"
                	if (params.REMOVE_OUTPUT) {
                		sh """
                        ssh -tt ${NCI_ALIAS} << EOF
                        rm -f ${OUT_DIR}/*
                        exit
                        EOF
                        """
                        sh "rm -f {LOCAL_OUT_DIR}/*"
                	}
                    sh """
                        ssh -tt ${NCI_ALIAS} ${SSH_COMP_NODE}<< EOF
                                              
                        sh ${SCRIPTS_DIR}/extract_visualize_results.sh ${PYTHON_SCRIPT_PATH} ${TREE_DIR} ${OUT_DIR} ${MAPLE_SPRTA_TREE_PREFIX} 
                        
                        exit
                        EOF
                        """
        			sh "mkdir -p {LOCAL_OUT_DIR} && scp -r ${NCI_ALIAS}:${OUT_DIR}/* ${LOCAL_OUT_DIR}"
        			sh "mkdir -p {LOCAL_OUT_DIR} && scp -r ${NCI_ALIAS}:${TREE_DIR} ${LOCAL_OUT_DIR}"
                }
            }
        }
        stage ('Verify') {
            steps {
                script {
                	sh """
                        ssh -tt ${NCI_ALIAS} << EOF
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
    // sh "ssh -tt ${NCI_ALIAS} 'rm -rf ${REPO_DIR} ${BUILD_SCRIPTS}'"
}