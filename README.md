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

In this file, we import our `MyBo` class named in iris `IRIS.MyBo`, and we add it to the `CLASSES` dictionnary.

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