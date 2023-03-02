# Django-DRF-JWT-API-CRUD
This is a Django Rest Framework project wiche provide APIs that allows users to register,like, unlike, and post article .
 
## Technologies Used
- Django
- Rest Framework
- Django Rest Framework
- JWT
- yasg


## Installation
1. Clone the repository to your local machine:

        git clone https://github.com/srahnama/Django-DRF-JWT-API-CRUD.git

2. Create a virtual environment and activate it:

        python -m venv venv
        source venv/bin/activate
3. Install the project dependencies::

        pip install -r requirements.txt
4. Run the following command:

        python manage.py makemigrations

This will analyze your models and create new migration files for any changes that have been detected since the last migration.

5. Apply the new migrations to your database by running the following command:

        python manage.py migrate

6. Then create a super user:

        python manage.py createsuperuser    

7. Start the development server:
 
        python manage.py runserver

8. Open your web browser and navigate to http://localhost:8000/api/ to view the project.
All APIs are there.
    You can find Swagger on this path:

        http://localhost:8000/api/swagger/
        
    The Redoc which is documentaion of project is here:

    
        http://localhost:8000/api/redoc/