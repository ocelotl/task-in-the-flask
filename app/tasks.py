from . import create_celery_app, create_app

app = create_app()
celery = create_celery_app(app)


@celery.task
def send_email(to_email):
    # Code to send email
    pass
