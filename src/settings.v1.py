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