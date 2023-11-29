 # 1. **Interoperability IRIS Python Formation**

 The goal of this formation is to learn InterSystems' interoperability framework using python, and particularly the use of: 
* Productions
* Messages
* Business Operations
* Adapters
* Business Processes
* Business Services
* REST Services and Operations


**TABLE OF CONTENTS:**

- [1. **Interoperability IRIS Python Formation**](#1-interoperability-iris-python-formation)
- [2. Framework](#2-framework)
- [3. Adapting the framework](#3-adapting-the-framework)
- [4. Prerequisites](#4-prerequisites)
- [5. Setting up](#5-setting-up)
  - [5.1. Docker containers](#51-docker-containers)
  - [5.2 Virtual Environnement](#52-virtual-environnement)
- [6. The actual training](#6-the-actual-training)
  - [6.1. Warm up](#61-warm-up)
    - [6.1.1. Create a Business Operation](#611-create-a-business-operation)
    - [6.1.2. Import this Business Operation in the framework](#612-import-this-business-operation-in-the-framework)
    - [6.1.3. Run the production](#613-run-the-production)
    - [6.1.4. Bonus : Create a message](#614-bonus--create-a-message)
    - [6.1.5. Bonus : Use the message in the business operation](#615-bonus--use-the-message-in-the-business-operation)
  - [Part 1 : Our first pipeline](#part-1--our-first-pipeline)
    - [Objectives](#objectives)
    - [Create a Message](#create-a-message)
    - [Create a Business Operation](#create-a-business-operation)
    - [Create a Business Service](#create-a-business-service)
    - [Discover the UI](#discover-the-ui)
    - [Add a component to the production](#add-a-component-to-the-production)

# 2. Framework

This is the IRIS Framework.

![FrameworkFull](https://raw.githubusercontent.com/thewophile-beep/formation-template/master/misc/img/FrameworkFull.png)

The components inside of IRIS represent a production. Inbound adapters and outbound adapters enable us to use different kind of format as input and output for our database. <br>The composite applications will give us access to the production through external applications like REST services.

The arrows between them all of this components are **messages**. They can be requests or responses.

# 3. Adapting the framework

In our case, we will read lines from a csv file and save it into the IRIS database and in a .txt file. 

We will then add an operation that will enable us to save objects in an extern database too, using a db-api. This database will be located in a docker container, using Postgres.

Finally, we will see how to use composite applications to insert new objects in our database or to consult this database (in our case, through a REST service).

The framework adapted to our purpose gives us:

![FrameworkAdapted](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/Main_Diagram.drawio.png)


# 4. Prerequisites

For this formation, you'll need:
* VSCode: https://code.visualstudio.com/
* The InterSystems addons suite for vscode: https://intersystems-community.github.io/vscode-objectscript/installation/
* Docker: https://docs.docker.com/get-docker/
* The docker addon for VSCode.
* Automatically done : [Postgres requisites](#101-prerequisites)
* Automatically done : [Flask requisites](#111-prerequisites)

# 5. Setting up 

## 5.1. Docker containers

First, we will need to create a docker container for IRIS and one for Postgres.

For this training everything is already done, just run the following command in your terminal:

```bash
$ docker-compose up -d
```

💡 FYI : the root folder of this projet is mounted in the IRIS container in the /irisdev/app folder.

## 5.2 Virtual Environnement

We will need to create a virtual environnement for our application.

To create a virtual environnement, run the following command in your terminal:

```bash
$ python3 -m venv .venv
```

Then, to activate it, run the following command in your terminal:

```bash
$ source .venv/bin/activate
```

To install the requirements, run the following command in your terminal:

```bash
$ pip install -r requirements.txt
```

# 6. The actual training

Now that everything is set up, we can start the training.

We will start by a warm up, that will enable us to get familiar with the framework.

Then we will see how to create a production, and how to add operations to it.

Finally, we will see how to create a business process and a business service.

Bonus : we will see how to use a db-api to access an extern database, and how to create a REST service.

## 6.1. Warm up

Ok, let's start 🚀.

We gonna start with the usual "Hello World" program.

### 6.1.1. Create a Business Operation

For this, we will create an `BusinessOperation` that will take a message as input and will return a message as output. In between, it will just print "Hello World" in the logs.

To do this, let's create a new folder in the `src` folder, named `hello_world`.

```bash
$ mkdir src/hello_world
```

In this folder, create a new file named `bo.py`.

This file will contain the code of our business operation.

```python
from grongier.pex import BusinessOperation

class MyBo(BusinessOperation):
    def on_message(self, request):
        self.log_info("Hello World")
```

Let's explain this code.

First, we import the `BusinessOperation` class from the `grongier.pex` module.

Then, we create a class named `MyBo` that inherits from `BusinessOperation`.

Finally, we override the `on_message` method. This method will be called when a message is received by the business operation.

### 6.1.2. Import this Business Operation in the framework

Now, we need to add this business operation to what we call a production.

To do this, we will create a new file in the `src` folder, named `settings.py`.

⚠️ Gotcha : in the `src` folder, not in the `src/hello_world` folder.

Every project starts at it's root folder by a file named `settings.py`. 

This file contains two main settings:

- `CLASSES` : it contains the classes that will be used in the project.
- `PRODUCTIONS` : it contains the name of the production that will be used in the project.

```python
from hello_world.bo import MyBo

CLASSES = {
    "MyIRIS.MyBo": MyBo
}

PRODUCTIONS = [
        {
            'MyIRIS.Production': {
                "@TestingEnabled": "true",
                "Item": [
                    {
                        "@Name": "Instance.Of.MyBo",
                        "@ClassName": "MyIRIS.MyBo",
                    }
                ]
            }
        } 
    ]
```

In this file, we import our `MyBo` class named in iris `MyIRIS.MyBo`, and we add it to the `CLASSES` dictionnary.

Then, we add a new production to the `PRODUCTIONS` list. This production will contain our `MyBo` class instance named `Instance.Of.MyBo`.

### 6.1.3. Run the production

Now, we can run our production.

To do this, we will use the `iop` command. `iop` stands for Interoperability On Python (name of the framework).

⚠️ As the code will be executed in the IRIS container, we need to run this command in the IRIS container.

💡 TIP : every command line prefixed by a `$` must be run in your terminal. Every command line prefixed by a `%` must be run in the IRIS container.

To do this, run the following command in your terminal:

```bash
$ docker-compose exec iris bash
```

Then, run the following command in your terminal:

```bash
% iop --migrate /irisdev/app/src/settings.py
```

This command will `migrate` the code to IRIS.

Now, we can run the production.

To do this, run the following command in your terminal:

```bash
% iop --start MyIRIS.Production --detach
```

This command will start the production in the background.

Now, we can send a test message to our business operation.

To do this, run the following command in your terminal:

```bash
% iop --test Instance.Of.MyBo 
```

Check the logs of the production to see the result.

To do this, run the following command in your terminal:

```bash
% iop --log
```

💡 TIP : to exit logs, press `ctrl + c`.

Great, congratulations 🎉. You have finished the warm up.

### 6.1.4. Bonus : Create a message

Now, we will create a message that will be used by our business operation.

To do this, create a new file in the `src/hello_world` folder, named `msg.py`.

This file will contain the code of our message.

```python
from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class MyMsg(Message):
    value: str = ''
```

This simple message contains a `value` attribute that is a string.

We will be able to use this message in our business operation as input and output.

### 6.1.5. Bonus : Use the message in the business operation

Now, we will use this message in our business operation.

To do this, we will modify the `bo.py` file.

```python
from hello_world.msg import MyMsg
from grongier.pex import BusinessOperation

class MyBo(BusinessOperation):
    def on_message(self, request):
        self.log_info("Hello World")
        response = MyMsg()
        response.value = "Hello World"
        return response
```

First, we import our message.

Then, we modify the `on_message` method to return a message.

Finally, we create a new message and we return it.

Now, we can test our business operation.

First we need to restart the production to take into account the changes we made.

To do this, run the following command in your terminal:

```bash
% iop --restart
```

Then, we can send a test message to our business operation.

To do this, run the following command in your terminal:

```bash
% iop --test Instance.Of.MyBo 
```

output:

```bash
hello_world.msg.MyMsg : {"value": "Hello World"}
```

Good job 👍. We have a string representation of our output message.

Let's try to make it variable.

To do this, we will modify the `bo.py` file.

```python
from hello_world.msg import MyMsg
from grongier.pex import BusinessOperation

class MyBo(BusinessOperation):
    def on_message(self, request):
        self.log_info("Hello World")
        response = MyMsg()
        response.value = "Hello World"
        return response

    def on_my_msg(self, request: MyMsg):
        self.log_info("Hello World")
        response = MyMsg()
        response.value = f"Hello World {request.value}"
        return response
```

What we did here is to add a new method named `on_my_msg` that takes a `MyMsg` as input and returns a `MyMsg` as output.

Our business operation will now have two methods that can be called:
- `on_message` : takes **any** message as input and returns a `MyMsg` as output.
- `on_my_msg` : takes **only** `MyMsg` as input and returns a `MyMsg` as output.

The business operation is smart enough to know which method to call depending on the input message.

Now, we can test our business operation.

First we need to restart the production to take into account the changes we made.

To do this, run the following command in your terminal:

```bash
% iop --restart
```

Then, we can send a test message to our business operation.

To do this, run the following command in your terminal:

```bash
% iop --test Instance.Of.MyBo --classname hello_world.msg.MyMsg --body '{"value": "of IRIS !!!"}'
```

output:

```bash
hello_world.msg.MyMsg : {"value": "Hello World of IRIS !!!"}
```

Great, we have a variable output message.

Now it's time to get serious 🔥.

## Part 1 : Our first pipeline

Now, we will create a pipeline that will read lines from a csv file and save it into the IRIS database and in a .txt file.

![Pipeline](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/Main_Diagram_part1.drawio.png)

To do this, we will create a new folder in the `src` folder, named `training`.

```bash
$ mkdir src/training
```

### Objectives

The objectives of this part are:

- Create a pipeline that will read lines from a csv file and save it into the IRIS database and in a .txt file.

The format of the csv file is the following:

```csv
id,nom,salle
1,Formation IRIS,Paris
2,Formation IRIS,Lyon
```

### Create a Message

A good habit when creating a pipeline is to start by creating the messages that will be used in the pipeline.

To do this, we will create a new file in the `src/training` folder, named `msg.py`.

This file will contain the code of our messages.

```python
from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class FormationRequest(Message):
    id: int = 0
    nom: str = ''
    salle: str = ''
```

This message contains three attributes:
- `id` : an integer
- `nom` : a string
- `salle` : a string

We will use this message to save the data in a .txt file.

So, we need to create the Business Operation that will save the data in a .txt file.

### Create a Business Operation

To do this, we will create a new file in the `src/training` folder, named `bo.py`.

This file will contain the code of our business operation.

```python
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
            self.logger.info(f'FormationRequest {request.id} saved in {self.filename}')

```

Let's explain this code.

First, we import our message.

Then, we create a class named `SaveInTxtBo` that inherits from `BusinessOperation`.

Then, we override the `on_init` method. This method will be called when the business operation is initialized.

In this method, we check if the instance of `SaveInTxtBo` has a `filename` attribute. If not, we set it to `formation.txt` as default value.

Then, we check if the instance of `SaveInTxtBo` has a `path` attribute. If not, we set it to `/irisdev/app/data/` as default value.

Finally, we open the file in append mode.

Then, we create the `on_formation_request` method. This method will be called when a `FormationRequest` message is received by the business operation.

In this method, we log the data received.

Then, we write the data in the file.

Now, we can add this business operation to our production.

To do this, we will modify the `src/settings.py` file.

```python
from training.bo import SaveInTxtBo
from hello_world.bo import MyBo # We import the MyBo class from the hello_world project

CLASSES = {
    "MyIRIS.MyBo": MyBo, # We add the MyBo from the hello_world project
    "MyIRIS.SaveInTxtBo": SaveInTxtBo
}

PRODUCTIONS = [
        {
            'MyIRIS.Production': {
                "@TestingEnabled": "true",
                "Item": [
                    {
                        "@Name": "Instance.Of.MyBo", # Item that has been added
                        "@ClassName": "MyIRIS.MyBo", # previously from the hello_world project
                    },
                    {
                        "@Name": "Instance.Of.SaveInTxtBo",
                        "@ClassName": "MyIRIS.SaveInTxtBo",
                    }
                ]
            }
        } 
    ]
```

Let's migrate the code to IRIS.

To do this, run the following command in your terminal:

```bash
% iop --migrate /irisdev/app/src/settings.py
```

Now, we can run the production.

To do this, run the following command in your terminal:

```bash
% iop --restart
```

Now, we can send a test message to our business operation.

To do this, run the following command in your terminal:

```bash
% iop --test Instance.Of.SaveInTxtBo --classname training.msg.FormationRequest --body '{"id": 1, "nom": "Formation IRIS", "salle": "Paris"}'
```

Check the result in the `data/formation.txt` file.

To do this, run the following command in your terminal:

```bash
$ cat data/formation.txt
```

Ok, now last but not least, we need to create the service that will read the csv file and send the data to our business operation.

### Create a Business Service

To do this, we will create a new file in the `src/training` folder, named `bs.py`.

This file will contain the code of our business service.

```python
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
                self.log_info(f'FormationRequest {msg.id} sent to Instance.Of.SaveInTxtBo')
```

Let's explain this code.

First, we import our message.

Then, we create a class named `ReadCsvBs` that inherits from `BusinessService`.

Then, we override the `get_adapter_type` method. This method will be called when the business service is initialized.

In this method, we return the type of the adapter that will be used by the business service. In our case, it will be an `Ens.InboundAdapter`.

Then, we override the `on_init` method. This method will be called when the business service is initialized.

In this method, we check if the instance of `ReadCsvBs` has a `filename` attribute. If not, we set it to `formation.csv` as default value.

Then, we check if the instance of `ReadCsvBs` has a `path` attribute. If not, we set it to `/irisdev/app/data/` as default value.

Finally, we check if the instance of `ReadCsvBs` has a `target` attribute. If not, we set it to `Instance.Of.SaveInTxtBo` as default value.

Then, we override the `on_process_input` method. This method will be called when a message is received by the business service.

In this method, we open the csv file.

Then, we create a csv reader.

Then, we iterate over the rows of the csv file.

For each row, we create a `FormationRequest` message.

Then, we set the attributes of the message.

Finally, we send the message to the business operation.

Now, we can add this business service to our production.

### Discover the UI

For the first time, we will use the UI to do this.

The UI gives us a visual representation of the production.

![UI](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/UI.jpg)

To access the UI, go to http://localhost:52775/csp/irisapp/EnsPortal.ProductionConfig.zen?$NAMESPACE=IRISAPP

You can even have a visual representation of the messages.

![UI](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/MessageView.jpg)

To access the message view, go to http://localhost:52775/csp/irisapp/EnsPortal.MessageViewer.zen

Default login and password are `SuperUser` and `SYS`.

### Add a component to the production

We still have to register our business service class to iris.

For this, we will modify the `src/settings.py` file.

```python
from training.bs import ReadCsvBs
from training.bo import SaveInTxtBo
from hello_world.bo import MyBo

CLASSES = {
    "MyIRIS.MyBo": MyBo,
    "MyIRIS.SaveInTxtBo": SaveInTxtBo,
    "MyIRIS.ReadCsvBs": ReadCsvBs
}

# No need to add the business service to the production
# We will add it directly in the UI
PRODUCTIONS = [
        {
            'MyIRIS.Production': {
                "@TestingEnabled": "true",
                "Item": [
                    {
                        "@Name": "Instance.Of.MyBo",
                        "@ClassName": "MyIRIS.MyBo",
                    },
                    {
                        "@Name": "Instance.Of.SaveInTxtBo",
                        "@ClassName": "MyIRIS.SaveInTxtBo",
                    }
                ]
            }
        } 
    ]
```

Migrate the code to IRIS.

To do this, run the following command in your terminal:

```bash
% iop --migrate /irisdev/app/src/settings.py
```

Now let's add the business service to the production.

To do this, go to the UI.

http://localhost:52775/csp/irisapp/EnsPortal.ProductionConfig.zen?$NAMESPACE=IRISAPP

Then, click on the `+` button next to the `Business Services` label.

![AddBS](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/AddBS.jpg)

Then, select the `MyIRIS.ReadCsvBs` class.

![SelectBS](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/SelectBS.jpg)

Then, click on the `Ok` button.

Now, we can even see the messages in the UI.

![MessageView](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/ProdMessage.jpg)

If we want to export the configuration of the production, we can do it with the `iop` command.

To do this, run the following command in your terminal:

```bash
% iop --export MyIRIS.Production
```

This will export the configuration of the production that you can copy paste in the `src/settings.py` file.

Congratulations 🎉. You have created your first pipeline.