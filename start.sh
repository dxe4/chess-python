source venv/bin/activate

echo "starting redis"
redis-server

echo "starting gunicorn"
python app/application.py
