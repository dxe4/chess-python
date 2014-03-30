source venv/bin/activate

echo "staring websocket server"
python sockets/server.py &

echo "starting redis"
redis-server

echo "starting gunicorn"
gunicorn -b 127.0.0.1:8080 -w 4 main:application &
