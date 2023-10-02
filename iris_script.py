import glob
import iris
import pandas as pd
from sqlalchemy import create_engine
from grongier.pex import Utils

# switch namespace to the %SYS namespace
iris.system.Process.SetNamespace("%SYS")

# set credentials to not expire
iris.cls('Security.Users').UnExpireUserPasswords("*")

# switch namespace to IRISAPP built by merge.cpf
iris.system.Process.SetNamespace("IRISAPP")

# load demo data
engine = create_engine('iris+emb:///')
# list all csv files in the demo data folder
for files in glob.glob('/irisdev/app/misc/*.csv'):
    # get the file name without the extension
    table_name = 'training'
    # load the csv file into a pandas dataframe
    df = pd.read_csv(files)
    # write the dataframe to IRIS
    df.to_sql(table_name, engine, if_exists='replace', index=False, schema='iris')

# load interop demo
Utils.migrate('/irisdev/app/settings.py')