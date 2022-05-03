from flask import Flask, jsonify, request
from grongier.pex import Director

from obj import Formation
from msg import FormationRequest


app = Flask(__name__)


# GET Infos
@app.route("/", methods=["GET"])
def get_info():
    info = {'version':'1.0.6'}
    return jsonify(info)

@app.route("/training/", methods=["GET"])
def get_all_training():
    payload = {}
    return jsonify(payload)

@app.route("/training/", methods=["POST"])
def post_formation():
    payload = {} 

    formation = Formation()
    formation.nom = request.get_json()['nom']
    formation.salle = request.get_json()['salle']
    msg = FormationRequest(formation=formation)

    t_service = Director.CreateBusinessService("Python.FlaskService")
    response = t_service.dispatchProcessInput(msg)

    return jsonify(payload)

# GET formation with id
@app.route("/training/<int:id>", methods=["GET"])
def get_formation(id):
    payload = {}
    return jsonify(payload)

# PUT to update foramtion with id
@app.route("/training/<int:id>", methods=["PUT"])
def update_formation(id):
    payload = {}
    return jsonify(payload)

# DELETE formation with id
@app.route("/training/<int:id>", methods=["DELETE"])
def delete_formation(id):
    payload = {}  
    return jsonify(payload)

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8081")