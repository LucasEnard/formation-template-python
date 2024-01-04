import csv
import os
from training.msg import FormationRequest
from grongier.pex import BusinessService

class ReadCsvBs(BusinessService):

    def get_adapter_type():
        # This is mandatory to schedule the service
        # By default, the service will be scheduled every 5 seconds
        return "Ens.InboundAdapter"
    
    def on_init(self):
        # Check if the instane of ReadCsvBs has a filename attribute
        # If not, set it to 'formation.csv' as default value
        if not hasattr(self, 'filename'):
            self.filename = 'formation.csv'
        # Check if the instane of ReadCsvBs has a path attribute
        # If not, set it to '/irisdev/app/data/' as default value
        if not hasattr(self, 'path'):
            self.path = '/irisdev/app/misc/'
        # Check if the target attribute is set
        if not hasattr(self, 'target'):
            # If not, set it to 'Instance.Of.SaveInTxtBo' as default value
            self.target = 'Instance.Of.SaveInTxtBo'

    def on_process_input(self, message_input):
        # Open the csv file
        with open(os.path.join(self.path, self.filename), newline='') as csvfile:
            # Create a csv reader
            reader = csv.reader(csvfile, delimiter=';')
            # Skip the header
            next(reader)
            # For each row in the csv file
            for row in reader:
                # Create a FormationRequest message
                msg = FormationRequest()
                # Set the attributes of the message
                msg.id = int(row[0])
                msg.nom = row[1]
                msg.salle = row[2]
                # Send the message to the business operation
                self.send_request_sync(self.target,msg)
                # Log the message
                self.log_info(f'FormationRequest {msg.id} sent to {self.target}')