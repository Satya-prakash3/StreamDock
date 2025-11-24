For Local Run uvicorn uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

For Production run gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level info --access-logfile - --error-logfile - app.main:app --reload
