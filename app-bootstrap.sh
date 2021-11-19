# Sets up python runtime and library dependencies for development on a fresh Cloud9 workspace.
# To execute: bash app-bootstrap.sh

# --- Install Python 3.8 and pip
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv -y
sudo python3.8 -m ensurepip --upgrade

# --- Install Pipenv
pip3 install --user pipenv
echo 'export PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"' >> ~/.profile 
echo 'export PATH="$PATH:$PYTHON_BIN_PATH"' >> ~/.profile 
source ~/.profile

# --- Use Pipenv to install dependencies
pipenv install --dev

# --- Initialize Django
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser --username gitpod --email gitpod@none.com --no-input
pipenv run python manage.py collectstatic