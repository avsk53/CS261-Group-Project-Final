# find out which machine we are on
grep -qs dcs.warwick.ac.uk /etc/resolv.conf
if [ $? -eq 0 ]; then # dcs will contain 0 if this is DCS warwick
 portid=5${USER: -4}
else
 portid=5005
fi

# add the FLASK RUN PORT to .env if it doesn't alrady exist
if ! grep -qs FLASK_RUN_PORT ".env" ; then
    echo Creating .env
    echo FLASK_ENV=development >.env

    
    echo FLASK_RUN_PORT=$portid >> .env
fi

# add virtual environment if it doesn't already exist
if ! [[ -d vpip ]]; then
    echo Adding virtual environment 
    python3 -m venv vpip

    # create pip.conf if doesn't exist
    echo Creating vpip/pip.conf
    ( cat <<'EOF'
[install]
user = false
EOF
    ) > vpip/pip.conf

    source vpip/bin/activate

    echo Setting up Flask requirements
    pip install -r requirements.txt
    deactivate
fi

# activate the virtual environment for the coursework
source vpip/bin/activate

# run Flask for coursework
./run.sh app
