import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline
import matplotlib
matplotlib.rcParams["figure.figsize"]=(20,10)

df1 = pd.read_csv("../../data/raw/Bengaluru_House_Data.csv")
df1.head()

df1.shape
# Get the totals
df1.groupby('area_type')["area_type"].agg('count')

# droping some columns
df2 =df1.drop(["area_type","society","balcony","availability"], axis="columns")

# check null values on the database
df2.isnull().sum()

# given that the na value are samll drop the value
df3= df2.dropna()
df3.isnull().sum()

# checking for unique values in a column
df3["size"].unique()

# make the size to be unique
# The code split the number from string and change integer

df3['bhk'] =df3["size"].apply(lambda x: int(x.split(' ')[0]))
df3['bhk'].head()

# confirm the changes made
df3["bhk"].unique()

# queriying data based on the creteria
df3[df3.bhk> 20]

# Converting  a range of values in a column to unique values
df3['total_sqft'].unique()

def is_float(x):
    try:
        float(x)
    except:
        return False
    return True

df3[~df3["total_sqft"].apply(is_float)]

# create a function that return mean range values
def convert_sqrf_to_num(x):
    tokens = x.split('-')
    if len(tokens)==2:
        return (float(tokens[0])+ float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None
    

# Testing the function 
convert_sqrf_to_num("3067 - 8156")

#copy the dataset 
df4 =df3.copy()
df4["total_sqft"] =df4["total_sqft"].applya(convert_sqrf_to_num)
df4.head()

df4.loc[30]

# Copy and create another data frame that
df5 =df4.copy()
df5['price_per_sqrf']=df5['price']* 100000/df5['total_sqft']
df5.head()

# check the unique number of location
len(df5.location.unique())

#removing the leading space
df5.location =df5.location.apply(lambda x: x.strip())

# counting locations
location_stats=df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_stats

# number of location which has less than or equal to data points.
len(location_stats[location_stats<=10])

location_stats_less_than_10=location_stats[location_stats<=10]
location_stats_less_than_10

df5.location =df5.location.apply(lambda x : 'other' if x in location_stats_less_than_10 else x)