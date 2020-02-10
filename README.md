# Project Scanner

## Instalation for linux

### 1. Install Git, Python3, pip3 and virtualenv
    sudo apt-get update
    sudo apt install git python3 python3-pip python3-venv -y

### 2. Needs for clone the repository. Have 2 ways: 
    
##### 2.1. HARD. Choose path, init git and clone the repository**
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 2.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url 2

### 3. Next needs for create and activate virtualenv
    1. choose location
    2. python3 -m venv name_venv
    3.1. [In terminal]: source location/name_venv/bin/activate
    3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/name_venv/bin/python3
    
### 4. Upgrade pip3 and install requirements 
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
### 5. Migrate to PostgreSQL 
    sudo apt-get install postgresql
    sudo -u postgres createdb API_DB
    sudo -u postgres createdb WEB_DB
    
### 6. Дальше все, как обычно
    За исключением того, что теперь, чтобы сделать миграции для базы API, нужно использовать команду:
    python manage.py migrate --database=API_DB
    
    

    