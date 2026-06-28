Windows run commands:

cd C:\Users\%USERNAME%\Documents\tewahedo_sunday_project\tewahedo_sunday
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Open:
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/

The custom User model automatically sets superusers to role='admin' and is_approved=True.
