#nohup python manage.py celery worker -B --loglevel=info > celery.log &nohup python-smallpay celeryapp.py worker -B --loglevel=info > celery.log &