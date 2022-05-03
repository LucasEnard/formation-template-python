from flask import Flask, jsonify


app = Flask(__name__)


# GET Infos
@app.route("/", methods=["GET"])
def get_info():
    info = {'version':'1.0.6'}
    return jsonify(info)

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8081")