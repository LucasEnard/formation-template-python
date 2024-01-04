import os
from training.msg import FormationRequest
from grongier.pex import BusinessOperation

class SaveInTxtBo(BusinessOperation):
    
    def on_init(self):
        # Check if the instane of SaveInTxtBo has a filename attribute
        # If not, set it to 'formation.txt' as default value
        if not hasattr(self, 'filename'):
            self.filename = 'formation.txt'
        # Check if the instane of SaveInTxtBo has a path attribute
        # If not, set it to '/irisdev/app/data/' as default value
        if not hasattr(self, 'path'):
            self.path = '/irisdev/app/data/'
        # Check is the path exists
        if not os.path.exists(self.path):
            # If not, create it
            os.makedirs(self.path)

    def on_formation_request(self, request: FormationRequest):

        with open(os.path.join(self.path, self.filename), 'a') as self.file:
            self.file.write(f'{request.id};{request.nom};{request.salle}\n')
            # log the message
            self.log_info(f'FormationRequest {request.id} saved in {self.filename}')

