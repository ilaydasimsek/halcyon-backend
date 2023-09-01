echo "Running release command in environment: $ENVIRONMENT"

python manage.py collectstatic --noinput || { echo "Collectstatic failed!"; exit 1; }
python manage.py migrate --noinput || { echo "Migration failed!"; exit 1; }
python manage.py runserver 0.0.0.0:8000
