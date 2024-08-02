# https://www.youtube.com/watch?v=AMp6hlA8xKA
from flask import Flask
from APIsRoutes import lobby
from Sockets.SocketOrchestrator import socketio

# Initializing flask app
app = Flask(__name__)
app.register_blueprint(lobby)

socketio.init_app(app, cors_allowed_origins="*")
socketio.run(app)
