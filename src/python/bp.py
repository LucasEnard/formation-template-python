from grongier.pex import BusinessProcess


class Router(BusinessProcess):

    def on_request(self, request):
        return None

class PatientProcess(BusinessProcess):

    def on_request(self, request):
        return None
