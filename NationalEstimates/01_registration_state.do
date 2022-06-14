*PREAMBLE
	
	clear all
	
	*set directory 
	global dir "/Users/aashishgupta/Dropbox/research/mortality_nfhs5"
	
	*bring in NFHS data 
	use "/Users/aashishgupta/Dropbox/Lekha Jokha/Data/NFHS/nfhs 5/data/IAHR7ADT/IAHR7AFL.DTA", clear 
	
*DATA WRANGLING  

	*keep if a death happened 	
	keep if sh88 != . 
	
	*generate a unique id
	gen hid = _n 

	*keep only necessary variables 
	keep sh87 sh88 sh90* sh91* sh92* sh93* sh94* hv000 hv001 hv006 hv007 hv005 hv024 hid
	
	*reshape so that each line is a death 
	reshape long sh90_ sh91_ sh92u_ sh92n_ sh93m_ sh93y_ sh94_, ///
		i(hid hv000 hv001 hv005 hv006 hv007 sh87 sh88) ///
		j(d_id)
		
	*rename variables
	rename sh90_ sex 
	rename sh91_ registered 
	rename sh92u_ unit_age
	rename sh92n_ number_age 
	rename sh93m_ month_died 
	rename sh93y_ year_died 
	rename sh94_ pregnancy_related 

	*drop those observations that were made in the reshape, and are not real deaths 
	drop if sex == . 
	
	*generate a date of interview variable 
	gen doi = ym(hv007, hv006)
	format doi %tm 
	
	*generate a date of death variable 
	drop if month_died == 98
	drop if year_died == 9998
	gen dod = ym(year_died, month_died)
	format dod %tm 	
	
	
	*registration levels in 2018 
	preserve 
	keep if year_died == 2018
	tabstat registered [aw=hv005], by(hv024)
	restore 
	
	*registration levels in the first 6 months of 2019
	preserve 
	keep if year_died == 2019 & month_died < 7 
	tab month_died 
	tabstat registered [aw=hv005], by(hv024)
	restore 


	


	
	