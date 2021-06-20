# drf_excel_json
GET API endpoint using Django that would pull data from the Excel and transform the data into a JSON response 


[![Python Version](https://img.shields.io/badge/python-3.8-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.0.20-brightgreen.svg)](https://djangoproject.com)

## Running the Project Locally
First, clone the repository to your local machine:

```bash
git clone https://github.com/amity29/drf_excel_json.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```


Create .env file in the settings.py directory

Set up following environment variable:

```
    SECRET_KEY =
    DEBUG =
```


Finally, run the development server:

```bash
python manage.py runserver
```

The API endpoints will be available at **http://127.0.0.1:8000/** by default.

## API endpoints details

#### Get data
```
    http://{server}:{port}
```
