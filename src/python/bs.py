from grongier.pex import BusinessService,Message
from dataclass_csv import DataclassReader
from obj import Formation,Patient
from msg import FormationRequest,PatientRequest

import requests
import json

class ServiceCSV(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        if not hasattr(self,'path'):
            self.path = '/irisdev/app/misc/'
        return None

    def on_process_input(self,request):
        filename='formation.csv'
        with open(self.path+filename,encoding="utf-8") as formation_csv:
            reader = DataclassReader(formation_csv, Formation,delimiter=";")
            for row in reader:
                msg = FormationRequest()
                msg.formation = row
                self.SendRequestSync('Python.Router',msg)
        return None

class FlaskService(BusinessService):

    def on_init(self):
        if not hasattr(self,'target'):
            self.target = "Python.Router"
        return None

    def on_process_input(self,request):
        return self.SendRequestSync(self.target,request)

class PatientService(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        if not hasattr(self,'target'):
            self.target = 'Python.PatientProcess'
        if not hasattr(self,'api_url'):
            self.api_url = "https://lucasenard.github.io/Data/patients.json"
        return None

    def on_process_input(self,request):
        req = requests.get(self.api_url)
        if req.status_code == 200:
            dat = req.json()
            for key,val in dat.items():
                patient = Patient()
                patient.name = key
                patient.infos = json.dumps(val)
                msg = PatientRequest()
                msg.patient = patient                
                self.SendRequestSync(self.target,msg)
        return None
