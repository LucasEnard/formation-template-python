from grongier.pex import BusinessOperation
from msg import TrainingRequest,FormationRequest,TrainingResponse,PatientRequest
import iris
import os
import psycopg2
import random


class FileOperation(BusinessOperation):

    def on_init(self):
        if hasattr(self,'path'):
            os.chdir(self.path)
        else:
            os.chdir("/tmp")
        if not hasattr(self,'filename'):
            self.filename = 'toto.csv'
        return None

    def write_training(self, request:TrainingRequest):
        room = name = ""
        if request.training is not None:
            room = request.training.room
            name = request.training.name
        line = room+" : "+name+"\n"
        self.put_line(self.filename, line)
        return None

    def write_patient(self, request:PatientRequest):
        name = ""
        avg = 0
        if request.patient is not None:
            name = request.patient.name
            avg = request.patient.avg
        line = name + " avg nb steps : " + str(avg) +"\n"
        filename = 'Patients.csv'
        self.put_line(filename, line)
        return None

    def on_message(self, request):
        return None


    def put_line(self,filename,string):
        try:
            with open(filename, "a",encoding="utf-8",newline="") as outfile:
                outfile.write(string)
        except Exception as error:
            raise error

class IrisOperation(BusinessOperation):

    def insert_training(self, request:TrainingRequest):
        resp = TrainingResponse()
        resp.decision = round(random.random())
        sql = """
        INSERT INTO iris.training
        ( name, room )
        VALUES( ?, ? )
        """
        #self.log_info(resp)
        #self.log_info(resp.decision)
        iris.sql.exec(sql,request.training.name,request.training.room)
        return None #resp

    def on_message(self, request):
        return None

class PostgresOperation(BusinessOperation):

    def on_init(self):
        self.conn = psycopg2.connect(
        host="db",
        database="DemoData",
        user="DemoData",
        password="DemoData",
        port="5432")
        self.conn.autocommit = True
        return None

    def on_tear_down(self):
        self.conn.close()
        return None

    def insert_training(self,request:TrainingRequest):
        cursor = self.conn.cursor()
        sql = "INSERT INTO public.formation ( nom,salle ) VALUES ( %s , %s )"
        cursor.execute(sql,(request.training.nom,request.training.salle))
        return None

    def on_message(self,request):
        return None
