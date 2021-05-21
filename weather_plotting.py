
# coding: utf-8

# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[3]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[28]:

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df = df.sort_values(by=['ID','Date'])


# In[42]:

df.head()


# In[35]:

df = df[df["Date"]!="2008-02-29"]
df = df[df["Date"]!="2012-02-29"]


# In[39]:

df['Year'], df['Month-date'] = zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))


# In[43]:

import numpy as np


# In[52]:

temp_min = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-date').aggregate({'Data_Value':np.min})
temp_max = df[(df['Element'] == "TMAX") & (df["Year"] != "2015")].groupby("Month-date").aggregate({"Data_Value":np.max})


# In[55]:

temp_min_15 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-date').aggregate({'Data_Value':np.min})
temp_max_15 = df[(df['Element'] == "TMAX") & (df["Year"] == "2015")].groupby("Month-date").aggregate({"Data_Value":np.max})


# In[65]:

broken_min = np.where(temp_min_15["Data_Value"] < temp_min["Data_Value"])
broken_max = np.where(temp_max_15["Data_Value"] > temp_max["Data_Value"])


# In[69]:

get_ipython().magic('matplotlib inline')


# In[109]:

plt.figure()
plt.plot(temp_max.values, c='r', label='record high')
plt.plot(temp_min.values, c='b', label='record low')
plt.scatter(broken_max, temp_max_15.iloc[broken_max], s=25, c='black', label='broken high')
plt.scatter(broken_min, temp_min_15.iloc[broken_min], s=25, c='red', label='broken low')
plt.gca().axis([-5, 370, -400, 450])
plt.xticks(range(0, len(temp_max), 30), temp_max.index[range(0, len(temp_max), 30)], rotation=45)
plt.fill_between(range(len(temp_max)), temp_max['Data_Value'], temp_min['Data_Value'], facecolor='yellow', alpha=0.25)
plt.legend(frameon=False, loc=0)
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Global Daily Climate Records')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)


# In[110]:

plt.show()


# In[111]:

plt.savefig("temprecords.png")

