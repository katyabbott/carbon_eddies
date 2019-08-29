from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter
import datetime
import glob

##Concatenate and merge into one dataframe
bminlon, bmaxlon = 290.125 - 360, 300.125 - 360
bminlat, bmaxlat = 27.125, 37.125
socat_filepath = '../../carbon/SOCAT_Sargasso_v2019/*.nc'
filelist = glob.glob(socat_filepath)
#ds = Dataset(filelist[0])
df = pd.DataFrame()

for file in filelist:
    ds = Dataset(file)
    ## extract expocodes for each observation
    dict_ds = {}
    trajectory_id = ds.variables['expocode'][:].data
    ship_ids = [''.join([letter.decode('UTF-8') for letter in id]) for id in trajectory_id]
    dict_ds['expocode'] = ship_ids
    dict_ds['lon'] = ds.variables['longitude'][:]
    dict_ds['lat'] = ds.variables['latitude'][:]
    dict_ds['depth'] = ds.variables['depth'][:]
    times = ds.variables['time'][:]
    dict_ds ['date'] = [datetime.timedelta(seconds = s) + datetime.datetime(1970, 1, 1) for s in times]
    dict_ds['sal'] = ds.variables['sal'][:]
    dict_ds['pressure'] = ds.variables['Pressure_equi'][:]
    # In case in situ pressure and salinity are missing
    dict_ds['ncep_press'] = ds.variables['pressure_ncep_slp'][:]
    dict_ds['woa_sss'] = ds.variables['woa_sss'][:]
    dict_ds['SST'] = ds.variables['temp'][:]
    dict_ds['fCO2'] = ds.variables['fCO2_recommended'][:]
    #If comparing pCO2 calculation to in situ measurements:
    dict_ds['pCO2_ship'] = ds.variables['pCO2_water_sst_100humidity_uatm'][:]
    for k, v in dict_ds.items():
        if np.ma.is_masked(v): #does it have a mask
            if (v.mask != False).any(): #i.e. there are masked elements in the mask
                v[v.mask == True] = np.nan
                dict_ds[k] = v.data
    df1 = pd.DataFrame.from_dict(dict_ds)
    df = df.append(df1, ignore_index = True, sort = True)

#Calculate virial coefficient B, v in terms of SST (K)
B_v = lambda T: -1636.75 + 12.0408*T - 3.279e-2*T**2 + 3.16528e-5*T**3
delta_v = lambda T: 57.7 - 0.118*T

#From Weiss 1974
def fCO2_to_pCO2(fCO2, Ps, T):
    Ps /= 1013.25
    T += 273.15
    exp_calc = np.exp(Ps*(B_v(T)+ 2*delta_v(T))/(82.05746*T))
    pCO2 = fCO2/exp_calc
    return pCO2

#Use ncep pressure if equilibrator pressure is NaN
df_equi = df[~df['pressure'].isna()]
df_ncep = df[df['pressure'].isna()]

#Calculate pCO2 from fCO2
df_equi = df_equi.assign(pCO2 = fCO2_to_pCO2(df_equi['fCO2'], 
    df_equi['pressure'], df_equi['SST']))
df_ncep = df_ncep.assign(pCO2 = fCO2_to_pCO2(df_ncep['fCO2'], 
    df_ncep['ncep_press'], df_ncep['SST']))
    
#Rejoin data
df_pCO2 = df_equi.append(df_ncep)
df_pCO2 = df_pCO2[pd.notnull(df_pCO2['pCO2'])]
