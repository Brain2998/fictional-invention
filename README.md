# fictional-invention

## Installation

### Initialize database

Initialize database from createDatabase.sql script

### Setup database connection

Database credentials are stored in environment variables. In order to establsih a database connection you need to create following environment variables:

- DatabaseLogin: stores database user
- DatabasePassword: stores databasse password

Creating environment variable in Windows:
```bash
setx DatabaseLogin login
setx DatabasePassword password
```

Creating environment variable in Linux:
```bash
export DatabaseLogin=login
export DatabasePassword=password
```

### Installing dependencies

```bash
pip3 install -r requirements.txt
```

## Running server

```bash
python3 main.py
```
## Preinstalled users

admin/P@ssw0rd
user/qwerty
