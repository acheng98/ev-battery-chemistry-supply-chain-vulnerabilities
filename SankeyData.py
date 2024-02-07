"""
This code takes production and trade data, and creates a file that describes flows in 
a Sankey diagram-manner. Plots by this script generate the figures found in Fig. 2 and Fig. 3
of the paper. 

Data inputs are written below or imported from csv files downloaded from IntraCen. 

"""

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os.path

# GLOBAL VARIABLES
# DATA SETUP
# MINING
LI_PROD_2020 = {"Argentina": 5900, "Australia": 39700, "Brazil": 1420, "Chile": 21500, "China": 13300, "Portugal": 348, 
	"Zimbabwe": 417, "United States of America": 710} # Source: MCS 2022, US production estimated - metric tons contained lithium
CO_PROD_2020 = {"United States of America": 600, "Australia": 5630, "Canada": 3690, "China": 2200, "Congo, Democratic Republic of the": 98000, 
	"Cuba": 3800, "Indonesia": 1100, "Madagascar": 850, "Morocco": 2300, "Papua New Guinea": 2940, "Philippines": 4500, "Russian Federation": 9000, 
	"Other": 7640} # Source: MCS 2022 - metric tons contained cobalt
NI_PROD_2020 = {"United States of America": 16700, "Australia": 169000, "Brazil": 77100, "Canada": 167000, "China": 120000, 
	"Indonesia": 771000, "New Caledonia": 200000, "Philippines": 334000, "Russian Federation": 283000, "Other": 373000} # Source: MCS 2022 - metric tons contained nickel
MN_PROD_2020 = {"Australia": 3330000, "Brazil": 494000, "Myanmar": 254000, "China": 1340000, "Côte d'Ivoire": 525000, "Gabon": 3310000, 
	"Georgia": 186000, "Ghana": 637000, "India": 632000, "Kazakhstan": 158000, "Malaysia": 347000, "Mexico": 198000, "South Africa": 6500000, 
	"Ukraine": 578000, "Viet Nam": 121000, "Other": 260000} # Source: MCS 2022 - metric tons manganese ore
for key in MN_PROD_2020: # Convert to contained Manganese
	MN_PROD_2020[key] *= 0.300
P_PROD_2020 = {"United States of America": 23500000, "Algeria": 1200000, "Australia": 2000000, "Brazil": 6000000, "China": 88000000,
	"Egypt": 4800000, "Finland": 995000, "India": 1400000, "Israel": 3090000, "Jordan": 8940000, "Kazakhstan": 1300000, "Mexico": 577000,
	"Morocco": 37400000, "Peru": 3300000, "Russian Federation": 14000000, "Saudi Arabia": 8000000, "Senegal": 1600000, 
	"South Africa": 1800000, "Togo": 942000, "Tunisia": 3190000, "Turkey": 600000, "Uzbekistan": 900000, "Viet Nam": 4500000, 
	"Other": 870000} # Source: MCS 2022 - metric tons phosphorus rock
for key in P_PROD_2020: # Convert to contained phosphorus - 
	P_PROD_2020[key] *= 30/223
MINE_PROD = [LI_PROD_2020,CO_PROD_2020,NI_PROD_2020,MN_PROD_2020,P_PROD_2020]

# REFINING - Sun et al. 2021 except Phosphorus, which is estimated with trade data only
# LI_CARB_PROD = {"Argentina": 34904, "Chile": 102692, "China": 154000}
# LI_HYD_PROD = {"Chile": 9120, "China": 76000, "United States of America": 13173}
# Derived from above and conversion coefficients below
# LI_REF_PROD = {"Argentina": 34904, "Chile": 110718, "China": 211520, "United States of America": 11592} # Old conversion coefficients
LI_REF_PROD = {"Argentina": 6562, "Chile": 20930, "China": 42480, "United States of America": 2345} 
CO_REF_PROD = {"Australia": 3200, "Belgium": 6600, "Canada": 6500, "China": 78360, "Congo, Democratic Republic of the": 400, "Finland": 12800,
				"India": 100, "Japan": 4000, "Madagascar": 2800, "Morocco": 1600, "Norway": 3500, "South Africa": 1000, "Zambia": 2000}
NI_REF_PROD = {"China": 167000, "Finland": 8000, "France": 1000, "Japan": 17000, "Norway": 8000, "Korea, Republic of": 12000, 
				"South Africa": 6000, "United Kingdom": 8000}
# MN_REF_PROD = {"China": 300400, "Colombia": 5143, "Greece": 22286, "India": 857, "Japan": 28286, "Spain": 12857, "United States of America": 50143}
# Derived from [above x conversion coefficient below]
MN_REF_PROD = {"China": 189850, "Colombia": 3250, "Greece": 14085, "India": 542, "Japan": 17877, "Spain": 8126, 
				"United States of America": 31690}
# Phosphoric Acid Only
PA_REF_PROD = {"West Europe": 884000, "Central Europe": 564000, "East Europe & Central Asia": 8715000, "North America": 11649000,
	"Latin America": 3363000, "Africa": 15898000, "West Asia": 8467000, "South Asia": 2948000, "East Asia": 33278000, "Oceania": 743000}
for key in PA_REF_PROD:
	PA_REF_PROD[key] *= 0.316
REF_PROD = [LI_REF_PROD,CO_REF_PROD,NI_REF_PROD,MN_REF_PROD,PA_REF_PROD]

# CATHODE
CATH_CTS = ["China","Japan","Korea, Republic of","Canada","United States of America"] 
FINAL_PRODS = ["NCM","NCA","LFP","LMO","LCO"]
NCX_AMT = [197000,56481,94135,0,0]							# Sun et al. NCA/NCM production 
NCM_Li = 0.07173*0.441										# Calculated from chemical formula - 'Chemical Formula Calculations' + market share of NCM from Xu et al. 2019
NCM_Ni = 0.33181*0.441										# Calculated from chemical formula + market share of NCM vs NCA from Xu et al. 2019
NCM_Co = 0.12703*0.441										# Calculated from chemical formula + market share of NCM vs NCA from Xu et al. 2019
NCM_Mn = 0.13874*0.441										# Calculated from chemical formula + market share of NCM vs NCA from Xu et al. 2019
NCA_Li = 0.07224*0.559										# Calculated from chemical formula + market share of NCA vs NCM from Xu et al. 2019
NCA_Ni = 0.48869*0.559										# Calculated from chemical formula + market share of NCA vs NCM from Xu et al. 2019
NCA_Co = 0.03067*0.559										# Calculated from chemical formula + market share of NCA vs NCM from Xu et al. 2019
LMO_AMT = [76400,10629,0,0,0]								# Sun et al. LMO production
LMO_Li = 0.0384 											# Calculated from chemical formula
LMO_Mn = 0.60766 											# Calculated from chemical formula
LCO_AMT = [54800,5509,23413,0,0]							# Sun et al. LCO production
LCO_Li = 0.0709 											# Calculated from chemical formula
LCO_Co = 0.60216 											# Calculated from chemical formula
LFP_AMT = [80000,0,0,5000,4000] 							# Sun et al. LFP production 
LFP_Li = 0.04400											# Calculated from chemical formula
LFP_P = 0.1963												# Calculated from chemical formula


NCM_Li_amt = [l*NCM_Li for l in NCX_AMT]
NCM_Ni_amt = [l*NCM_Ni for l in NCX_AMT]
NCM_Co_amt = [l*NCM_Co for l in NCX_AMT]
NCM_Mn_amt = [l*NCM_Mn for l in NCX_AMT]
NCA_Li_amt = [l*NCA_Li for l in NCX_AMT]
NCA_Ni_amt = [l*NCA_Ni for l in NCX_AMT]
NCA_Co_amt = [l*NCA_Co for l in NCX_AMT]
LMO_Li_amt = [l*LMO_Li for l in LMO_AMT]
LMO_Mn_amt = [l*LMO_Mn for l in LMO_AMT]
LCO_Li_amt = [l*LCO_Li for l in LCO_AMT]
LCO_Co_amt = [l*LCO_Co for l in LCO_AMT]
LFP_Li_amt = [l*LFP_Li for l in LFP_AMT]
LFP_P_amt  = [l*LFP_P  for l in LFP_AMT]
zeros = [0 for l in range(len(CATH_CTS))]

Li_amts = [NCM_Li_amt,NCA_Li_amt,LFP_Li_amt,LMO_Li_amt,LCO_Li_amt]
Ni_amts = [NCM_Ni_amt,NCA_Ni_amt,zeros.copy(),zeros.copy(),zeros.copy()]
Co_amts = [NCM_Co_amt,NCA_Co_amt,zeros.copy(),zeros.copy(),LCO_Co_amt]
Mn_amts = [NCM_Mn_amt,zeros.copy(),zeros.copy(),LMO_Li_amt,zeros.copy()]
P_amts = [zeros.copy(),zeros.copy(),LFP_P_amt,zeros.copy(),zeros.copy()]
CATH_PROD = [Li_amts,Co_amts,Ni_amts,Mn_amts,P_amts]

# CODES
# Sources: Sun et al 2021, Scott and Ireland 2020, Tian et al. 2021, Ronzheimer et al. 2022, Li et al. 2023
LI_RAW = ["253090 Unprocessed Lithium"]
LI_REF = ["282520 Li O-OH","283691 Li Carbonates"] #, "280519 Alkali and alkali earth",
		 # "282739 Lithium Chlorides"] #, "282690 Lithium Fluorine salts"]
CO_RAW = ["260500 Cobalt ores and concentrates"] #, "260400 Nickel ores and concentrates"] #
CO_REF = ["282200 Cobalt oxides", "283329 Sulphates", "810520 Unwrought cobalt; powders", 
		"810590 Cobalt and articles", "810530 Cobalt waste and scrap"]
NI_RAW = ["260400 Nickel ores and concentrates"]
NI_REF = ["282540 Nickel oxides and hydroxides", "282735 Nickel Chlorides", "283324 Sulphates of nickel", 
		"750110 Nickel; nickel mattes", "750120 Nickel oxide sinters", 
		"750210 Unwrought nickel, not alloyed", "750220 Unwrought nickel alloys", "750400 Nickel powders and flakes",
		"750300 Nickel; waste and scrap"] # Need to be careful here because only class 1 nickel works for batteries...
MN_RAW = ["260200 Manganese ores and concentrates"]
MN_REF = ["282010 Manganese dioxide","282090 Manganese oxides; excluding manganese dioxide",
		"283329 Sulphates", "811100 Manganese; articles thereof including waste and scrap"]
P_RAW = ["2510 Phosphate, Ground or Unground"]
P_REF = ["280470 Phosphorus", "280920 Phosphoric Acid"]

MINE_CODES = [LI_RAW,CO_RAW,NI_RAW,MN_RAW,P_RAW]
REF_CODES = [LI_REF,CO_REF,NI_REF,MN_REF,P_REF]

# CODE CONVERSIONS 
# Calculated using chemical formulas, which match up with Sun et al. 2018
LI_CONV = [1, # Source data [Sun et al 2021] gives in terms of contained lithium - this does not contain the actual data from 250390, only the Australian spodumene
			0.16542, # 282520 Lithium Hydroxide and Oxides - LiOH•H2O: 41.96
			0.18787, # 283691 Lithium Carbonate - Li2CO3: 73.89
			0.03, # Alkali and alkali earth – estimate from Sun et al. 2018 "concentrates"
			0.16374, # Lithium chlorides - LiCl: 42.39
			]

# Sun et al 2019 Cobalt
CO_CONV = [0.150, # 260500 cobalt ore
			0.001, # 260400 nickel ore
			0.329, # 282200 oxide and hydroxide
			0.600, # scrap, unwrought cobalt, cobalt and articles <-- this seems wrong 
			# below are highly uncertain estimates
			0.01, # sulfates - this is accounting for all sulfates that are not sodium, magnesium, aluminum, nickel, copper, barium, alums, or persulphates
			] 

# Nakajima et al 2018 Nickel
NI_CONV = [0.015, # ores and concentrates - 260400
			0.787, # oxides and hydroxides - 282540
			0.454, # chlorides - 282735
			0.224, # other sulphates of nickel - 283324
			0.750, # nickel mattes - 750110
			0.600, # nickel oxide sinters - 750210
			0.995, # nickel, not alloyed - 750210
			0.500, # nickel alloys - 750220
			0.995, # nickel powders and flakes - 750400
			0.500, # nickel waste and scrap 750300
			]

# Sun et al 2020 Manganese
MN_CONV = [ 0.300, # 260200 - ore
			0.900, # EMM - Electrolytic Manganese Metal
			0.632, # 282010 - EMD (Electrolytic Manganese Dioxide)
			0.774, # manganese oxides - 282090
			0.020, # sulphates - 283329 - this is accounting for all sulfates that are not sodium, magnesium, aluminum, nickel, copper, barium, alums, or persulphates
				# "many manganese-based batteries used manganese sulfate as a primary precursor"
			0.004, # Manganese; articles thereof including waste and scrap, 811100
			]

# Li et al. 2023 and Chen and Chen 2023
P_CONV = [ 0.119,  # Ore - take average of Li et al. (0.098) and Chen and Chen (0.140)
			1, 	   # Assume phosphorus is pure
			0.436, # Calculated from chemical formula
			0.273, # Average of Phosphorus in Phosphoric Acid (0.316, calculated from chemical formula), Li et al. (0.268), and Chen and Chen (0.236)
			]

MINE_CODE_CONVS = [[LI_CONV[0]],CO_CONV[:2],[NI_CONV[0]],[MN_CONV[0]],[P_CONV[0]]]
REF_CODE_CONVS = [LI_CONV[1:5],[CO_CONV[2],CO_CONV[4],CO_CONV[3],CO_CONV[3],CO_CONV[3]],NI_CONV[1:],MN_CONV[2:],P_CONV[1:]]

# COUNTRIES
COUNTRIES = ["Angola","Argentina","Australia","Austria",
			"Bahamas","Bahrain","Bangladesh","Belarus","Belgium","Belize","Bolivia, Plurinational State of",
			"Bosnia and Herzegovina","Brazil","Brunei Darussalam","Bulgaria","Burkina Faso",
			"Cambodia","Cameroon","Canada","Chile","China","Colombia","Congo","Congo, Democratic Republic of the",
			"Costa Rica","Côte d'Ivoire","Croatia","Cuba","Cyprus","Czech Republic",
			"Denmark","Dominican Republic",
			"Ecuador","Egypt","El Salvador","Estonia","Eswatini","Ethiopia","Finland","France","French Polynesia",
			"Gabon","Georgia","Germany","Ghana","Greece","Guatemala","Guyana",
			"Honduras","Hong Kong, China","Hungary",
			"Iceland","India","Indonesia","Iran, Islamic Republic of","Iraq","Ireland","Israel","Italy",
			"Jamaica","Japan","Jordan",
			"Kazakhstan","Kenya","Korea, Democratic People's Republic of","Korea, Republic of","Kuwait","Kyrgyzstan",
			"Lao People's Democratic Republic","Latvia","Lebanon","Lesotho","Lithuania","Luxembourg",
			"Macedonia, North","Madagascar","Malaysia","Mali","Mauritius","Mexico","Moldova, Republic of",
			"Mongolia","Montenegro","Morocco","Mozambique","Myanmar",
			"Namibia","Nepal","Netherlands","New Caledonia","New Zealand","Nicaragua","Nigeria","Norway","Oman",
			"Pakistan","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar",
			"Romania","Russian Federation",
			"Saudi Arabia","Senegal","Serbia","Seychelles","Singapore","Slovakia","Slovenia","South Africa","Spain",
			"Sri Lanka","Sudan","Sweden","Switzerland","Syrian Arab Republic",
			"Taipei, Chinese","Tanzania, United Republic of","Thailand","Togo","Trinidad and Tobago","Tunisia",
			"Turkey","Turkmenistan",
			"Uganda","Ukraine","United Arab Emirates","United Kingdom","United States of America","Uruguay",
			"Uzbekistan",
			"Viet Nam","Zambia","Zimbabwe"]

# IFASTAT regions
REGIONS = {"West Europe": ["Austria", "Belgium", "Luxembourg", "Denmark", "Finland", "France", "Germany", "Greece",
			"Iceland", "Ireland", "Italy", "Netherlands", "Norway", "Portugal", "Spain", "Sweden", "Switzerland", "United Kingdom"], 
		   "Central Europe": ["Albania", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czech Republic", "Cyprus", "Hungary", 
			"Macedonia, North", "Poland", "Romania", "Serbia", "Montenegro", "Slovakia", "Slovenia"], 
		   "East Europe & Central Asia": ["Armenia", "Azerbaijan", "Estonia", "Latvia", "Lithuania", "Belarus", "Georgia",
			"Kazakhstan", "Kyrgyzstan", "Moldova, Republic of", "Russian Federation", "Tajikistan", "Turkmenistan", 
			"Ukraine", "Uzbekistan"], 
		   "North America": ["Canada", "United States of America"],
		   "Latin America": ["Argentina", "Bahamas", "Belize", "Bolivia, Plurinational State of", "Brazil", "Chile", 
			"Colombia", "Costa Rica", "Cuba", "Curacao", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Guyana", 
			"Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Trinidad and Tobago", "Uruguay", "Venezuela"], 
		   "Africa": ["Angola","Algeria", "Burkina Faso", "Cameroon", "Congo", "Congo, Democratic Republic of the", "Côte d'Ivoire", 
			"Egypt", "Eswatini", "Ethiopia", "Gabon", "Ghana", "Kenya", "Libya", "Madagascar", "Mali", "Mauritania", "Mauritius", 
			"Morocco", "Mozambique", "Namibia", "Nigeria", "Senegal", "Seychelles", "South Africa", "Sudan", 
			"Tanzania, United Republic of", "Togo", "Tunisia", "Uganda", "Western Sahara", "Zambia", "Zimbabwe"], 
		   "West Asia": ["United Arab Emirates", "Afghanistan", "Bahrain", "Iran, Islamic Republic of", "Iraq", "Israel", "Jordan",
			"Kuwait", "Lebanon", "Oman", "Qatar", "Saudi Arabia", "Syrian Arab Republic", "Turkey"], 
		   "South Asia": ["Bangladesh", "India", "Nepal", "Pakistan", "Sri Lanka"], 
		   "East Asia": ["Cambodia", "China", "Brunei Darussalam", "Hong Kong, China", "Indonesia", "Japan", 
			"Korea, Democratic People's Republic of", "Korea, Republic of", "Lao People's Democratic Republic of", "Malaysia", "Mongolia", 
			"Myanmar", "Philippines", "Singapore", "Taipei, Chinese", "Thailand", "Viet Nam"], 
		   "Oceania": ["Australia", "Christmas Island", "French Polynesia", "Nauru", "New Caledonia", "New Zealand", "Papua New Guinea"]}

COUNTRIESREGIONS = COUNTRIES + ["Other","Missing"]

NBCP = "Non-Battery Cathode Products"
NCPC = "Trade to countries with no cathode production or <br /> refined materials not accounted for in trade"
NTRM = "Raw Materials not accounted for in refining production"
MRMT = "Missing Refined Material Trade"
URMS = "Unknown Raw Material Source"
UARP = "Unaccounted for Additional Refining Production"
TTCR = "Trade to countries with no refining or <br /> raw materials not accounted for in trade"
TFCR = "Trade from countries with no refining"
TFCM = "Trade from countries with no mining"

def quot(value):
	'''
	Takes a string input and returns it in quotations. Used to convert country names to get the right input data files. 
	'''
	return '"' + value + '"'

def underline(value):
	'''
	Takes a string input and replaces spaces and commas with an underline. Used to convert country names to get the right input data files. 
	'''
	out = ""
	for char in value:
		if char == " " or char == ",":
			out += "_"
		else:
			out += char
	return out

def unquot(value):
	'''
	Takes a string input and removes any quotation marks. Used to convert country names to get the right input data files. 
	'''
	val = str(value)
	val.strip('"')
	val.strip("'")
	return val

def ununder(value):
	'''
	Takes a string input and replaces underlines with spaces and/or commas. Used to convert country names to get the right input data files. 
	'''
	val = str(value)
	val.replace("__", ", ")
	val.replace("_", " ")
	return val

def hex2rgba(value):
	'''
	Takes a string HEX code and returns the equivalent RGBA value. Used to convert hex color codes to matplotlib-friendly rgba values.
	'''
	value = value.lstrip('#')
	lv = len(value)
	return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def commonname(country_list):
	'''
	A function to provide a common name for a given list of countries, given that trade data sometimes uses 
	long-form or official country names. 
	'''
	common = {"Congo, Democratic Republic of the": "DRC", 
				"Russian Federation": "Russia",
				"Korea, Republic of": "South Korea",
				"United States of America": "USA"}
	out = []
	for c in country_list:
		if c in common:
			out.append(common[c])
		else:
			out.append(c)
	return out

def find_region(regions,country):
	'''
	A function to find which region a country is in, used primarily for the phosphorus analysis which requires regional
	aggregation of trade data as production data is only defined at the regional level. 
	'''
	for k,reg in regions.items():
		if country in reg:
			return k
	return "Other"

# MINING TO REFINING STEP
def balance(year,mat,codes,convs,regind,regions):
	'''
	Inputs:
	- Year: The year of the data. Integer
	- Mat: The production of this material at the supply step. Dictionary of producers: amount they produce
	- Codes: The list of relevant trade codes for this material. List of strings.
	- Convs: The conversion coefficients for each trade code. List of floats. 
	- regind: The regional indicator. If equal to 0, we don't have any summary regions. If 1, we set all importers to regions. 
			If 2, we set all exporters to regions. If 3, set both importers nad exporters to regions.
	- regions: A dictionary of regions and the corresponding countries

	Output:
    - flow_dict: A dictionary representing the trade flows between countries or regions.
    - miss_prod: A dictionary describing missing production that couldn't be balanced.
	'''

	# Structure: exporting --> importing : amount moving
	flow_dict = {} # summary dictionary
	miss_prod = {} # This is the dictionary describing missing production

	# Add all countries is listed as miners or refiners with that much production
	for country,amount in mat.items():
		# Throw in flag to deal with regions
		if country in COUNTRIES:
			flow_dict[country] = {country: amount} # Repeat because first / left side is the list of exporting countries and right dictionary will contain all importers 
	upstream = list(mat.keys())

	for code_ind,code in enumerate(codes):

		for country in COUNTRIES:
			# Import data
			under = underline(country) 
			try:
				df = pd.read_csv("../SupplyChainData/TradeMap/" + str(code) + "/Trade_Map_-_List_of_supplying_markets_for_a_product_imported_by_"+under+".txt",sep="\t")
			except FileNotFoundError:
				try:
					df = pd.read_csv("../SupplyChainData/TradeMap/" + str(code) + "/Trade_Map_-_List_of_supplying_markets_for_a_product_imported_by_"+under+"_(Mirror).txt",sep="\t")
				except FileNotFoundError:
					# print("File not found for " + country + " for code '" + code +"'")
					continue

			ct = 0

			# Get the column of the year
			yr = -1
			for yct,col in enumerate(list(df.columns)):
				if col[:4] == str(year):
					yr = yct
					break
			if yr < 0:
				# print("Data not found for year " + str(year) + " for " + country + " for code '" + code + "'")
				continue

			# Iterate through all rows of dataframe, pull the data from that year
			for ind,row in df.iterrows():
				# Need to skip the first line - world summary 
				if ct < 1:
					ct += 1
					continue

				# Get the value in the column of the year desired, adjusted for the conversion factor
				try:
					adjval = int(row[yr])*convs[code_ind]
				except ValueError:
					# print("Value not found for " + str(year) + " for " + country + " for code '" + code + "'")
					adjval = 0

				# Get the name of the country that is exporting to our source file country
				exporter = unquot(ununder(row["Exporters"]))
				importer = country

				if exporter not in flow_dict:
					flow_dict[exporter] = {exporter: 0}

				flow_dict[exporter].setdefault(importer, 0)
				flow_dict[exporter][importer] += adjval
				# Subtract the amount from the producing country
				flow_dict[exporter][exporter] -= adjval

	# FIX MISSING BALANCES 
	for exp in flow_dict.keys():
		if flow_dict[exp][exp] < 0:
			# Missing from other, add to missing data 
			miss_prod.setdefault(exp,0)
			miss_prod[exp] -= flow_dict[exp][exp]
			# Set "Other" back to zero
			flow_dict[exp][exp] = 0 

	# Iterate through flow_dict and replace with regions where applicable 
	if regind == 1: # Replace all importers with regions
		# Make a new dict to contain all of the regions for ease of retrieval
		exptoregion = {}
		for exporter,importers in flow_dict.items():
			for importer,value in importers.items():
				region = find_region(regions,importer)
				if region == None:
					print(exporter,importer)
				if exporter not in exptoregion:
					exptoregion[exporter] = {region: value}
				elif region not in exptoregion[exporter]:
					exptoregion[exporter][region] = value
				else:
					exptoregion[exporter][region] += value
		flow_dict = exptoregion
	elif regind == 2: # Replace all exporters with regions
		# Make a new dict to contain all of the regions for ease of retrieval
		imptoregion = {}
		# Add all region production 
		for region,amount in mat.items():
			imptoregion[region] = {region: amount} # Repeat because first / left side is the list of exporting countries and right dictionary will contain all importers 

		for exporter,importers in flow_dict.items():
			region = find_region(regions,exporter)
			if region != "Other":
				for importer,value in importers.items():
					if importer in imptoregion[region]:
						imptoregion[region][importer] += value
					else:
						imptoregion[region][importer] = value
					imptoregion[region][region] -= value # subtract out from stuff not traded in region
					if imptoregion[region][region] < 0:
						miss_prod.setdefault(region,0)
						miss_prod[region] -= imptoregion[region][region]
						imptoregion[region][region] = 0 # Reset to zero 
		flow_dict = imptoregion
	return flow_dict, miss_prod

def sankey(plotflag,year,material,regions,comb_cath,make_color,label,save):
	'''
	Creates a Sankey diagram for the input mining, refining, and cathode production data

	Inputs:
	- plotflag: True or false, to plot or not
	- year: The year of the data being analyzed
	- material: the name of the material selected
	- comb_cath: Combine the cathode material production at the end or not. 
	- make_color: fix the colors 

	Outputs:
	- Sankey diagram visualization if plotflag is True
	- A csv file with the relevant flows, if save is True
	'''
	material_index = {"Lithium": 0, "Cobalt": 1, "Nickel": 2, "Manganese": 3, "Phosphorus": 4}
	matind = material_index.get(material, -1)
	if matind == -1:
		print("Material not identified.")
		return
	flows = pd.DataFrame(columns = ["Source","Target","Value"])
	fi = 0 # flow index

	# Phosphorus region flag
	if matind == 4:
		mr_regind = 1
		rc_regind = 2
	else:
		mr_regind = 0
		rc_regind = 0

	mineprod = MINE_PROD[matind]
	refprod = REF_PROD[matind]

	###
	# Calculate outflow trade balances and missing production, based on production and trade. 
	###
	mrbal,mmiss = balance(year,mineprod,MINE_CODES[matind],MINE_CODE_CONVS[matind],mr_regind,regions)
	rcbal,rmiss = balance(year,refprod,REF_CODES[matind],REF_CODE_CONVS[matind],rc_regind,regions)

	cmiss = {}

	# Add flows of refined material from total possible space of refined material to those that go into cathodes
	for ind1,cath in enumerate(CATH_PROD[matind]):
		for ind2,val in enumerate(cath):
			if val > 0: # Don't need to add flows that are 0 
				if comb_cath:
					cathct = FINAL_PRODS[ind1]
				else:
					cathct = CATH_CTS[ind2] + "_" + FINAL_PRODS[ind1]
				cathposs = CATH_CTS[ind2] + "_cath_poss"
				flows.loc[fi] = [cathposs,cathct,val]
				fi += 1

	# Sum inputs into the cathode step for countries
	cathindict = {} 
	for exporter,trade in rcbal.items():
		for importer,value in trade.items():
			cathindict.setdefault(importer,0)
			cathindict[importer] += value

	# Combine cath production with refined trade to determine missing data or non-battery products
	for country,cathin in cathindict.items(): 
		pcpc = country + "_cath_poss" # potential cathode producing country
		if country in CATH_CTS:
			diff = cathin - sum(flows[flows["Source"] == pcpc]["Value"])

			# If the amount of input refined material is greater than the sum of the amount going into cathodes, 
			# assume it goes to non-battery products
			if diff >= 0: 
				# Search 
				flows.loc[fi] = [pcpc,NBCP,diff]
				fi += 1
			# If the amount of input refined material is less than the sum of the amount going into cathodes,
			# assume we are missing trade data that would have supplied this cathode production. 
			else: 
				flows.loc[fi] = [MRMT,pcpc,-diff]
				fi += 1
	#
	###

	# print(flows.to_string())

	###
	# Add the flows of refined material to cathode
	###
	for exporter,trade in rcbal.items():
		exp = exporter + "_ref"
		for importer,value in trade.items():
			if value > 0: # Get rid of all of the unnecessary, empty rows
				# ONLY CARE ABOUT REFINING PRODUCERS (including Missing) AT EACH STEP 
				# Add additional flag to cover regions
				if exporter in refprod.keys() or exporter == MRMT or exporter in regions: 
					# SEPARATE THE CATHODE PRODUCING COUNTRIES FROM NON-CATHODE PRODUCING COUNTRIES
					if importer in CATH_CTS:
						imp = importer + "_cath_poss"
						flows.loc[fi] = [exp,imp,value]
						fi += 1
					else:
						imp = NCPC
						# Get the specific flow that goes from the exporting source to the target importer
						flow = flows.loc[(flows["Source"] == exp) & (flows["Target"] == imp)]
						if flow.empty:
							flows.loc[fi] = [exp,imp,value]
							fi += 1
						else:
							# Explanation of below:
							# Get the index of the flow in the bigger flows DataFrame.
							# Update the Value at that row to the new sum – of that old Value at that row plus the new value
							flows.at[flow.index.to_list()[0],'Value'] = float(flow['Value']) + value
				else: # Add to "trade from non-producing countries"
					if importer in CATH_CTS:
						imp = importer + "_cath_poss"
						flow = flows.loc[(flows["Source"] == TFCR) & (flows["Target"] == imp)]
						if flow.empty:
							flows.loc[fi] = [TFCR,imp,value]
							fi += 1
						else:
							flows.at[flow.index.to_list()[0],'Value'] = float(flow['Value']) + value
					else:
						# We don't care about the trade from non-producing countries to non-cathode producing countries
						pass

	# Add flows of refined material from total possible space of refined material to those that go into cathodes, but also
	for country,value in refprod.items():
		flows.loc[fi] = [country + "_ref_poss",country + "_ref",value]
		fi += 1				

	###
	# Sum inputs into the refining step for countries
	refindict = {}
	for exporter,trade in mrbal.items():
		for importer,value in trade.items():
			refindict.setdefault(importer,0)
			refindict[importer] += value

	# Combine ref production with mining trade to determine missing *trade* data or non-battery products
	for country,refin in refindict.items(): 
		prpc = country + "_ref_poss" # potential refining producing country
		if country in refprod.keys(): 
			diff = refin - sum(flows[flows["Source"] == prpc]["Value"])
			
			# If the amount of input mined material is greater than the sum of the amount going into refining, 
			# assume it goes to non-refined materials
			if diff >= 0: 
				# Search 
				flows.loc[fi] = [prpc,NTRM,diff]
				fi += 1
			# If the amount of input refined material is less than the sum of the amount going into cathodes,
			# assume we are missing trade data that would have supplied this cathode production. 
			else: 
				if URMS not in mrbal.keys():
					mrbal.setdefault(URMS,{})
				mrbal[URMS].setdefault(country,0)
				mrbal[URMS][country] -= diff
	#
	###

	# Add the missing refining
	for importer,value in rmiss.items():
		if importer in refprod.keys():
			imp = importer + "_ref"
			flows.loc[fi] = [UARP,imp,value]
			fi += 1

	###
	# Add the flows of mined material to refined
	###
	for exporter,trade in mrbal.items():
		exp = exporter + "_mine"
		for importer,value in trade.items():
			if value > 0: # Get rid of all of the unnecessary, empty rows
				if (exporter in mineprod.keys() or exporter == URMS) and exporter != "Other": # ONLY CARE ABOUT MINING PRODUCERS (including Missing) AT EACH STEP - don't include cobalt
					# SEPARATE THE REFINING COUNTRIES FROM NON-REFINING PRODUCING COUNTRIES
					if importer in refprod.keys():
						imp = importer + "_ref_poss"
						flows.loc[fi] = [exp,imp,value]
						fi += 1
					else: # Add to "trade from non-producing countries"
						imp = TTCR
						# Get the specific flow that goes from the exporting source to the target importer
						flow = flows.loc[(flows["Source"] == exp) & (flows["Target"] == imp)]
						if flow.empty:
							flows.loc[fi] = [exp,imp,value]
							fi += 1
						else:
							# Explanation of below:
							# Get the index of the flow in the bigger flows DataFrame.
							# Update the Value at that row to the new sum – of that old Value at that row plus the new value
							flows.at[flow.index.to_list()[0],'Value'] = float(flow['Value']) + value
				else: # Add to "trade from non-producing countries"
					if importer in refprod.keys():
						imp = importer + "_ref_poss"
						flow = flows.loc[(flows["Source"] == TFCM) & (flows["Target"] == imp)]
						if flow.empty:
							flows.loc[fi] = [TFCM,imp,value]
							fi += 1
						else:
							flows.at[flow.index.to_list()[0],'Value'] = float(flow['Value']) + value
					else:
						# We don't care about the trade from non-producing countries to non-refining producing countries
						pass

	# Double check that the URMS covers all refining countries
	for country,value in refprod.items():
		ref_poss_out = sum(flows[flows["Source"] == country + "_ref_poss"]["Value"])
		ref_poss_in = sum(flows[flows["Target"] == country + "_ref_poss"]["Value"])
		diff = ref_poss_in - ref_poss_out
		if diff > 0:
			# Check to make sure that it doesn't exist
			crp = country + "_ref_poss"
			cr = country + "_ref"
			flow = flows.loc[(flows["Source"] == crp ) & (flows["Target"] == cr)]
			if flow.empty:
				flows.loc[fi] = [crp,cr,diff]
				fi += 1
		else:
			# Check to make sure that it doesn't exist
			crp = country + "_ref_poss"
			flow = flows.loc[(flows["Source"] == (URMS + "_mine") ) & (flows["Target"] == crp)]
			if flow.empty:
				flows.loc[fi] = [URMS + "_mine",crp,-diff]
				fi += 1

	# print(flows.to_string())

	# Sankey format inputs
	labels = []
	sources = [] 
	targets = []
	values = []

	for index,flow in flows.iterrows():
		s = flow["Source"]
		t = flow["Target"]
		v = flow["Value"]

		if s not in labels:
			labels.append(s)
		if t not in labels:
			labels.append(t)
		sources.append(labels.index(s))
		targets.append(labels.index(t))
		values.append(v)

	# Edit labels to only do country names
	nlabels = []
	for lab in labels:
		p = lab.find("_") # p for place
		if p != -1:
			nlabels.append(lab[:p])
		else:
			nlabels.append(lab)

	if label == "Shorten":
		labels = commonname(nlabels)
	elif label is None:
		labels = ["" for a in range(len(labels))]

	# Fix colors based on labels
	if make_color: 
		ncolor = []
		for lab in nlabels:
			if lab not in COLORS:
				ncolor.append("#CCCCCC")
			else:
				ncolor.append(COLORS[lab])

		lcolor = []
		for source in sources:
			if nlabels[source] not in COLORS:
				lc = "#CCCCCC"
			else:
				lc = COLORS[nlabels[source]]

			col = hex2rgba(lc)
			col.append(0.4)
			lcolor.append("rgba" + str(tuple(col)))
	else:
		ncolor = "blue"
		lcolor = None

	if save:
		flows.to_csv(material+"_Sankey_data.csv",index=False)

	if plotflag:
		fig = go.Figure(data=[go.Sankey(
			node = dict(
				pad = 15,
				thickness = 20,
				line = dict(color = "black", width = 0.5),
				label = labels,
				customdata = nlabels,
				color = ncolor,
				# hovertemplate="%{customdata}<extra></extra>",
			),
			link = dict(
				source = sources, # indices for source
				target = targets, # indices for target
				value = values, # value of flows
				color = lcolor, # color of flows
			),
			arrangement = "freeform"
			)])

		fig.update_layout(title_text="Flows of " + material + " for year " + str(year), font_size=10)
		# fig.update_layout(hovermode = 'x')
		fig.show()


if __name__ == '__main__':
	PLOT = True
	COMBINE_CATH = True
	MAKE_COLOR = True
	LABEL = None # None = no labels, 'Shorten': shorten to first underline, 'Other' = raw labels
	SAVE = True
	YEAR = 2020
	COLORS = {"China": "#E81313", "Australia": "#DB05AA", "Russian Federation": "#B7B7B7", 
				"Indonesia": "#53C55E", "Congo, Democratic Republic of the": "#028573", 
				"South Africa": "#773F05", "Japan": "#FB9431", "Korea, Republic of": "#6D9EEB", 
				"Argentina": "#F6B50C","Chile": "#008A03", "United States of America": "#635EFF", 
				"Canada": "#01FFFF", "Brazil": "#009639", 
				"Portugal": "#016201", "Zimbabwe": "#056002", "Belgium": "#C8102E", "Finland": "#002F6C", 
				"India": "#FF9933", "Madagascar": "#F2D2BD", "Morocco": "#C1272D",
				"Norway": "#BA0C2F", "Zambia": "#FFC0CB", "Cuba": "#ADD8E6", "Papua New Guinea": "#FFCD00",
				"Philippines": "#FFD580", "France": "#ED2939", "United Kingdom": "#012169", 
				"New Caledonia": "#30D5C8", "Colombia": "#FFCD00", "Greece": "#001489", "Spain": "#AA151B", 
				"Myanmar": "#FFCD00", "Côte d'Ivoire": "#FF8200", "Gabon": "#009E60", "Georgia": "#DA291C", 
				"Ghana": "#EF3340", "Kazakhstan": "#00AFCA", "Malaysia": "#0032A0", "Mexico": "#006341", 
				"Ukraine": "#0057B7", "Viet Nam": "#C8102E",
				"East Asia": "#F8C69F", "Africa": "#3E6E48", "North America": "#B6133B", 
				"Missing": "#CCCCCC", "Other": "#4B535D", 
				"LFP": "#000086", "NCM": "#000086", "NCA": "#000086", "LMO": "#000086", "LCO": "#000086"}

	# mat = "Lithium" # Lithium, Nickel, Cobalt, Manganese
	# mat = "Cobalt"
	# mat = "Manganese"
	mat = "Phosphorus"
	sankey(PLOT,YEAR,mat,REGIONS,COMBINE_CATH,MAKE_COLOR,LABEL,SAVE)
	# for mat in ["Nickel","Cobalt","Manganese"]:
	# for mat in ["Lithium","Nickel","Cobalt","Manganese"]:
	# 	sankey(PLOT,YEAR,mat,REGIONS,COMBINE_CATH,MAKE_COLOR,LABEL,SAVE)
	








