# Sample project created to demonstrate Django Rest Framework and API creation.


## How to run this project

1. Install python (above 3.7) on your machine
2. In root folder of this project, create a virtual environment. You can find more about virtual environment.
3. Once Virtual environment is created, Activate it.
4. Run following command to install all dependent packages -
   ```
   pip install -r requirements.txt
   ```
5. Go to src folder and run following command to create database tables -
   ```
   python manage.py migrate
   ```
6. Next you have to create a superuser to access protected APIs. Run following command to create a superuser
   ```
   python manage.py createsuperuser
   ```
   Fill in details and complete superuser creation process.
7. Run following command to run the project
   ```
   python manage.py runserver
