 # 1. **Ensemble / Interoperability Formation**

 The goal of this formation is to learn InterSystems' interoperability framework using python, and particularly the use of: 
* Productions
* Messages
* Business Operations
* Adapters
* Business Processes
* Business Services
* REST Services and Operations


**TABLE OF CONTENTS:**

- [1. **Ensemble / Interoperability Formation**](#1-ensemble--interoperability-formation)
- [2. Framework](#2-framework)
- [3. Adapting the framework](#3-adapting-the-framework)
- [4. Prerequisites](#4-prerequisites)
- [5. Setting up](#5-setting-up)
  - [5.1. Docker containers](#51-docker-containers)
  - [5.2. Management Portal and VSCode](#52-management-portal-and-vscode)
  - [5.3. Saving progress](#53-saving-progress)
  - [5.4. Register components](#54-register-components)
- [6. Productions](#6-productions)
- [7. Business Operations](#7-business-operations)
  - [7.1. Creating our storage classes](#71-creating-our-storage-classes)
  - [7.2. Creating our message classes](#72-creating-our-message-classes)
  - [7.3. Creating our operations](#73-creating-our-operations)
  - [7.4. Adding the operations to the production](#74-adding-the-operations-to-the-production)
  - [7.5. Testing](#75-testing)
- [8. Business Processes](#8-business-processes)
  - [8.1. Simple BP](#81-simple-bp)
  - [8.2. Adding the process to the production](#82-adding-the-process-to-the-production)
  - [8.3. Testing](#83-testing)
- [9. Business Service](#9-business-service)
  - [9.1. Simple BS](#91-simple-bs)
  - [9.2. Adding the service to the production](#92-adding-the-service-to-the-production)
  - [9.3. Testing](#93-testing)
- [10. Getting access to an extern database using JDBC](#10-getting-access-to-an-extern-database-using-jdbc)
  - [10.1. Prerequisites](#101-prerequisites)
  - [10.2. Creating our new operation](#102-creating-our-new-operation)
  - [10.3. Configuring the production](#103-configuring-the-production)
  - [10.4. Testing](#104-testing)
  - [10.5. Exercise](#105-exercise)
  - [10.6. Solution](#106-solution)
- [11. REST service](#11-rest-service)
  - [11.1. Prerequisites](#111-prerequisites)
  - [11.2. Creating the service](#112-creating-the-service)
  - [11.3. Testing](#113-testing)
- [12. Global exercise](#12-global-exercise)
  - [12.1. Instructions](#121-instructions)
  - [12.2. Hints](#122-hints)
    - [12.2.1. bs](#1221-bs)
      - [12.2.1.1. Get information](#12211-get-information)
      - [12.2.1.2. Get information with requests](#12212-get-information-with-requests)
      - [12.2.1.3. Get information with requests and using it](#12213-get-information-with-requests-and-using-it)
      - [12.2.1.4. Get information solution](#12214-get-information-solution)
    - [12.2.2. bp](#1222-bp)
      - [12.2.2.1. Average and dict](#12221-average-and-dict)
      - [12.2.2.2. Average and dict hint](#12222-average-and-dict-hint)
      - [12.2.2.3. Average and dict with map](#12223-average-and-dict-with-map)
      - [12.2.2.4. Average and dict the answer](#12224-average-and-dict-the-answer)
    - [12.2.3. bo](#1223-bo)
  - [12.3. Solutions](#123-solutions)
    - [12.3.1. obj & msg](#1231-obj--msg)
    - [12.3.2. bs](#1232-bs)
    - [12.3.3. bp](#1233-bp)
    - [12.3.4. bo](#1234-bo)
  - [12.4. Testing](#124-testing)
  - [12.5. Conclusion of the global exercise](#125-conclusion-of-the-global-exercise)
- [13. Conclusion](#13-conclusion)

# 2. Framework

This is the IRIS Framework.

![FrameworkFull](https://raw.githubusercontent.com/thewophile-beep/formation-template/master/misc/img/FrameworkFull.png)

The components inside of IRIS represent a production. Inbound adapters and outbound adapters enable us to use different kind of format as input and output for our databse. <br>The composite applications will give us access to the production through external applications like REST services.

The arrows between them all of this components are **messages**. They can be requests or responses.

# 3. Adapting the framework

In our case, we will read lines from a csv file and save it into the IRIS database and in a .txt file. 

We will then add an operation that will enable us to save objects in an extern database too, using JDBC. This database will be located in a docker container, using postgre.

Finally, we will see how to use composite applications to insert new objects in our database or to consult this database (in our case, through a REST service).

The framework adapted to our purpose gives us:

WIP
![FrameworkAdapted](https://raw.githubusercontent.com/thewophile-beep/formation-template/master/misc/img/FrameworkAdapted.png)


# 4. Prerequisites

For this formation, you'll need:
* VSCode: https://code.visualstudio.com/
* The InterSystems addons suite for vscode: https://intersystems-community.github.io/vscode-objectscript/installation/
* Docker: https://docs.docker.com/get-docker/
* The docker addon for VSCode.
* Automatically done : [Postgre requisites](#101-prerequisites)
* Automatically done : [Flask requisites](#111-prerequisites)

# 5. Setting up 


## 5.1. Docker containers


In order to have access to the InterSystems images, we need to go to the following url: http://container.intersystems.com. After connecting with our InterSystems credentials, we will get our password to connect to the registry. In the docker VScode addon, in the image tab, by pressing connect registry and entering the same url as before (http://container.intersystems.com) as a generic registry, we will be asked to give our credentials. The login is the usual one but the password is the one we got from the website.

From there, we should be able to build and compose our containers (with the `docker-compose.yml` and `Dockerfile` files given).

## 5.2. Management Portal and VSCode

This repository is ready for [VS Code](https://code.visualstudio.com/).

Open the locally-cloned `formation-template` folder in VS Code.

If prompted (bottom right corner), install the recommended extensions.

When prompted, reopen the folder inside the container so you will be able to use the python components within it. The first time you do this it may take several minutes while the container is readied.

By opening the folder remote you enable VS Code and any terminals you open within it to use the python components within the container. Configure these to use `/usr/irissys/bin/irispython`

<img width="1614" alt="PythonInterpreter" src="https://user-images.githubusercontent.com/47849411/145864423-2de24aaa-036c-4beb-bda0-3a73fe15ccbd.png">

## 5.3. Saving progress

A part of the things we will be doing will be saved locally, but productions are saved in the docker container. In order to persist all of our progress, we need to export every class that is created through the Management Portal with the InterSystems addon `ObjectScript`:

![ExportProgress](https://user-images.githubusercontent.com/77791586/164473715-b08d0465-0c7b-42f5-9de4-f1a125ecce96.png)

We will have to save our Production this way. After that, when we close our docker container and compose it up again, we will still have all of our progress saved locally (it is, of course, to be done after every change through the portal). To make it accessible to IRIS again we need to compile the exported files (by saving them, InterSystems addons take care of the rest).

## 5.4. Register components

In order to register the components we are creating in python to the production it is needed to use the `RegisterComponent` function from the `Grongier.PEX.Utils` module.

For this we advise you to use the build-in python console to add manually the component at first when you are working on the project.

You will find those commands in the `misc/register.py` file.<br>To use them you need to firstly create the component then you can start a terminal in VSCode ( it will be automatically in the container if you followed step [5.2.](#52-management-portal-and-vscode)) and enter :
```
/usr/irissys/bin/irispython
```
To launch an IrisPython console.

Then enter :
```
import iris
```

Now you can register your component using :
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bo","FileOperation","/irisdev/app/src/python/",1,"Python.FileOperation")
```
This line will register the class `FileOperation` that is coded inside the file `bo`, file situated in `/irisdev/app/src/python/` (which is the right path if you follow this course) using the name `Python.FileOperation` in the management portal.

It is to be noted that if you don't change to name of the file or the class, if a component was registered you can modify it on VSCode without the need to register it again. Just don't forget to restart it in the management portal.

# 6. Productions 

A **production** is the base of all our work on Iris, it must be seen as the shell of our [framework](#2-framework) that will hold the **services**, **processes** and **operations**.<br>
Everything in the production is going to inherit functions ; Those are the `on_init` function that resolve at the creation of an instance of this class and the `on_tear_down` function that resolve when the instance is killed.
This will be useful to set variables or close a used open file when writing.

We can now create our first production.<br>
For this, we will go through the [Interoperability] and [Configure] menus: 

![ProductionMenu](https://user-images.githubusercontent.com/77791586/164473827-ffa2b322-095a-46e3-8c8b-16d467a80485.png)

We then have to press [New], select the [Formation] package and chose a name for our production: 

![ProductionCreation](https://user-images.githubusercontent.com/77791586/164473884-5c7aec69-c45d-4062-bedc-2933e215da22.png)

Immediatly after creating our production, we will need to click on [Production Settings] just above the [Operations] section. In the right sidebar menu, we will have to activate [Testing Enabled] in the [Development and Debugging] part of the [Settings] tab (don't forget to press [Apply]).

![ProductionTesting](https://user-images.githubusercontent.com/77791586/164473965-47ab1ba4-85d5-46e3-9e15-64186b5a457e.png)

In this first production we will now add Business Operations.

# 7. Business Operations

A **Business Operation** (BO) is a specific operation that will enable us to send requests from IRIS to an external application / system. It can also be used to directly save in IRIS what we want.<br>
BO also have an `on_message` function that will be called everytime this instance receive a message from any source, this will allow us to receive information and send it, as seen in the framework, to an external client.

We will create those operations in local in VSCode, that is, in the `python/bo.py` file.<br>Saving this file will compile them in IRIS. 

For our first operations we will save the content of a message in the local database and write the same information locally in a .txt file.

We need to have a way of storing this message first. 

## 7.1. Creating our storage classes

We will use `dataclass` to hold information in our [messages](#72-creating-our-message-classes).

In our `python/obj.py` file we have: 
```python
from dataclasses import dataclass

@dataclass
class Formation:
    id:int = None
    nom:str = None
    salle:str = None

@dataclass
class Training:
    name:str = None
    room:str = None
```

The Formation class will be used as a Python object to read a csv and write in a texte file later on, while the Training class will be used as a way to interact with the Iris database.

## 7.2. Creating our message classes

These messages will contain a `Formation` object or a `Training` object, located in the `obj.py` file created in [7.1](#71-creating-our-storage-classes)

Note that messages, requests and responses all inherit from the `grongier.pex.Message` class.

In the `python/msg.py` file we have: 
```python
from dataclasses import dataclass
import grongier.pex.Message

from obj import Formation,Training

@dataclass
class FormationRequest(Message):
    formation:Formation = None

@dataclass
class TrainingIrisRequest(Message):
    training:Training = None
```

Again, the `FormationRequest` class will be used as a message to read a csv and write in a texte file later on, while the `TrainingIrisRequest` class will be used as a message to interact with the Iris database.

## 7.3. Creating our operations

Now that we have all the elements we need, we can create our operations.<br>
Note that any Business Operation inherit from the `grongier.pex.BusinessOperation` class.

In the `python/bo.py` file we have: 
```python
from grongier.pex import BusinessOperation
import os
import iris

from msg import TrainingIrisRequest,FormationRequest

class FileOperation(BusinessOperation):

    def on_init(self):
        if hasattr(self,'path'):
            os.chdir(self.path)
        else:
            os.chdir("/tmp")
        return None

    def write_formation(self, pRequest:FormationRequest):
        id = salle = nom = ""
        if (pRequest.formation is not None):
            id = str(pRequest.formation.id)
            salle = pRequest.formation.salle
            nom = pRequest.formation.nom
        line = id+" : "+salle+" : "+nom+"\n"
        filename = 'toto.csv'
        self.put_line(filename, line)
        return None

    def on_message(self, request):
        return None


    @staticmethod
    def put_line(filename,string):
        try:
            with open(filename, "a",encoding="utf-8",newline="") as outfile:
                outfile.write(string)
        except Exception as e:
            raise e


class IrisOperation(BusinessOperation):

    def insert_training(self, request:TrainingIrisRequest):
        sql = """
        INSERT INTO iris.training
        ( name, room )
        VALUES( ?, ? )
        """
        iris.sql.exec(sql,request.training.name,request.training.room)
        return None
        
    def on_message(self, request):
        return None
```

When one of the operation receive a message/request, it will automatically dispatch the message/request to the correct function depending of the type of message/request specified in the signature of each function.
If the type of the message/request is not handled, it will be forwarded to the `on_message` function.

As we can see, if the `FileOperation` receive a message of the type `msg.FormationRequest`, the information hold by the message will be written down on the `toto.csv` file.<br>Note that `Path` is already a parameter of the operation and you could make `filename` a variable with a base value of `toto.csv` that can be change directly onto the management portal by doing :
```python
    def on_init(self):
        if hasattr(self,'path'):
            os.chdir(self.path)
        else:
            os.chdir("/tmp")
        if not hasattr(self,'filename'):
            self.filename = 'toto.csv'
        return None
```
Then, we would call `self.filename` instead of coding it directly inside the operation.
<br><br><br>

As we can see, if the `IrisOperation` receive a message of the type `msg.TrainingIrisRequest`, the information hold by the message will be transformed into an SQL querry and executed by the `iris.sql.exec` IrisPython function. This method will save the message in the IRIS local database.

Don't forget to register your components :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bo","FileOperation","/irisdev/app/src/python/",1,"Python.FileOperation")
```

And:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bo","IrisOperation","/irisdev/app/src/python/",1,"Python.IrisOperation")
```

## 7.4. Adding the operations to the production

We now need to add these operations to the production. For this, we use the Management Portal. By pressing the [+] sign next to [Operations], we have access to the [Business Operation Wizard].<br>There, we chose the operation classes we just created in the scrolling menu. 

![OperationCreation](https://user-images.githubusercontent.com/77791586/164474068-49c7799c-c6a2-4e1e-8489-3788c50acb86.png)

## 7.5. Testing

Double clicking on the operation will enable us to activate it. After that, by selecting the operation and going in the [Actions] tabs in the right sidebar menu, we should be able to test the operation (if not see the production creation part to activate testings / you may need to start the production if stopped).

For IrisOperation it is to be noted that the table was created automatically.
The steps to create it and save it beetween container build :
Access the Iris DataBase using the access to the management portal and seek [System Explorer] then [SQL] then [Go].
Now you can enter in the [Execute Query] :
```
CREATE TABLE iris.training (
	name varchar(50) NULL,
	room varchar(50) NULL
)
```
Now it is possible to [save](#53-saving-progress) our table iris.training by exporting the `iris` folder using the Objectscript addon.
Now, even after rebuilding the container, the tabe will be saved.

By using the test function of our management portal, we will send the operation a message of the type we declared earlier. If all goes well, showing the visual trace will enable us to see what happened between the processes, services and operations. <br>Here, we can see the message being sent to the operation by the process, and the operation sending back a response (that is just an empty string).
You should get a result like this :
![IrisOperation](https://user-images.githubusercontent.com/77791586/164474137-f21b78f1-fbe6-493f-8f50-f2729f81295d.png)


<br><br><br>

For FileOperation it is to be noted that you must fill the Path in the `%settings` available on the Management Portal as follow ( and you can add in the settings the `Filename` if you have followed the `Filename` note from [7.3.](#73-creating-our-operations) ) :
![Settings for FileOperation](https://user-images.githubusercontent.com/77791586/164474207-f31805ff-b36c-49be-972a-dc8d32ce495c.png)

You should get a result like this :
![FileOperation](https://user-images.githubusercontent.com/77791586/164474286-0eaa6f27-e56f-4a87-b12a-9dab57c21506.png)


In order to see if our operations worked it is needed for us to acces the toto.csv file and the Iris DataBase to see the changes.<br>
To access the toto.csv you will need to open a terminal inside the container then type:
```
bash
```
```
cd /tmp
```
```
cat toto.csv
```

To access the Iris DataBase you will need to access the management portal and seek [System Explorer] then [SQL] then [Go].
Now you can enter in the [Execute Query] :
```
SELECT * FROM iris.training
```



# 8. Business Processes

**Business Processes** (BP) are the business logic of our production. They are used to process requests or relay those requests to other components of the production.<br>
BP also have an `on_request` function that will be called everytime this instance receive a request from any source, this will allow us to receive information and process it in anyway and disptach it to the right BO.

We will create those process in local in VSCode, that is, in the `python/bp.py` file.<br>Saving this file will compile them in IRIS. 


## 8.1. Simple BP

We now have to create a **Business Process** to process the information coming from our future services and dispatch it accordingly. We are going to create a simple BP that will call our operations.

Since our BP will only redirect information we will call it `Router` and it will be in the file `python/bp.py` like this :
```python
from grongier.pex import BusinessProcess

from msg import FormationRequest, TrainingIrisRequest
from obj import Training


class Router(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,FormationRequest):
            msg = TrainingIrisRequest()
            msg.training = Training()
            msg.training.name = request.formation.nom
            msg.training.room = request.formation.salle
            self.SendRequestSync('Python.FileOperation',request)
            self.SendRequestSync('Python.IrisOperation',msg)
        return None
```
The Router will receive a request of the type `FormationRequest` and will send a message of the type `TrainingIrisRequest` to the `IrisOperation` operation.
If the message/request is not an instance of the type we are looking for, we will just do nothing and not dispatch it.

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bp","Router","/irisdev/app/src/python/",1,"Python.Router")
```

## 8.2. Adding the process to the production

We now need to add the process to the production. For this, we use the Management Portal. By pressing the [+] sign next to [Processes], we have access to the [Business Process Wizard]. There, we chose the process class we just created in the scrolling menu. 

## 8.3. Testing

Double clicking on the process will enable us to activate it. After that, by selecting the process and going in the [Actions] tabs in the right sidebar menu, we should be able to test the process (if not see the production creation part to activate testings / you may need to start the production if stopped).

By doing so, we will send the process a message of the type `msg.FormationRequest`.
![RouterTest](https://user-images.githubusercontent.com/77791586/164474368-838fd740-0548-44e6-9bc0-4c6c056f0cd7.png)

If all goes well, showing the visual trace will enable us to see what happened between the process, services and processes. <br>Here, we can see the messages being sent to the operations by the process, and the operations sending back a response.
![RouterResults](https://user-images.githubusercontent.com/77791586/164474411-efdae647-5b8b-4790-8828-5e926c597fd1.png)

# 9. Business Service

**Business Service** (BS) are the ins of our production. They are used to gather information and send them to our routers.
BS also have an `on_process_input` function that often gather information in our framework, it can be called by multiple ways such as a REST API or an other service, or by the service itself to execute his code again.
BS also have a `get_adapter_type` function that allow us to allocate an adapter to the class, for example `Ens.InboundAdapter`that will make it so that the service will call his own `on_process_input`every 5 seconds.

We will create those services in local in VSCode, that is, in the `python/bs.py` file.<br>Saving this file will compile them in IRIS.

## 9.1. Simple BS

We now have to create a Business Service to read a CSV and send each line as a `msg.FormationRequest` to the router.

Since our BS will read a csv we will call it `ServiceCSV` and it will be in the file `python/bs.py` like this :
```python
from grongier.pex import BusinessService

from dataclass_csv import DataclassReader

from obj import Formation
from msg import FormationRequest

class ServiceCSV(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"
    
    def on_init(self):
        if hasattr(self,'path'):
            self.Path = self.path
        else:
            self.Path = '/irisdev/app/misc/'
        return None

    def on_process_input(self,request):
        filename='formation.csv'
        with open(self.Path+filename) as formation_csv:
            reader = DataclassReader(formation_csv, Formation,delimiter=";")
            for row in reader:
                msg = FormationRequest()
                msg.formation = row
                self.SendRequestSync('Python.Router',msg)
        return None
```
As we can see, the ServiceCSV gets an InboundAdapter that will allow it to function on it's own and to call on_process_input every 5 seconds ( parameter that can be changed in the basic settings of the settings of the service on the Management Portal)

Every 5 seconds, the service will open the `formation.csv` to read each line and create a `msg.FormationRequest` that will be send to the `Python.Router`.

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bs","ServiceCSV","/irisdev/app/src/python/",1,"Python.ServiceCSV")
```

## 9.2. Adding the service to the production

We now need to add the service to the production. For this, we use the Management Portal. By pressing the [+] sign next to [Services], we have access to the [Business service Wizard]. There, we chose the service class we just created in the scrolling menu. 

## 9.3. Testing

Double clicking on the process will enable us to activate it. As explained before, nothing more has to be done here since the service will start on his own every 5 seconds.
If all goes well, showing the visual trace will enable us to see what happened between the process, services and processes. Here, we can see the messages being sent to the process by the service, the messages to the operations by the process, and the operations sending back a response.
![ServiceCSVResults](https://user-images.githubusercontent.com/77791586/164474470-c77c4a06-0d8f-4ba9-972c-ce09b20fa54a.png)

# 10. Getting access to an extern database using JDBC

In this section, we will create an operation to save our objects in an extern database. We will be using the JDBC API, as well as the other docker container that we set up, with postgre on it. 

## 10.1. Prerequisites
In order to use postgre we need psycopg2 which is a python module allowing us to connect to the postegre database with a simple command.<br>
It was already done automatically but the steps are : access the inside of the docker container to install psycopg2 using pip3.<br>Once you are in the terminal enter :
```
pip3 install psycopg2-binary
```

Or add your module in the requirements.txt and rebuild the container.

## 10.2. Creating our new operation

Our new operation needs to be added after the two other one in the file `python/bo.py`.
Our new operation and the imports are as follows: 
````python
import psycopg2

class PostgresOperation(BusinessOperation):

    def on_init(self):
        if not hasattr(self,'filename'):
            self.filename = "/tmp/test.txt"
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

    def insert_training(self,request:FormationRequest):
        cursor = self.conn.cursor()
        sql = "INSERT INTO public.formation ( id,nom,salle ) VALUES ( %s , %s , %s )"
        cursor.execute(sql,(request.formation.id,request.formation.nom,request.formation.salle))
        return None
    
    def on_message(self,request):
        return None
````
It is to be noted that it is better if you put the `import psycopg2` at the beginning of the file with the other imports for clarity.
This operation is similar to the first one we created. When it will receive a message of the type `msg.FormationRequest`, it will use the psycopg module to execute SQL requests. Those requests will be sent to our postgre database.

As you can see here the connection is written directly into the code, to improve our code we could do as before for the other operations and make, `host`, `database` and the other connection information, variables with a base value of `db` and `DemoData` etc that can be change directly onto the management portal.<br>To do this we can change our `on_init` function by :
```python
    def on_init(self):
        if hasattr(self,'path'):
            os.chdir(self.path)
        if not hasattr(self,'host'):
          self.host = 'db'
        if not hasattr(self,'database'):
          self.database = 'DemoData'
        if not hasattr(self,'user'):
          self.user = 'DemoData'
        if not hasattr(self,'password'):
          self.password = 'DemoData'
        if not hasattr(self,'port'):
          self.port = '5432'

        self.conn = psycopg2.connect(
        host=self.host,
        database=self.database,
        user=self.user,
        password=self.password,
        port=self.port)

        self.conn.autocommit = True

        return None
```

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bo","PostgresOperation","/irisdev/app/src/python/",1,"Python.PostgresOperation")
```

## 10.3. Configuring the production

We now need to add the operation to the production. For this, we use the Management Portal. By pressing the [+] sign next to [Operations], we have access to the [Business Operation Wizard]. There, we chose the operation class we just created in the scrolling menu. 

Afterward, if you wish to change the connection, you can simply add in the %settings in [Python] in the [parameter] window of the operation the parameter you wish to change.
See the second image of [7.5. Testing](#75-testing) for more details.

## 10.4. Testing

When testing the visual trace should show a success: 


![JDBCTest](https://user-images.githubusercontent.com/77791586/164474520-8e355daf-77f0-4827-9c08-8b0c7ae4b18a.png)

We have successfully connected with an extern database. 

## 10.5. Exercise

As an exercise, it could be interesting to modify `bo.IrisOperation` so that it returns a boolean that will tell the `bp.Router` to call `bo.PostgresOperation` depending on the value of that boolean.

**Hint**: This can be done by changing the type of reponse bo.IrisOperation returns and by adding to that new type of message/response a new boolean property and using the `if` activity in our bp.Router.

## 10.6. Solution

First, we need to have a response from our bo.IrisOperation . We are going to create a new message after the other two, in the `python/msg.py`:
````python
@dataclass
class TrainingirisResponse(Message):
    bool:Boolean = None
````

Then, we change the response of bo.IrisOperation by that response, and set the value of its boolean randomly (or not).<br>In the `python/bo.py`you need to add two imports and change the IrisOperation class:
````python
import random
from msg import TrainingIrisResponse

class IrisOperation(BusinessOperation):

    def insert_training(self, request:TrainingIrisRequest):
        resp = TrainingIrisResponse()
        resp.bool = (random.random() < 0.5)
        sql = """
        INSERT INTO iris.training
        ( name, room )
        VALUES( ?, ? )
        """
        iris.sql.exec(sql,request.training.name,request.training.room)
        return resp
        
    def on_message(self, request):
        return None
````

We will now change our process `bp.Router` in `python/bp.py` , where we will make it so that if the response from the IrisOperation has a boolean equal to True it will call the PostgesOperation.
Here is the new code :
```python
class Router(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,FormationRequest):
            msg = TrainingIrisRequest()
            msg.training = Training()
            msg.training.name = request.formation.nom
            msg.training.room = request.formation.salle
            self.SendRequestSync('Python.FileOperation',request)
            form_iris_resp = self.SendRequestSync('Python.IrisOperation',msg)
            if form_iris_resp.bool:
                self.SendRequestSync('Python.PostgresOperation',request)
        return None
```

VERY IMPORTANT : we need to make sure we use **SendRequestSync** and not **SendRequestAsync** in the call of our operations, or else the activity will set off before receiving the boolean response.

In the visual trace, after testing, we should have approximately half of objects read in the csv saved also in the remote database.<br>
Note that to test you can just start the `bs.ServiceCSV` and it will automatically send request to the router that will then dispatch properly the requests.<br>
Also note that you must double click on a service and press reload or restart if you want your saved changes on VSCode to apply.

# 11. REST service

In this part, we will create and use a REST Service.

## 11.1. Prerequisites
In order to use Flask we will need to install flask which is a python module allowing us to easily create a REST service.
It was already done automatically but for information the steps are : access the inside of the docker container to install flask on iris python.
Once you are in the terminal enter :
```
pip3 install flask
```

Or add your module in the requirements.txt and rebuild the container.

## 11.2. Creating the service

To create a REST service, we will need a service that will link our API to our production, for this we create a new simple service in `python/bs.py` just after the `ServiceCSV` class.
```python
class FlaskService(BusinessService):

    def on_init(self):        
        if not hasattr(self,'Target'):
            self.Target = "Python.Router"        
        return None

    def on_process_input(self,request):
        return self.SendRequestSync(self.Target,request)
```
on_process_input this service will simply transfer the request to the Router.

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bs","FlaskService","/irisdev/app/src/python/",1,"Python.FlaskService")
```

To create a REST service, we will need Flask to create an API that will manage the `get` and `post` function:
We need to create a new file as `python/app.py`:
```python
from flask import Flask, jsonify, request, make_response
from grongier.pex import Director
import iris

from obj import Formation
from msg import FormationRequest


app = Flask(__name__)

# GET Infos
@app.route("/", methods=["GET"])
def get_info():
    info = {'version':'1.0.6'}
    return jsonify(info)

# GET all the formations
@app.route("/training/", methods=["GET"])
def get_all_training():
    payload = {}
    return jsonify(payload)

# POST a formation
@app.route("/training/", methods=["POST"])
def post_formation():
    payload = {} 
    formation = Formation(request.get_json()['id'],request.get_json()['nom'],request.get_json()['salle'])
    msg = FormationRequest(formation=formation)
    service = Director.CreateBusinessService("Python.FlaskService")
    response = service.dispatchProcessInput(msg)
    return jsonify(payload)

# GET formation with id
@app.route("/training/<int:id>", methods=["GET"])
def get_formation(id):
    payload = {}
    return jsonify(payload)

# PUT to update formation with id
@app.route("/training/<int:id>", methods=["PUT"])
def update_person(id):
    payload = {}
    return jsonify(payload)

# DELETE formation with id
@app.route("/training/<int:id>", methods=["DELETE"])
def delete_person(id):
    payload = {}  
    return jsonify(payload)

if __name__ == '__main__':
    app.run('0.0.0.0', port = "8081")
```

Note that the Flask API will use a Director to create an instance of our FlaskService from earlier and then send the right request.

We made the POST formation functional in the code above, if you wish, you can make the other functions in order to get/post the right information using all the things we have learned so far, however note that no solution will be provided for it.

## 11.3. Testing

Finally, we can test our service with any kind of REST client after having reloaded the Router service.

Using any REST service as RESTer for Mozilla, it is needed to fill the headers like this:
![RESTHeaders](https://user-images.githubusercontent.com/77791586/165522396-154a4ef4-535b-44d7-bcdd-a4bfd2f574d3.png)


The body like this:
![RESTBody](https://user-images.githubusercontent.com/77791586/165522641-b4e772e0-bad3-495e-9a1f-ffe3210053a9.png)

The authorization like this:
![RESTAuthorization](https://user-images.githubusercontent.com/77791586/165522730-bb89797a-0dd1-4691-b1e8-b7c491b53a6a.png)


Finally, the results should be something like this:
![RESTResults](https://user-images.githubusercontent.com/77791586/165522839-feec14c0-07fa-4d3f-a435-c9a06a544785.png)


# 12. Global exercise

Now that we are familliar with all the important concepts of the Iris DataPlatform and its [Framework](#2-framework) it is time to try ourselves on a global exercise that will make us create a new BS and BP, modify greatly our BO and also explore new concept in Python.

## 12.1. Instructions
Using this **endpoint** : `https://lucasenard.github.io/Data/patients.json` we have to automatically **get** information about `patients and their number of steps`.
Then, we must calculate the average number of steps per patient before writing it down on a csv file locally.

If needed, it is advised to seek guidance by rereading through the whole formation or the parts needed or by seeking help using the [hints](#122-hints) below.

Don't forget to [register your components](#54-register-components) to acces them on the management portal.

When everything is done and tested, or if the hints aren't enough to complete the exercise, the [solution](#123-solutions) step-by-step is present to walk us through the whole procedure.

## 12.2. Hints
In this part we can find hints to do the exercise, the [hints](#1221-hints) are an increasing guidance on how to accomplish different task.


### 12.2.1. bs
#### 12.2.1.1. Get information

To get the information from the endpoint it is advised to search for the `requests` module of python and use `json` and `json.dumps` to make it into str to send it in the bp

#### 12.2.1.2. Get information with requests

An online python website or any local python file can be used to use requests and print the output and it's type to go further and understand what we get.

#### 12.2.1.3. Get information with requests and using it

It is advised to create a new message type and object type to hold information and send it to a process to calculate the average.

#### 12.2.1.4. Get information solution

Solution on how to use request to get data and in our case, partially what to do with it.
```python
r = requests.get(https://lucasenard.github.io/Data/patients.json)
data = r.json()
for key,val in data.items():
    ...
```

Again, in an online python website or any local python file, it is possible to print key, val and their type to understand what can be done with them.<br>
It is advised to store `val` usign `json.dumps(val)` and then, after the SendRequest,when you are in the process, use `json.loads(request.patient.infos)`to get it ( if you have stored the informations of `val` into `patient.infos` )

### 12.2.2. bp
#### 12.2.2.1. Average and dict

`statistics` is a native library that can be used to do math.

#### 12.2.2.2. Average and dict hint

The native `map` function in python can allow you to seperate information within a list or a dict for example.

Don't forget to transform the result of `map` back to a list using the `list` native function.

#### 12.2.2.3. Average and dict with map

Using an online python website or any local python file it is possible to calculate average of a list of lists or a list of dict doing :
```python
l1 = [[0,5],[8,9],[5,10],[3,25]]
l2 = [["info",12],["bidule",9],[3,3],["patient1",90]]
l3 = [{"info1":"7","info2":0},{"info1":"15","info2":0},{"info1":"27","info2":0},{"info1":"7","info2":0}]

#avg of the first columns of the first list (0/8/5/3)
avg_l1_0 = statistics.mean(list(map(lambda x: x[0]),l1))

#avg of the second columns of the first list (5/9/10/25)
avg_l1_1 = statistics.mean(list(map(lambda x: x[1]),l1))

#avg of 12/9/3/90
avg_l2_1 = statistics.mean(list(map(lambda x: x[1]),l2))

#avg of 7/15/27/7
avg_l3_info1 = statistics.mean(list(map(lambda x: int(x["info1"])),l3))

print(avg_l1_0)
print(avg_l1_1)
print(avg_l2_1)
print(avg_l3_info1)
```

#### 12.2.2.4. Average and dict the answer

If your request hold a patient which as an atribute infos which is a json.dumps of a dict of date and number of steps, you can calculate his avergae number of steps using :
```python
statistics.mean(list(map(lambda x: int(x['steps']),json.loads(request.patient.infos))))
```
### 12.2.3. bo

It is advised to use something really similar to `bo.Fileoperation.WriteFormation`

Something like `bo.Fileoperation.WritePatient`

## 12.3. Solutions

### 12.3.1. obj & msg

In our `obj.py` we can add :
```python
@dataclass
class Patient:
    name:str = None
    avg:int = None
    infos = None
```

In our `msg.py` we can add :
```python
from obj import Formation,Training,Patient

@dataclass
class PatientRequest(Message):
    patient:Patient = None
```
We will hold the information in a single obj and we will put the str of the dict out of the get requests directly into the `infos` attribute.
The avg will be calculated in the process.

### 12.3.2. bs

In our `bs.py` we can add :
```python
import requests

class PatientService(BusinessService):

    def get_adapter_type():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"

    def on_init(self):
        if not hasattr(self,'target'):
            self.target = "Python.PatientProcess"

        if not hasattr(self,'ApiUrl'):
            self.api_url = "https://lucasenard.github.io/Data/patients.json"
        
        return None

    def on_process_input(self,request):
        r = requests.get(self.api_url)
        if r.status_code == 200:

            dat = r.json()

            for key,val in dat.items():

                patient = Patient()
                patient.name = key
                patient.infos = json.dumps(val)

                msg = PatientRequest()
                msg.patient = patient
                
                self.SendRequestSync(self.target,msg)

        return None
```
It is advised to make the target and the api url variables ( see on_init ).<br>
After the `requests.get`putting the information in the `r` variable, it is needed to extract the information in json, which will make `dat` a dict.<br>
Using dat.items it is possible to iterate on the patient and its info directly.<br>
We then create our object patient and put `val` into a string into the `patient.infos` variable using `json.dumps` that transform any json data to string.<br>
Then, we create the request `msg` which is a `msg.PatientRequest` to call our process. 

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bs","PatientService","/irisdev/app/src/python/",1,"Python.PatientService")
```

### 12.3.3. bp
In our `bp.py` we can add :
```python
import statistic

class PatientProcess(BusinessProcess):

    def on_request(self, request):
        if isinstance(request,PatientRequest):
            request.patient.avg = statistics.mean(list(map(lambda x: int(x['steps']),json.loads(request.patient.infos))))
            self.SendRequestSync('Python.FileOperation',request)

        return None
```
We take the request we just got, and if it is a `PatientRequest` we calculate the mean of the steps and we send it to our FileOperation.
This fills the `avg` variable of our patient with the right information ( see the hint on the bp for more information )

Don't forget to register your component :
Following [5.4.](#54-register-components) and using:
```
iris.cls("Grongier.PEX.Utils").RegisterComponent("bp","PatientProcess","/irisdev/app/src/python/",1,"Python.PatientProcess")
```

### 12.3.4. bo
In our `bo.py` we can add, inside the class `FileOperation` :
```python
    def write_patient(self, request:PatientRequest):
        name = ""
        avg = 0

        if (request.patient is not None):
            name = request.patient.name
            avg = request.patient.avg

        line = name + " avg nb steps : " + str(avg)

        filename = 'Patients.csv'

        self.put_line(filename, line)

        return None
```

As explained before, it is not needed to register `FileOperation` again since we did it already before.

## 12.4. Testing

Now we can head towards the management portal and do as before.
Remember that our new service will execute automatically since we added an InboundAdapter to it.

The same way we checked for the `toto.csv` we can check the `Patients.csv`

## 12.5. Conclusion of the global exercise

Through this exercise it is possible to learn and understand the creation of messages, services, processes and operation.<br>
We discovered how to fecth information in Python and how to execute simple task on our data.

In the github, a `solution` branch is available with everything already completed.

# 13. Conclusion

Through this formation, we have created a fully fonctional production using only IrisPython that is able to read lines from a csv file and save the read data into a local txt, the IRIS database and an extern database using JDBC. <br>We also added a REST service in order to use the POST verb to save new objects.

We have discovered the main elements of InterSystems' interoperability Framework.

We have done so using docker, vscode and InterSystems' IRIS Management Portal.
