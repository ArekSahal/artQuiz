from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from random import randint, choice
from get_data import get_img

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=["POST"])
def hello_world():
    req = request.get_json()
    data = req["data"]
    groups = data["groups"]
    img = get_img(groups)
    print(img)


    return jsonify({"answer": img[0], "imgurl": img[1]})

@app.route("/", methods=["GET"])
def hello():
    return "You should not be here."


if __name__ == '__main__':
    app.run(debug=True)


