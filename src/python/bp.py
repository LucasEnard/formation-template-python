from grongier.pex import BusinessProcess

import json

from msg import FormationRequest, TrainingIrisRequest,PatientRequest
from obj import Training

import statistics


class Router(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,FormationRequest):
            msg = TrainingIrisRequest()
            msg.training = Training()
            msg.training.name = request.formation.nom
            msg.training.room = request.formation.salle
            self.SendRequestSync('Python.FileOperation',request)
            form_iris_resp = self.SendRequestSync('Python.IrisOperation',msg)
            if form_iris_resp.bool:
                self.SendRequestSync('Python.PostgresOperation',request)
        return None

class PatientProcess(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,PatientRequest):
            request.patient.avg = statistics.mean(list(map(lambda x: int(x['steps']),json.loads(request.patient.infos))))
            self.SendRequestSync('Python.FileOperation',request)
        return None