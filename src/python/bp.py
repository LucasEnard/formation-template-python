from grongier.pex import BusinessProcess
from msg import FormationRequest, TrainingRequest,PatientRequest
from obj import Training

import json
import statistics


class Router(BusinessProcess):

    def on_request(self, request):
        """
        It receives a request, checks if it is a formation request, and if it
        is, it sends a TrainingRequest request to FileOperation, which in turn sends it to the IrisOperation, which in
        turn sends it to the PostgresOperation if IrisOperation returned a 1.
        
        :param request: The request object that was received
        :return: None
        """
        if isinstance(request,FormationRequest):

            msg = TrainingRequest()
            msg.training = Training()
            msg.training.name = request.formation.nom
            msg.training.room = request.formation.salle

            self.send_request_sync('Python.FileOperation',msg)
            
            form_iris_resp = self.send_request_sync('Python.IrisOperation',msg)
            if form_iris_resp.decision == 1:
                self.send_request_sync('Python.PostgresOperation',msg)
        return None

class PatientProcess(BusinessProcess):

    def on_request(self, request):
        """
        It takes a request, checks if it's a PatientRequest, and if it is, it calculates the average number
        of steps for the patient and sends the request to the Python.FileOperation service.
        
        :param request: The request object that was sent to the service
        :return: None
        """
        if isinstance(request,PatientRequest):
            request.patient.avg = statistics.mean(list(map(lambda x: int(x['steps']),json.loads(request.patient.infos))))
            self.send_request_sync('Python.FileOperation',request)
        return None
