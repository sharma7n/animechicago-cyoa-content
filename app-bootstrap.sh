# Sets up python runtime and library dependencies for development on a fresh Cloud9 workspace.
# To execute: bash app-bootstrap.sh

sudo apt-get update
sudo apt-get install python3.6 python3.6-venv -y
sudo python3.6 -m ensurepip --upgrade
pip3 install --user pipenv
echo 'export PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"' >> ~/.profile 
echo 'export PATH="$PATH:$PYTHON_BIN_PATH"' >> ~/.profile 
source ~/.profile
pipenv install --dev