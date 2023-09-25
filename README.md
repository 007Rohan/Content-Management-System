# Content-Management-System


### How to setup locally
#### Requirements

- Python3
- pip
- venv


#### setup instructions

- create   a virtualenv using venv
```cmd
   python -m pip install --upgrade pip
   pip install virtualenv
   python3 -m venv venv
   ```
- activate it 
```cmd
   source venv/bin/activate
   ```
- or activate Windows
```cmd
   venv/bin/activate.bat
   ```
- install dependencies from the requirements.txt file
```cmd
   pip install -r requirements.txt
   ```

- migrate the database tables
```cmd
   python manage.py migrate
   ```
- start a development server using 
```cmd
   python manage.py runserver
   ```
