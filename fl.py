from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from os import getenv, environ

from Functions import generate_matrix, create_graph, bfs

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


global matrix


@app.route("/generate_circles", methods=["POST"])
def generate_circles():
    data = request.get_json()
    num_circles = data["numCircles"]
    connection_chance = data["connectionChance"]
    start_point = data["startPoint"]
    matrix = generate_matrix(num_circles, connection_chance / 100)
    circle_data = create_graph(matrix)
    layers = bfs(matrix, start_point)
    for i in range(num_circles):
        x = circle_data[i].x
        y = circle_data[i].y
        radius = 40
        connections = circle_data[i].neighbours
        circle_data[i] = {
            "x": x,
            "y": y,
            "radius": radius,
            "connections": connections,
            "matrix": matrix,
        }
    circle_data[len(circle_data)] = layers
    return jsonify(circle_data)


@app.route("/update_circles", methods=["POST"])
def update_circles():
    data = request.get_json()
    start_point = data["startPoint"]
    matrix = data["matrix"]
    layers = bfs(matrix, start_point)
    return jsonify(layers)


@socketio.on("move")
def handle_move(data):
    emit("move", data, broadcast=True)


if __name__ == "__main__":
    app.debug = True
    PORT = environ.get("PORT")
    socketio.run(app, port=PORT)
