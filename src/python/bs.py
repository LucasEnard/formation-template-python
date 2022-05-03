from grongier.pex import BusinessService,Message

class ServiceCSV(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_process_input(self,request):
        return None

class FlaskService(BusinessService):

    def on_process_input(self,request):
        return None

