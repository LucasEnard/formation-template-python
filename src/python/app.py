from flask import Flask, jsonify, request
from grongier.pex import Director

from obj import Formation
from msg import FormationRequest


app = Flask(__name__)

# ----------------------------------------------------------------
### CRUD FOR Person
# ----------------------------------------------------------------

# GET Infos
@app.route("/", methods=["GET"])
def getInfo():
    info = {'version':'1.0.6'}
    return jsonify(info)

@app.route("/training/", methods=["GET"])
def getAlltraining():
    payload = {}
    return jsonify(payload)

@app.route("/training/", methods=["POST"])
def postPerson():
    payload = {} 

    formation = Formation(request.get_json()['id'],request.get_json()['nom'],request.get_json()['salle'])
    msg = FormationRequest(formation=formation)

    tService = Director.CreateBusinessService("Python.FlaskService")
    response = tService.dispatchProcessInput(msg)


    return jsonify(payload)

# GET person with id
@app.route("/training/<int:id>", methods=["GET"])
def getPerson(id):
    payload = {}
    return jsonify(payload)

# PUT to update person with id
@app.route("/training/<int:id>", methods=["PUT"])
def updatePerson(id):

    payload = {}
    return jsonify(payload)

# DELETE person with id
@app.route("/training/<int:id>", methods=["DELETE"])
def deletePerson(id):
    payload = {}  
    return jsonify(payload)


# ----------------------------------------------------------------
### MAIN PROGRAM
# ----------------------------------------------------------------

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8081")