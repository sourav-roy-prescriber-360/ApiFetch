import pandas as pd
import requests
import json
import numpy as np
import csv
from datetime import date

data=pd.read_csv('npiid_Data_List1.csv')
data=data.replace(np.nan, '', regex=True)
df=pd.DataFrame()

for fn in data['fullname']:
    load={'terms':fn}
    response = requests.get("https://clinicaltables.nlm.nih.gov/api/npi_idv/v3/search?sf=name.full&df=name.full,NPI,provider_type,addr_practice.full", params=load)
    print(response.url)
    dfjson = json.loads(response.text)
    for hcp in dfjson[3]:
        df = df.append(pd.DataFrame(np.array(hcp).reshape(-1,len(hcp)),columns=['Full Name','NPI','Provider Type','Address']),ignore_index=True)

df.to_csv(r'missing_npi_'+str(date.today())+'.csv',index=False,header=True)