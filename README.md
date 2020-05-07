# Project Scanner

## Using Docker:
*  [Installation for Linux (using Docker)](#installation_for_linux_docker)
*  [Installation for MACOS (using Docker)](#installation_for_macos_docker)
*  [Installation for Windows (using Docker)](#installation_for_windows_docker)
## **Not** Using Docker:
*  [Installation for Linux (not using Docker)](#installation_for_linux)
*  [Installation for MACOS (not using Docker)](#installation_for_macos)
*  [Installation for Windows (not using Docker)](#installation_for_windows)

## WITH DOCKER

## Installation for linux <a name="installation_for_linux_docker"></a>

### 1. Install Git, Python3, pip3 and virtualenv
    sudo apt-get update
    sudo apt install git python3 python3-pip python3-venv -y

### 2. Needs for clone the repository. Have 2 ways: 
    
##### 2.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 2.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

### 3. Next needs for create and activate virtualenv
    3.1. choose location
    3.2. python3 -m venv name_venv
    3.3.1. [In terminal]: source location/name_venv/bin/activate
    3.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/name_venv/bin/python3
    
### 4. Upgrade pip3 and install requirements 
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
### 5. Install Docker
    Install Docker from [https://www.docker.com](docker.com)
    (Don't forget about the registration)
    In application "Docker" needs to authorize
    
### 6. Up the project
    [In Terminal]: docker-compose up
    
    
## Installation for MACOS <a name="installation_for_macos_docker"></a>

### 1. Install Homebrew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

### 2. Install Git, Python3, pip3 and virtualenv
    brew update
    brew install git python3 python3-pip python3-venv
    
### 3. Needs for clone the repository. Have 2 ways: 
    
##### 3.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 3.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git
    
### 4. Next needs for create and activate virtualenv
    4.1. choose location
    4.2. python3 -m venv venv
    4.3.1. [In terminal]: source location/name_venv/bin/activate
    4.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/venv/bin/python3

### 5. Upgrade pip3 and install requirements 
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
### 6. Install Docker
    Install Docker from [https://www.docker.com](docker.com)
    (Don't forget about the registration)
    In application "Docker" needs to authorize
    
### 7. Up the project
    [In Terminal]: docker-compose up
    
## Installation for windows <a name="installation_for_windows_docker"></a>

### 1. Install Git, Python, pip and virtualenv
    Ссылка на установку Git for windows (установщик, 
    запускать от имени администратора):
    https://git-scm.com/download/win
    
    Ссылка на установку Python for windows (установщик, 
    запускать от имени администратора):
    https://www.python.org/downloads/

### 2. Needs for clone the repository. Have 2 ways: 
    
##### 2.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 2.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

### 3. Next needs for create and activate virtualenv
    3.1. choose location
    3.2. python -m venv venv
    3.3.1. [In terminal]: location\name_venv\Scripts\activate
    3.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location\venv\Scripts\python.exe
    
### 4. Upgrade pip3 and install requirements 
    pip install --upgrade pip
    pip install -r requirements.txt
    
### 6. Install Docker
    Install Docker from [https://www.docker.com](docker.com)
    (Don't forget about the registration)
    In application "Docker" needs to authorize
    
### 7. Up the project
    [In Terminal]: docker-compose up
    

## WITHOUT DOCKER


## Installation for linux <a name="installation_for_linux"></a>

### 1. Install Git, Python3, pip3 and virtualenv
    sudo apt-get update
    sudo apt install git python3 python3-pip python3-venv -y

### 2. Needs for clone the repository. Have 2 ways: 
    
##### 2.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 2.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

### 3. Next needs for create and activate virtualenv
    3.1. choose location
    3.2. python3 -m venv venv
    3.3.1. [In terminal]: source location/name_venv/bin/activate
    3.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/venv/bin/python3
    
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
    
### 7. Меняем настройки в settings.py
    1.  Закомментировать словарь DATABASES, который ниже "WITH DOCKER"
    2.  Раскомментировать словарь DATABASES, который ниже "WITHOUT DOCKER"
    
    
## Installation for MACOS <a name="installation_for_macos"></a>

### 1. Install Homebrew
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

### 2. Install Git, Python3, pip3 and virtualenv
    brew update
    brew install git python3 python3-pip python3-venv
    
### 3. Needs for clone the repository. Have 2 ways: 
    
##### 3.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 3.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git
    
### 4. Next needs for create and activate virtualenv
    4.1. choose location
    4.2. python3 -m venv venv
    4.3.1. [In terminal]: source location/name_venv/bin/activate
    4.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location/venv/bin/python3
    
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
    
### 8. Меняем настройки в settings.py
    1.  Закомментировать словарь DATABASES, который ниже "WITH DOCKER"
    2.  Раскомментировать словарь DATABASES, который ниже "WITHOUT DOCKER"
    
## Installation for windows <a name="installation_for_windows"></a>

### 1. Install Git, Python, pip and virtualenv
    Ссылка на установку Git for windows (установщик, 
    запускать от имени администратора):
    https://git-scm.com/download/win
    
    Ссылка на установку Python for windows (установщик, 
    запускать от имени администратора):
    https://www.python.org/downloads/

### 2. Needs for clone the repository. Have 2 ways: 
    
##### 2.1. HARD. Choose path, init git and clone the repository
    git init
    git clone https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

##### 2.2. EASY. By PyCharm
    1. Open PyCharm (without project)
    2. Choose "Get from Version Control"
    3. Paste the url https://gitlab.informatics.ru/2019-2020/online/s101/scaner.git

### 3. Next needs for create and activate virtualenv
    3.1. choose location
    3.2. python -m venv venv
    3.3.1. [In terminal]: location\name_venv\Scripts\activate
    3.3.2. [In PyCharm]: PyCharm preferences -> Project: name -> Project: Interpreter -> 
    -> Add -> choose "Existing environment" -> "..." -> choose location\venv\Scripts\python.exe
    
### 4. Upgrade pip3 and install requirements 
    pip install --upgrade pip
    pip install -r requirements.txt
    
### 5. Migrate to PostgreSQL 
    Теперь самое интересное, 
    хотя это несложно, как оказалось :)
    
    Ссылка на установку Postgres for windows (установщик, 
    запускать от имени администратора):
    https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows
    
    Устанавливаем пакет (все настройки можно оставить по умолчанию, пароль поставить postgres).
    После установки выполняем все в следующем порядке:
    5.1. в программах находим pgAdmin 4 и открываем
    5.2. заходим во вкладку server 
    5.3. вводим пароль postgres во всплывающем окне
    5.4. нажимаем на databases ПКМ -> create -> database
    5.5. вкладка general:
    database API_DB
    owner postgres
    все остальное по умолчанию
    5.6. save
    5.7. аналогично с WEB_DB
    
### 6. Дальше все, как обычно
    python manage.py makemigrations
    python manage.py migrate
    
### 7. Меняем настройки в settings.py
    1.  Закомментировать словарь DATABASES, который ниже "WITH DOCKER"
    2.  Раскомментировать словарь DATABASES, который ниже "WITHOUT DOCKER"