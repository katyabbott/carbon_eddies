## Calculate reference year xxxx data from 
## Landschutzer (2016) or other pCO2 climatologies
## as well as rate of pCO2 change per year
#https://www.nodc.noaa.gov/ocads/oceans/SPCO2_1982_2015_ETH_SOM_FFN.html

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.rrule import rrule, MONTHLY
from sklearn.linear_model import LinearRegression


#Bermuda region coordinates are 290.125, 300.125, 27.125, 37.125
buf_dist = 2.5 #additional distance on either side of Bermuda region
#Creating six 5 deg lat x 10 deg lon boxes per Takahashi (2009)
minlon, maxlon = (290.125 - 360) - 2*buf_dist, (300.125 - 360) + 2*buf_dist 
minlat, maxlat = 27.125 - buf_dist, 37.125 + buf_dist
#land_data is Landschutzer dataset with pCO2 for all months/years
#land_clim is just monthly climatology created by averaging all data by month
land_data = '../../carbon/Landschutzer_data/spco2_1982-2015_MPI_SOM-FFN_v2016.nc'
land_clim = '../../carbon/Landschutzer_data/spco2_clim_1985-2015_MPI_SOM-FFN_v2016.nc'
time_since = dt.datetime(2000,1,1) #reference date of dataset
ds = Dataset(land_data)
ds_clim = Dataset(land_clim)
times = ds['time'][:]
lat_all = ds['lat'][:].data
lon_all = ds['lon'][:].data
pco2_all = ds['spco2_smoothed'][:]
pco2_clim_all = ds_clim['spco2_clim'][:]

#Calculate indices for Bermuda region
lat_ind = (lat_all > minlat) & (lat_all < maxlat)
lon_ind = (lon_all > minlon) & (lon_all < maxlon)
lon = lon_all[lon_ind]
lat = lat_all[lat_ind]
pco2 = pco2_all[:,lat_ind,:][:,:,lon_ind]
clim = pco2_clim_all[:,lat_ind,:][:,:,lon_ind]

#Create 6 5x10 boxes
lonbox1, lonbox2 = np.array_split(lon,2)
latbox1, latbox2, latbox3 = np.array_split(lat,3)



#Test on one box
lonbox, latbox = lonbox1, latbox1
latb_ind = np.isin(lat, latbox)
lonb_ind = np.isin(lon, lonbox)
pco2_box = pco2[:,latb_ind,:][:,:,lonb_ind]
clim_boxes = np.mean(clim[:,latb_ind,:][:,:,lonb_ind], axis = (1,2)) #calculate monthly averages across box points
box_ave = np.mean(clim[:,latb_ind,:][:,:,lonb_ind], axis = (0,1,2)) #calculate annual average across box points
detrend = clim_bin - box_ave #seasonal correction to produce detrended data

#Calculate detrended data within box
pco2_bin_detrended = np.empty(pco2_bin.shape)
for i in range(12):
    pco2_bin_month = pco2_bin[i::12,:,:]
    xx = pco2_bin_month - detrend[i]
    pco2_bin_detrended[i::12,:,:] = xx

start_date = dt.timedelta(seconds = int(times[0])) + time_since
end_date = dt.timedelta(seconds = int(times[-1])) + time_since

mmyy = []
pco2_detrended = np.empty(0)
for i, date in enumerate(rrule(freq = MONTHLY, dtstart=start_date, until = end_date)):
    pco2_detrend_mmyy = pco2_bin_detrended[i,:,:].ravel()
    pco2_detrended = np.append(pco2_detrended, pco2_detrend_mmyy)
    my = [date for x in range(len(pco2_detrend_mmyy))]
    mmyy = mmyy + my

date_ordinals = [x.toordinal() for x in mmyy]
X = np.array(date_ordinals).reshape((-1, 1))

#Calculate regression coefficients
model = LinearRegression().fit(X,pco2_detrended)
model.score(X, pco2_detrended)
annual_inc = 365*model.coef_


