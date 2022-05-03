from grongier.pex import BusinessOperation
from msg import TrainingRequest,TrainingResponse,PatientRequest
import iris
import os
import psycopg2
import random


class FileOperation(BusinessOperation):
    """
    It is an operation that write a training or a patient in a file
    """
    def on_init(self):
        """
        It changes the current working directory to the one specified in the path attribute of the object,
        or to /tmp if no path attribute is specified. It also sets the filename attribute to toto.csv if it
        is not already set
        :return: None
        """
        if hasattr(self,'path'):
            os.chdir(self.path)
        else:
            os.chdir("/tmp")
        if not hasattr(self,'filename'):
            self.filename = 'toto.csv'
        return None

    def write_training(self, request:TrainingRequest):
        """
        It writes a training to a file
        
        :param request: The request message
        :type request: TrainingRequest
        :return: None
        """
        room = name = ""
        if request.training is not None:
            room = request.training.room
            name = request.training.name
        line = room+" : "+name+"\n"
        self.put_line(self.filename, line)
        return None

    def write_patient(self, request:PatientRequest):
        """
        It writes the name and average number of steps of a patient in a file
        
        :param request: The request message
        :type request: PatientRequest
        :return: None
        """
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
        """
        It opens a file, appends a string to it, and closes the file
        
        :param filename: The name of the file to write to
        :param string: The string to be written to the file
        """
        try:
            with open(filename, "a",encoding="utf-8",newline="") as outfile:
                outfile.write(string)
        except Exception as error:
            raise error

class IrisOperation(BusinessOperation):
    """
    It is an operation that write trainings in the iris database
    """

    def insert_training(self, request:TrainingRequest):
        """
        It takes a `TrainingRequest` object, inserts a new row into the `iris.training` table, and returns a
        `TrainingResponse` object
        
        :param request: The request object that will be passed to the function
        :type request: TrainingRequest
        :return: A TrainingResponse message
        """
        resp = TrainingResponse()
        resp.decision = round(random.random())
        sql = """
        INSERT INTO iris.training
        ( name, room )
        VALUES( ?, ? )
        """
        iris.sql.exec(sql,request.training.name,request.training.room)
        return resp

    def on_message(self, request):
        return None

class PostgresOperation(BusinessOperation):
    """
    It is an operation that write trainings in the Postgre database
    """
    
    def on_init(self):
        """
        it is a function that connects to the Postgre database and init a connection object
        :return: None
        """
        self.conn = psycopg2.connect(
        host="db",
        database="DemoData",
        user="DemoData",
        password="DemoData",
        port="5432")
        self.conn.autocommit = True
        return None

    def on_tear_down(self):
        """
        It closes the connection to the database
        :return: None
        """
        self.conn.close()
        return None

    def insert_training(self,request:TrainingRequest):
        """
        It inserts a training in the Postgre database
        
        :param request: The request object that will be passed to the function
        :type request: TrainingRequest
        :return: None
        """
        cursor = self.conn.cursor()
        sql = "INSERT INTO public.formation ( name,room ) VALUES (%s , %s )"
        cursor.execute(sql,(request.training.name,request.training.room))
        return None

    def on_message(self,request):
        return None
