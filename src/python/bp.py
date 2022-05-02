from grongier.pex import BusinessProcess
from msg import FormationRequest, TrainingRequest,PatientRequest
from obj import Training

import json
import statistics


class Router(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,FormationRequest):

            msg = TrainingRequest()
            msg.training = Training()
            msg.training.name = request.formation.nom
            msg.training.room = request.formation.salle

            self.send_request_sync('Python.FileOperation',msg)
            
            form_iris_resp = self.send_request_sync('Python.IrisOperation',msg)
            typ = type(form_iris_resp)
            #self.log_info(typ)
            #self.log_info(form_iris_resp)
            #self.log_info(form_iris_resp.decision)
            if True: #form_iris_resp.decision == 1:
                self.send_request_sync('Python.PostgresOperation',msg)
        return None

class PatientProcess(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,PatientRequest):
            request.patient.avg = statistics.mean(list(map(lambda x: int(x['steps']),
                json.loads(request.patient.infos))))
            self.send_request_sync('Python.FileOperation',request)
        return None
