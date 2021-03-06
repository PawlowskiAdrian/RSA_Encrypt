#!/bin/bash
source env_file
# ONE TIME ENCRYPT/DECRYPT WITH DEPLOYMENT OVER THE NETWORK
ssh $SSH_USER@$SSH_IP -p $SSH_PORT << EOF
	cd ~/
	rm 0000*
	python3 PREPARE.py
	exit
EOF
scp -P $SSH_PORT $SSH_USER@$SSH_IP:~/00001-key.pub ./00002-key.pub
echo -e '3' | python3 SECURE.py
scp -P $SSH_PORT ${OUTPUT_FOLDER}/* $SSH_USER@$SSH_IP:~/
ssh $SSH_USER@$SSH_IP -p $SSH_PORT << EOF
    cd ~/
    echo -e '4' | python3 SECURE.py
	cd ${OUTPUT_FOLDER}
	nohup python3 secret.py &
	sleep 5
	rm -r __pycache__/
	cd ..
	rm -r __pycache__/
	rm *.bin
	rm 0000*
	exit
EOF
