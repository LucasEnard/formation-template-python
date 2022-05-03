from grongier.pex import BusinessService,Message
from dataclass_csv import DataclassReader
from obj import Formation,Patient
from msg import FormationRequest,PatientRequest

import requests
import json

class ServiceCSV(BusinessService):
    """
    It reads a csv file every 5 seconds, and sends each line as a message to the Python Router process.
    """
    
    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        """
        It changes the current path to the file to the one specified in the path attribute of the object,
        or to '/irisdev/app/misc/' if no path attribute is specified
        :return: None
        """
        if not hasattr(self,'path'):
            self.path = '/irisdev/app/misc/'
        return None

    def on_process_input(self,request):
        """
        It reads the formation.csv file, creates a FormationRequest message for each row, and sends it to
        the Python.Router process.
        
        :param request: the request object
        :return: None
        """
        filename='formation.csv'
        with open(self.path+filename,encoding="utf-8") as formation_csv:
            reader = DataclassReader(formation_csv, Formation,delimiter=";")
            for row in reader:
                msg = FormationRequest()
                msg.formation = row
                self.send_request_sync('Python.Router',msg)
        return None

class FlaskService(BusinessService):

    def on_init(self):
        """
        It changes the current target of our API to the one specified in the target attribute of the object,
        or to 'Python.Router' if no target attribute is specified
        :return: None
        """
        if not hasattr(self,'target'):
            self.target = "Python.Router"
        return None

    def on_process_input(self,request):
        """
        It is called to transmit information from the API directly to the Python.Router process.
        :return: None
        """
        return self.send_request_sync(self.target,request)

class PatientService(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        """
        It changes the current target of our API to the one specified in the target attribute of the object,
        or to 'Python.PatientProcess' if no target attribute is specified.
        It changes the current api_url of our API to the one specified in the target attribute of the object,
        or to 'https://lucasenard.github.io/Data/patients.json' if no api_url attribute is specified.
        :return: None
        """
        if not hasattr(self,'target'):
            self.target = 'Python.PatientProcess'
        if not hasattr(self,'api_url'):
            self.api_url = "https://lucasenard.github.io/Data/patients.json"
        return None

    def on_process_input(self,request):
        """
        It makes a request to the API, and for each patient it finds, it creates a Patient object and sends
        it to the target
        
        :param request: The request object that was sent to the service
        :return: None
        """
        req = requests.get(self.api_url)
        if req.status_code == 200:
            dat = req.json()
            for key,val in dat.items():

                patient = Patient()
                patient.name = key
                patient.infos = json.dumps(val)

                msg = PatientRequest()
                msg.patient = patient

                self.send_request_sync(self.target,msg)
        return None
