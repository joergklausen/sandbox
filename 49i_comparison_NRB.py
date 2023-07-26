# %%
import os
import re
import requests
import polars as pl
import io
import json
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

### Get data ###
# %%
## read file(s) (49i_2)
# NB: Polars does not provide an import for fixed-width-files (yet), so we 
# convert to .csv first. 
with open("data\\49i 071723 1419.dat",'r') as dat, open("data\\49i 071723 1419.csv",'w') as csv:
    csv.writelines(re.sub(" +", ",", s) for s in dat.readlines())

# headers = ['Time', 'Date', 'Flags', 'o3', 'hio3', 'cellai', 'cellbi', 'bncht', 'lmpt', 'o3lt', 'flowa', 'flowb', 'pres']
df = pl.read_csv("data\\49i 071723 1419.csv", comment_char=";")

with open("data\\49i 072123 1631.dat",'r') as dat, open("data\\49i 072123 1631.csv",'w') as csv:
    csv.writelines(re.sub(" +", ",", s) for s in dat.readlines())
df1 = pl.read_csv("data\\49i 072123 1631.csv", comment_char=";")

with open("data\\49i 072423 1559.dat",'r') as dat, open("data\\49i 072423 1559.csv",'w') as csv:
    csv.writelines(re.sub(" +", ",", s) for s in dat.readlines())
df2 = pl.read_csv("data\\49i 072423 1559.csv", comment_char=";")

# %%
# concatenate data, remove duplicate rows (=maintain unique rows)
df = pl.concat(items=[df, df1, df2])
del(df1)
del(df2)
# create proper dtm
df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%m-%d-%y"))
df = df.with_columns(pl.col("Time").str.strptime(pl.Time, format="%H:%M"))
df = df.with_columns(pl.col("Date").dt.combine(pl.col("Time")).alias("dtm"))

plt.scatter(df.select("dtm"), df.select("o3"))

# %%
## load ozone data from DWH (49i)
API_TOKEN = open(file="api-token", mode="r").read()
auth_url='https://service.meteoswiss.ch/auth/realms/meteoswiss.ch/protocol/openid-connect/token'
auth_data = (('grant_type', 'refresh_token'), ('client_id', 'api-token'), ('refresh_token', API_TOKEN))
# using requests
res = requests.post(url=auth_url, data=auth_data)
auth_header = 'Bearer ' + json.loads(res.text)['access_token']

jretrieve_base_url = 'https://service.meteoswiss.ch/jretrieve/api/v1'
jretrieve_url = jretrieve_base_url + '/surface/nat_abbr?delimiter=,&placeholder=None&locationIds=KENAI&date=20230710100100-20230724130700&parameterShortNames=itosurr0&measCatNr=1'
res = requests.get(url=jretrieve_url, headers={'Authorization': auth_header})
df1 = pl.read_csv(io.StringIO(res.text), null_values='None', dtypes=[pl.Int64, pl.Utf8, pl.Float64])
df1.drop_in_place("station")
df1.columns = ["dtm", "o3_1"]
df1 = df1.with_columns(pl.col("dtm").str.strptime(pl.Datetime, format="%Y%m%d%H%M%S"))

### select valid data and plot ###
# %%
df_valid = df.filter(pl.col("Flags").is_in(["c104000"]) & (pl.col("o3") > 1) & (pl.col("o3") < 70))
fig, ax = plt.subplots()
ax.plot(df.select("dtm"), df.select("o3"), ".k")
ax.plot(df_valid.select("dtm"), df_valid.select("o3"), ".r")

df1_valid = df1.filter((pl.col("o3_1") > 1) & (pl.col("o3_1") < 70))
fig, ax = plt.subplots()
ax.plot(df1.select("dtm"), df1.select("o3_1"), ".k")
ax.plot(df1_valid.select("dtm"), df1_valid.select("o3_1"), ".g")

### aggregate data to 10' ###
# %%
df_10m = df_valid.select(["dtm", "o3"]).sort("dtm")
df_10m = df_10m.groupby_dynamic("dtm", every="10m").agg(pl.col("o3").mean())

df1_10m = df1_valid.select(["dtm", "o3_1"]).sort("dtm")
df1_10m = df1_10m.groupby_dynamic("dtm", every="10m").agg(pl.col("o3_1").mean())

fig, ax = plt.subplots()
fig.suptitle("10' ozone at NRB")
fig.supxlabel("Date")
fig.supylabel("ozone (ppb)")
ax.plot(df_10m.select("dtm"), df_10m.select("o3"), ".r", label="49i_2")
ax.plot(df1_10m.select("dtm"), df1_10m.select("o3_1"), ".g", label="49i")
ax.legend()


### correlate instruments ####
# %%
df2 = df_10m.join(df1_10m, on="dtm")
fig, ax = plt.subplots()
fig.suptitle("10' ozone at NRB")
fig.supxlabel("49i_2 ozone (ppb)")
fig.supylabel("49i ozone (ppb)")
ax.plot(df2.select("o3"), df2.select("o3_1"), '.b', label='49i vs 49i_2')
ax.plot(range(50), range(50), 'r-', label='1:1')
ax.legend()

# %%
model = LinearRegression().fit(df2.select("o3"), df2.select("o3_1"))
r2 = model.score(df2.select("o3"), df2.select("o3_1"))
a = model.intercept_
b = model.coef_

print(f"<49i> = {b} * <49i_2> + {a}; r2={r2}")
# %%
