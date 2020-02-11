# Project Scanner

*  [Installation for Linux](#installation_for_linux)
*  [Installation for MACOS](#installation_for_macos)

## Instalation for linux
<a name="installation_for_linux"></a>

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
    3.1. choose location
    3.2. python3 -m venv name_venv
    3.3.1. [In terminal]: source location/name_venv/bin/activate
    3.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/name_venv/bin/python3
    
### 4. Upgrade pip3 and install requirements 
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
### 5. Migrate to PostgreSQL 
    sudo apt-get install postgresql
    sudo service postgresql start
    
    sudo -u postgres psql
    \password postgres
    
    -> Тут вам нужно будет дважды повторить пароль postgres <-
    -> Важно, чтобы пароль был таким, иначе придется перенастраивать проект <-
    -> Забавая штука, на макбуке все работает без пароля, а на линксе джанго наотрез отказывается подключаться к бд <-
    
    \q (чтобы выйти из psql)
    
    sudo -u postgres createdb API_DB
    sudo -u postgres createdb WEB_DB
    
### 6. Дальше все, как обычно
    За исключением того, что теперь, чтобы сделать миграции для базы API, нужно использовать команду:
    python manage.py migrate --database=API_DB
    
    
## Instalation for MACOS 
<a name="installation_for_macos"></a>

### 1. Install Homebrew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

### 2. Install Git, Python3, pip3 and virtualenv
    brew update
    brew install git python3 python3-pip python3-venv
    
### 3. Needs for clone the repository. Have 2 ways: 
    
##### 3.1. HARD. Choose path, init git and clone the repository**
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 3.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url 2
    
### 4. Next needs for create and activate virtualenv
    4.1. choose location
    4.2. python3 -m venv name_venv
    4.3.1. [In terminal]: source location/name_venv/bin/activate
    4.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/name_venv/bin/python3
    
### 5. Upgrade pip3 and install requirements 
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
### 6. Migrate to PostgreSQL 
###### 6.1. Install PostgreSQL
    brew install postgresql
###### 6.2. Choose location and create database (choosen folder must be clean)
    initdb path 
###### 6.3. Create superuser, start postgresql and set password
    createuser --superuser postgres
    pg_ctl -D db_path -l logfile start 
    psql -U postgres
    \password postgres
    
    -> Тут вам нужно будет дважды повторить пароль postgres <-
    -> Важно, чтобы пароль был таким, иначе придется перенастраивать проект <-
    
    \q (чтобы выйти из psql)
    
###### 6.4. Create databases for project: API_DB and WEB_DB
    createdb --owner=postgres API_DB
    createdb --owner=postgres WEB_DB
    
###### 6.5. Stop postgresql
    pg_ctl -D db_path stop
    
### 7. Дальше все, как обычно
    За исключением того, что теперь, чтобы сделать миграции для базы API, нужно использовать команду:
    python manage.py migrate --database=API_DB