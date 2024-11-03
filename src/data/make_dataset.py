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
df4["total_sqft"] =df4["total_sqft"].apply(convert_sqrf_to_num)
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
df5.head()

# Outliers detection
df5[df5.total_sqft / df5.bhk < 300].head()

df5.shape

df6=df5[~(df5.total_sqft / df5.bhk < 300)]
df6.shape
df6.head()
df6.price_per_sqrf.describe()

def remove_pps_outliers(df):
    df_out =pd.DataFrame()
    for key, subdf in df.groupby("location"):
        m = np.mean(subdf.price_per_sqrf)
        st=np.std(subdf.price_per_sqrf)
        reduced_df=subdf[(subdf.price_per_sqrf>(m-st)) & (subdf.price_per_sqrf<=(m+st))]
        df_out=pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out

df7 =remove_pps_outliers(df6)
df7.shape


def plot_scatter_chart(df, location):
    bhk2 = df[(df.location == location) & (df.bhk == 2)]
    bhk3 = df[(df.location == location) & (df.bhk == 3)]
    
    matplotlib.rcParams['figure.figsize'] = (15, 10)
    plt.scatter(bhk2.total_sqft, bhk2.price, color='blue', label="2 BHK", s=50)
    plt.scatter(bhk3.total_sqft, bhk3.price, marker='+', color='green', label="3 BHK", s=50)
    plt.xlabel('Total Square Feet Area')
    plt.ylabel("Price per Square Feet")
    plt.title(location)
    plt.legend()
    plt.show()

# Call the function with a valid location
plot_scatter_chart(df7, 'Rajaji Nagar')

def remove_bhk_outliers(df):
    exclude_indices=np.array([])
    for location, location_df in df.groupby('location'):
        bhk_stats ={}
        for bhk, bhk_df in location_df.groupby('bhk'):
            bhk_stats[bhk]={
                "mean": np.mean(bhk_df.price_per_sqrf),
                "std": np.std(bhk_df.price_per_sqrf),
                "count": bhk_df.shape[0]
            }
        for bhk,bhk_df in location_df.groupby('bhk'):
            stats =bhk_stats.get(bhk-1)
            if stats and stats['count']>5:
                exclude_indices=np.append(exclude_indices,bhk_df[bhk_df.price_per_sqrf<(stats['mean'])].index.values)
    return df.drop(exclude_indices,axis='index')

df8 = remove_bhk_outliers(df7)
df8.shape
plot_scatter_chart(df8, 'Rajaji Nagar')

import matplotlib
matplotlib.rcParams["figure.figsize"]=(20,30)
plt.hist(df8.price_per_sqrf,rwidth=0.80)
plt.xlabel("price per sqaure Feet")
plt.ylabel('count')

df8.bath.unique()
df8[df8.bath>10]

plt.hist(df8.bath,rwidth=0.8)
plt.xlabel("Number of bathrooms")
plt.ylabel("count")
df8.shape
df9=df8
df9.shape()
#df8[df8.bath>df8.bhk+2]
df9 =df8[df8.bath>0]
df9.shape

df10 =df9.drop(['size','price_per_sqrf'],axis='columns')
df10.head(3)
