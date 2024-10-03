from src.api.config.bootstrap import create_app

app = create_app()
celery_app = app.extensions["CELERY"]
celery_app.conf.update(app.config)
