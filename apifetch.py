import pandas as pd
import requests
import json
import numpy as np
import csv
from datetime import date

data=pd.read_csv('npiid_Data_List1.csv')
data=data.head()
data=data.replace(np.nan, ' ', regex=True)
df=pd.DataFrame()

for fn,zipval in zip(data['fullname'],data['p360_primaryzip']):
    if(zipval!=' '):
        zipval=int(zipval)
    name=fn+' '+str(zipval)
    print(name)
    load={'terms':name}
    response = requests.get("https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?maxList=500&df=name.full,NPI,provider_type,addr_practice.full,addr_practice.zip", params=load)
    dfjson = json.loads(response.text)
    for hcp in dfjson[3]:
        print(hcp)
        df = df.append(pd.DataFrame(np.array(hcp).reshape(-1,len(hcp)),columns=['Full Name','NPI','Provider Type','Address','zip']),ignore_index=True)

df.to_csv(r'missing_npi_'+str(date.today())+'.csv',index=False,header=True)