web: daphne --port $PORT --bind 0.0.0.0 --ws-protocol "graphql-ws" --proxy-headers pss.asgi:application -v2
pssworker: python manage.py runworker --only-channels=http.* --only-channels=websocket.* -v2