#!/bin/bash
source env_file
# ONE TIME ENCRYPT/DECRYPT WITH DEPLOYMENT OVER THE NETWORK
ssh $SSH_USER@$SSH_IP -p $SSH_PORT << EOF
	cd ${$WORKING_DIR}
	rm 0000*
	python3 PREPARE.py
EOF
scp -P $SSH_PORT $SSH_USER@$SSH_IP:$WORKING_DIR/00001-key.pub ./00002-key.pub
echo -e '3' | python3 SECURE_LOCAL.py
scp -P $SSH_PORT ${OUTPUT_FOLDER}/* $SSH_USER@$SSH_IP:$WORKING_DIR/
ssh $SSH_USER@$SSH_IP -p $SSH_PORT << EOF
    cd ${$WORKING_DIR}
    echo -e '4' | python3 SECURE_REMOTE.py
	cd ${OUTPUT_FOLDER}
	rm -r __pycache__/
	cd ..
	rm -r __pycache__/
	rm *.bin
	rm 0000*
EOF
