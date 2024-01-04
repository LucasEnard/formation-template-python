from training.bs import ReadCsvBs
from training.bo import SaveInTxtBo
from hello_world.bo import MyBo # We import the MyBo class from the hello_world project

CLASSES = {
    "MyIRIS.MyBo": MyBo, # We add the MyBo from the hello_world project
    "MyIRIS.SaveInTxtBo": SaveInTxtBo,
    "MyIRIS.ReadCsvBs": ReadCsvBs
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
                    },
                    {
                        "@Name": "Instance.Of.ReadCsvBs",
                        "@ClassName": "MyIRIS.ReadCsvBs",
                    }
                ]
            }
        } 
    ]