This repository contains code to analyze mesoscale eddy-CO2 interactions using sea level anomaly data and observations from the [SOCAT](https://socat.info/index.php/data-access/) database. 

Workflow so far is as follows (code in the process of being added to this repository).
- Use SOCAT_erddap_retrieval.py to get the netCDF files for your region of interest, modifying the URL as necessary.
- Use SOCAT_database.py to consolidate this data into a dataframe, convert fCO2 into pCO2, and calculate air-sea CO2 fluxes (in progress).
- reference_year_calculations.py can be used to seasonally detrend pCO2 data, calculate the average annual increase, and normalize all data to a climatological year in order to calculate pCO2 anomalies. Used here with the Landschutzer (2016) SOM pCO2 dataset, but could be used with others as needed.
