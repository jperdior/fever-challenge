from src.api.bootstrap import create_app

app = create_app()
celery_app = app.extensions["CELERY"]
