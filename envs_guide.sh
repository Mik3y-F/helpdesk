export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/<DB name given to createdb>
# Optional: set broker URL if using Celery

export CELERY_BROKER_URL=redis://localhost:6379/0
