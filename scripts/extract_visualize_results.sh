#!bin/bash

###### handle arguments ######
PYTHON_SCRIPT_PATH=$1 # path to the python script
TREE_DIR=$2 # tree dir
OUT_DIR=$3 # output dir
MAPLE_SPRTA_TREE_PREFIX=$4 # The prefix of trees with SPRTA computed by MAPLE


### pre steps #####



############
mkdir -p ${OUT_DIR}

for tree_path in "${TREE_DIR}"/MAPLE_SPRTA_TREE_PREFIX*_nexusTree.tree; do
	tree=$(basename "$tree_path")
    echo "Extract results from ${tree} and visualize them to ${OUT_DIR}/${tree}.png"
    echo "cd ${OUT_DIR} && ${PYTHON_SCRIPT_PATH} --input ${TREE_DIR}/${tree} --output${OUT_DIR}/${tree}"
    cd ${OUT_DIR} && ${PYTHON_SCRIPT_PATH} --input ${TREE_DIR}/${tree} --output${OUT_DIR}/${tree}
done
                        