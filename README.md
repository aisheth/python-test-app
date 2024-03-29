# Sample project created to demonstrate Django Rest Framework and API creation.


## How to run this project

1. Install python (above 3.7) on your machine
2. In the root folder of this project, create a virtual environment.
3. Once, the Virtual environment is created, Activate it.
4. Run the following command to install all dependent packages -
   ```
   pip install -r requirements.txt
   ```
5. Go to the src folder and run the following command to create database tables -
   ```
   python manage.py migrate
   ```
6. Next you have to create a superuser to access protected APIs. Run the following command to create a superuser
   ```
   python manage.py createsuperuser
   ```
   Fill in the details and complete the superuser creation process.
7. Run the following command to run the project
   ```
   python manage.py runserver
