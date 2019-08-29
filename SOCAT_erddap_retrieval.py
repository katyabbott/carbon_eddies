from urllib.request import urlretrieve
from urllib.error import HTTPError
filepath = 'https://ferret.pmel.noaa.gov/socat/erddap/tabledap/socat_v2019_fulldata.nc?expocode%2Cdataset_name%2Cplatform_name%2Cplatform_type%2Corganization%2Cgeospatial_lon_min%2Cgeospatial_lon_max%2Cgeospatial_lat_min%2Cgeospatial_lat_max%2Ctime_coverage_start%2Ctime_coverage_end%2Cinvestigators%2Csocat_version%2Call_region_ids%2Csocat_doi%2Cqc_flag%2Csample_number%2Cyear%2Cmonth%2Cday%2Chour%2Cminute%2Csecond%2Clongitude%2Clatitude%2Cdepth%2Csal%2CTemperature_equi%2Ctemp%2CTemperature_atm%2CPressure_equi%2CPressure_atm%2CpCO2_water_equi_temp%2CpCO2_water_sst_100humidity_uatm%2CfCO2_water_equi_uatm%2CfCO2_water_sst_100humidity_uatm%2CpCO2_atm_wet_actual%2CpCO2_atm_wet_interp%2CfCO2_atm_wet_actual%2CfCO2_atm_wet_interp%2Cdelta_xCO2%2Cdelta_pCO2%2Cdelta_fCO2%2Crelative_humidity%2Cspecific_humidity%2Cship_speed%2Cship_dir%2Cwind_speed_true%2Cwind_speed_rel%2Cwind_dir_true%2Cwind_dir_rel%2CWOCE_CO2_water%2CWOCE_CO2_atm%2Cwoa_sss%2Cpressure_ncep_slp%2CfCO2_insitu_from_xCO2_water_equi_temp_dry_ppm%2CfCO2_insitu_from_xCO2_water_sst_dry_ppm%2CfCO2_from_pCO2_water_water_equi_temp%2CfCO2_from_pCO2_water_sst_100humidity_uatm%2CfCO2_insitu_from_fCO2_water_equi_uatm%2CfCO2_insitu_from_fCO2_water_sst_100humidty_uatm%2CfCO2_from_pCO2_water_water_equi_temp_ncep%2CfCO2_from_pCO2_water_sst_100humidity_uatm_ncep%2CfCO2_recommended%2CfCO2_source%2Cdelta_temp%2Cregion_id%2Ccalc_speed%2Cetopo2%2CgvCO2%2Cdist_to_land%2Cday_of_year%2Ctime&longitude%3E=-75&longitude%3C=-55&latitude%3E=20&latitude%3C=40&time%3E{0}T00%3A00%3A00Z&time%3C={1}T00%3A00%3A00Z'
#0 - start date, 1 - end date

for i in range(2018,2019):
	for j in range(2):
		#Split it up into half-yearly downloads to keep them small enough
		if j == 0:
			start_date = str(i) + '-01-01'
			end_date = str(i) + '-07-01'
		else:
			start_date = str(i) + '-07-01'
			end_date = str(i+1) + '-01-01'
		infile = filepath.format(start_date, end_date)
		outfile = '../NWAT/socat_v2019_full_{}_{}.nc'.format(i,j)
		try:
			urlretrieve(infile,outfile)
		except HTTPError:
			pass


