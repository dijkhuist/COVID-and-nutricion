# -*- coding: utf-8 -*-
"""
This python program was written to perform basic statistics on covid patient information provided by 
Dutch hospitals.
"""

# Import libraries and set specific options
import pandas as pd


###########################################
###                                     ###
###     Get, check and prep data.       ###
###                                     ###
###########################################

# Retrieve data from csv files as pandas dataframes
df1_hvdt = pd.read_csv('HOEVEELHEID_VOEDING_DATA_TABLE.csv')
df2_iddt = pd.read_csv('INTUBATIE_DATUMS_DATA_TABLE.csv')
df3_mdt = pd.read_csv('MEETGEGEVENS_DATA_TABLE.csv')
df4_pcvdv = pd.read_csv('PATIENT_CALORIEN_V_DATA_VIEW.csv')
df5_pdt = pd.read_csv('PATIENTEN_DATA_TABLE.csv')
df6_spojnvdv = pd.read_csv('SAMENVATTING_PATIENT_OVERLEDEN_JA_NEE_V_DATA_VIEW.csv')
df7_sdt = pd.read_csv('SONDES_DATA_TABLE.csv')
df8_svdt = pd.read_csv('SOORT_VOEDING_DATA_TABLE.csv')

# Inspect data
# print("---df1------------------------------------------------------")
# print(df1_hvdt.iloc[0,:])
# # ID, PATIENT_ID, MEETDATUM, VOEDING_ML_24, SOORT_VOEDING_ID
# print("---df2------------------------------------------------------")
# print(df2_iddt.iloc[0,:])
# # PATIENT_ID, INTUBATIE_DATUM, ID
# print("---df3------------------------------------------------------")
# print(df3_mdt.iloc[0,:])
# # PATIENT_ID, MEETDATUM, VC02_MLMIN, EE_BEADEMINGSMACH, VOEDING_ML24H, 
# # MAAGRETENTIE_ML24H, PROPOFOL_ML24H, BUIKLIGGING, ID
# print("---df4------------------------------------------------------")
# print(df4_pcvdv.iloc[0,:])
# # PATIENT_ID,MEETDATUM,LIGDAG,LIGTIJD,CALORIEN,EE_BEADEMINGSMACH,GEWICHT,
# # GESLACHT,LENGTE,LEEFTIJD,APACHE_IV_SCORE,BMI,
# # BEREKENDE_BENODIGDE_CALORIEN,IN_LEVEN_3_MAANDEN,IN_LEVEN_6_MAANDEN
# print("---df5------------------------------------------------------")
# print(df5_pdt.iloc[0,:])
# # PATIENT_ID,BRUIKBAAR,LIGTIJD,LEEFTIJD,GESLACHT,LENGTE,GEWICHT,
# # APACHE_IV_SCORE,IN_LEVEN_3_MAANDEN,IN_LEVEN_6_MAANDEN
# print("---df6------------------------------------------------------")
# print(df6_spojnvdv.iloc[0:5,:])
# # AANTAL_JA,APACHE_SCORE_JA,LEEFTIJD_JA,GEWICHT_JA,BMI_JA,AANTAL_NEE,
# # APACHE_SCORE_NEE,LEEFTIJD_NEE,GEWICHT_NEE,BMI_NEE
# # Ignore df6? It has just one row
# print("---df7------------------------------------------------------")
# print(df7_sdt.iloc[0,:])
# # PATIENT_ID,MEETDATUM,SOORT_SONDE,ID
# print("---df8------------------------------------------------------")
# print(df8_svdt.iloc[0,:])
# # ID,PRODUCTCODE,PRODUCTNAAM,ML_CAL
# print("------------------------------------------------------------")
# print()

# print("---df1------------------------------------------------------")
# print(df1_hvdt.dtypes)
# print("---df2------------------------------------------------------")
# print(df2_iddt.dtypes)
# print("---df3------------------------------------------------------")
# print(df3_mdt.dtypes)
# print("---df4------------------------------------------------------")
# print(df4_pcvdv.dtypes)
# print("---df5------------------------------------------------------")
# print(df5_pdt.dtypes)
# print("---df6------------------------------------------------------")
# print(df6_spojnvdv.dtypes)
# print("---df7------------------------------------------------------")
# print(df7_sdt.dtypes)
# print("---df8------------------------------------------------------")
# print(df8_svdt.dtypes)
# print("------------------------------------------------------------")
# print()

# df1 MEETDATUM, df2 INTUBATIE_DATUM, df3 MEETDATUM, df4 MEETDATUM, df7 MEETDATUM need to be adjusted to proper dates
# print('Before adjusting date time columns')
# print("df1:", df1_hvdt['MEETDATUM'].dtypes)
# print("df2:", df2_iddt['INTUBATIE_DATUM'].dtypes)
# print("df3:", df3_mdt['MEETDATUM'].dtypes)
# print("df4:", df4_pcvdv['MEETDATUM'].dtypes)
# print("df7:", df7_sdt['MEETDATUM'].dtypes)
df1_hvdt['MEETDATUM'] = pd.to_datetime(df1_hvdt['MEETDATUM'], format='%d-%b-%y')
df2_iddt['INTUBATIE_DATUM'] = pd.to_datetime(df2_iddt['INTUBATIE_DATUM'], format='%d-%b-%y')
df3_mdt['MEETDATUM'] = pd.to_datetime(df3_mdt['MEETDATUM'], format='%d-%b-%y')
df4_pcvdv['MEETDATUM'] = pd.to_datetime(df4_pcvdv['MEETDATUM'], format='%d-%b-%y')
df7_sdt['MEETDATUM'] = pd.to_datetime(df7_sdt['MEETDATUM'], format='%d/%m/%Y')
# print('After adjusting date time columns')
# print("df1:", df1_hvdt['MEETDATUM'].dtypes)
# print("df2:", df2_iddt['INTUBATIE_DATUM'].dtypes)
# print("df3:", df3_mdt['MEETDATUM'].dtypes)
# print("df4:", df4_pcvdv['MEETDATUM'].dtypes)
# print("df7:", df7_sdt['MEETDATUM'].dtypes)

#######################################################################################
###                                                                                 ###
###     Merge the dfs that are needed to retrieve the requested information         ###
###     df2(?), df3, df4 and df5 seem to contain the info needed                    ###
###     ID and PATIENT_ID are not the same!                                         ###
###                                                                                 ###
#######################################################################################

###     Assumption: MEETDATUM is altijd na intubatie datum. 
###     Dus als er 21 MEETDATUM punten zijn die geen dag overslaan dan is 
###     dat alles wat nodig is. Dus df2 is niet nodig.

m1 = pd.merge(df3_mdt, df4_pcvdv)
m2 = pd.merge(m1, df5_pdt)
m2 = m2.sort_values(by=["PATIENT_ID", "MEETDATUM"])
#print("------------------------------------------------------------------------------")
#print(m2.iloc[0,:])
#print("------------------------------------------------------------------------------")

# Drop the patients with missing info in the columns "LEEFIJD", "GESLACHT" en "BMI"
m2 = m2[m2['BMI'].notna()]
m2 = m2[m2['LEEFTIJD'].notna()]
m2 = m2[m2['GESLACHT'].notna()]
m2 = m2[m2['IN_LEVEN_3_MAANDEN'].notna()]
m2 = m2[m2['EE_BEADEMINGSMACH'].notna()]

# Set "IN_LEVEN_6_MAANDEN" to nee if "IN_LEVEN_3_MAANDEN" == nee
m2.loc[m2["IN_LEVEN_3_MAANDEN"] == 'nee', "IN_LEVEN_6_MAANDEN"] = "nee"

#m2.to_csv("test.csv", index=False)

# 
#######################################################################################
###                                                                                 ###
###     Information that is requested                                               ###
###                                                                                 ###
###     1:  number of individuals?                                                  ###
###     2:  Age (mean, range)                                                       ###
###     3:  Male sex (n, %)                                                         ###
###     4:  BMI (mean, range)                                                       ###
###     5:  BMI > 30 (%)                                                            ###
###     6:  Ventilator days (21-day study period only)(mean, sd)                    ###
###     7:  Mortality (21-day study period only)(n, %)                              ###
###     8:  Mortality (hospital mortality)(n, %)                                    ###
###                                                                                 ###
###     9:  Measured REE in absolute kCal/day (all patients) (median, IQR)          ###
###     10: Measured REE kCal/kg actual BW (non-obese, BMI < 30) (median, IQR)      ###
###     11: Measured REE kCal/kg actual BW (obese, BMI > 30) (median, IQR)          ###
###     12: Measured REE kCal/kg adjusted BW (obese, BMI > 30) (median, IQR)        ###
###     13: Measured REE kCal/kg actual BW (all patients) (median, IQR)             ###
###     14: Measured REE kCal/kg actual BW (all patients) (median, IQR)             ###
###                                                                                 ###
###     15: Use of prone positioning (%) (mean, sd)                                 ###
###     16: Use of paralysis with neuromuscular blocker (%) (mean, sd)              ###
###                                                                                 ###
#######################################################################################

# Subgroup based on info needed
# For the first 8 we need only one row of info because these variables are not time dependend
# Assuming "in_leven_<>" are both constant
# 6, ventilator days, is "LIGTIJD" which appears to be the sum of "LIGDAG" 
# and is therefore constant for each row linked to a specific patient_id
one_row_per_patient = m2.groupby('PATIENT_ID').first().reset_index()
#m2.loc[m2["PATIENT_ID"] == 139].to_csv("test.csv", index=False)
#m2.loc[m2["PATIENT_ID"] == 147].to_csv("test.csv", index=False)
#m2.loc[m2["PATIENT_ID"] == 197].to_csv("test.csv", index=False)
#m2.loc[m2["PATIENT_ID"] == 227].to_csv("test.csv", index=False)

#one_row_per_patient.to_csv("test.csv", index=False)

print("--- Retrieving the first 8 requested variables -------------------------------")
print("------------------------------------------------------------------------------")
print("Collecting the summary info for the table and further calculations")
print(one_row_per_patient[["PATIENT_ID","LEEFTIJD","BMI","LIGTIJD"]].describe())
nPatients = one_row_per_patient["PATIENT_ID"].unique().shape[0]
print("------------------------------------------------------------------------------")
gender = one_row_per_patient["GESLACHT"].value_counts()
nMale = gender.loc[['m']][0]
print("Number of patients of each gender:")
print(gender)
print("So out of the ", nPatients, ",", (nMale/nPatients)*100, "% is male")
print("------------------------------------------------------------------------------")
nBMIHoog = one_row_per_patient.loc[one_row_per_patient["BMI"] > 30.0][["PATIENT_ID","BMI"]]
print("Number of patients with an BMI higher than 30:", nBMIHoog.shape[0], ", which is", (nBMIHoog.shape[0]/nPatients)*100, "% of the patients in this study.")
print("------------------------------------------------------------------------------")
mortality3 = one_row_per_patient["IN_LEVEN_3_MAANDEN"].value_counts()
dead3 = mortality3.loc[['nee']][0] #"IN_LEVEN" = nee => dead within three months
# (?) "IN_LEVEN_6_MAANDEN" because there are only 24 data points
mortality6 = one_row_per_patient["IN_LEVEN_6_MAANDEN"].value_counts()
dead6 = mortality6.loc[['nee']][0]
print(mortality3)
print("So out of the ", nPatients, ",", (dead3/nPatients)*100, "% died within 3 months")
print("------------------------------------------------------------------------------")
print(mortality6)
print("So out of the ", nPatients, ", atleast", (dead6/nPatients)*100, "% died within 6 months")
print("------------------------------------------------------------------------------")
print()
print()


print("--- Retrieving the REE variables ---------------------------------------------")
print("------------------------------------------------------------------------------")
# First add column EE/per day (one day per row so describe would be enough?)
# Nope, sum EE for each patient and devide by number of ventilator days for that person
# Then do describe for all patients in the requested time frame

# Create new columns to store EE_SUM and EE_PATIENT_AVERAGE for each patient
# Create new columns to store EE/BODYWEIGHT and EE/ADJUSTED BODY WEIGHT
m2["EE_SUM"] = m2.groupby("PATIENT_ID")["EE_BEADEMINGSMACH"].transform('sum')
m2["EE_PATIENT_DAY_AVERAGE"] = m2["EE_SUM"] / m2["LIGTIJD"]
m2["EE_PATIENT_BW"] = m2["EE_BEADEMINGSMACH"] / m2["GEWICHT"]

# Before the adjusted bw can be calculated, the ideal bw needs to be calculated
# First version uses the formula as given on http://www.ic-hints.nl/Berekeningen_N/Voeding/Espen/Sondevoeding_Espen.php
# The ideal bw depends on gender
m2["IDEAL_BW"] = 0.0
m2.loc[m2["GESLACHT"] == 'm', 'IDEAL_BW'] = 0.9 * (m2["LENGTE"] - 100.0)
m2.loc[m2["GESLACHT"] == 'v', 'IDEAL_BW'] = 0.9 * (m2["LENGTE"] - 106.0)
m2["ADJUSTED_BW"] = m2["IDEAL_BW"] + 0.2*(m2["GEWICHT"] - m2["IDEAL_BW"])
m2["EE_PATIENT_ADJUSTED_BW"] = m2["EE_BEADEMINGSMACH"] / m2["ADJUSTED_BW"]
# Now the EE/Adjuste BW can be calculated

m2.to_csv('test.csv', index=False)

# Now create new subsets based on number of days on ventilator
days0_7 = m2.loc[m2["LIGTIJD"] < 8].copy()
day8 = m2.loc[m2["LIGTIJD"] > 7].copy()
days8_14 = day8.loc[day8["LIGTIJD"] < 15].copy()
day15 = m2.loc[m2["LIGTIJD"] > 14].copy()
days15_21 = day15.loc[day15["LIGTIJD"] < 22].copy()
# print(days0_7["LIGTIJD"].describe())
# print("------------------------------------------------------------------------------")
# print(days8_14["LIGTIJD"].describe())
# print("------------------------------------------------------------------------------")
# print(days15_21["LIGTIJD"].describe())

print("--- EE per day all patients in data set ----------------------------------------")
print(m2.groupby('PATIENT_ID').first().reset_index()["EE_PATIENT_DAY_AVERAGE"].describe())
print("--- EE per day all patients with 0-7 days of data ------------------------------")
print(days0_7.groupby('PATIENT_ID').first().reset_index()["EE_PATIENT_DAY_AVERAGE"].describe())
print("--- EE per day all patients with 8-14 days of data -----------------------------")
print(days8_14.groupby('PATIENT_ID').first().reset_index()["EE_PATIENT_DAY_AVERAGE"].describe())
print("--- EE per day all patients with 15-21 days of data ----------------------------")
print(days15_21.groupby('PATIENT_ID').first().reset_index()["EE_PATIENT_DAY_AVERAGE"].describe())
print("--------------------------------------------------------------------------------")
print()

print("--- EE per kg body weight all patients in data set -----------------------------")
print(m2["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight all patients with 0-7 days of data -------------------")
print(days0_7["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight all patients with 8-14 days of data ------------------")
print(days8_14["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight all patients with 15-21 days of data -----------------")
print(days15_21["EE_PATIENT_BW"].describe())
print("--------------------------------------------------------------------------------")
print()

print("--- EE per kg body weight for patients with BMI < 30 and with 0-7 days of data -")
print(days0_7.loc[days0_7["BMI"] < 30]["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight for patients with BMI < 30 and with 8-14 days of data ")
print(days8_14.loc[days8_14["BMI"] < 30]["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight for patients with BMI < 30 and with 15-21 days of data")
print(days15_21.loc[days15_21["BMI"] < 30]["EE_PATIENT_BW"].describe())
print("--------------------------------------------------------------------------------")
print()

print("--- EE per kg body weight for patients with BMI >= 30 and with 0-7 days of data ")
print(days0_7.loc[days0_7["BMI"] >= 30]["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight for patients with BMI >= 30 and  with 8-14 days of data")
print(days8_14.loc[days8_14["BMI"] >= 30]["EE_PATIENT_BW"].describe())
print("--- EE per kg body weight for patients with BMI >= 30 and  with 15-21 days of data")
print(days15_21.loc[days15_21["BMI"] >= 30]["EE_PATIENT_BW"].describe())
print("--------------------------------------------------------------------------------")
print()

print("--- EE per kg adjusted body weight for patients with BMI >= 30 and with 0-7 days of data")
print(days0_7.loc[days0_7["BMI"] >= 30]["EE_PATIENT_ADJUSTED_BW"].describe())
print("--- EE per kg adjusted body weight for patients with BMI >= 30 and with 8-14 days of data")
print(days8_14.loc[days8_14["BMI"] >= 30]["EE_PATIENT_ADJUSTED_BW"].describe())
print("--- EE per kg adjusted body weight for patients with BMI >= 30 and with 15-21 days of data")
print(days15_21.loc[days15_21["BMI"] >= 30]["EE_PATIENT_ADJUSTED_BW"].describe())
print("--------------------------------------------------------------------------------")
print()

# Time for use of prone position (buikligging)
print("--- Prone or not prone ---------------------------------------------------------")
ligging = m2["BUIKLIGGING"].value_counts()
buik = ligging.loc[['buik']][0]
totaal = ligging.loc[['buik']][0] + ligging.loc[['rug']][0]
print(ligging)
print("Only considering buik or rug option gives a total of", totaal, ", making it", (buik/totaal)*100, "% being prone.")


###### OLD CODE

# Only work with patients who have 21 days of data after intubation
# ###     Assumption: MEETDATUM is altijd na intubatie datum.
# print("---------------------------------------------------------------------------------------")
# print(list(m2.columns))
# print("---group1------------------------------------------------------------------------------------")
# group1 = m2.groupby(["PATIENT_ID"], as_index=False)["MEETDATUM"].aggregate('count')
# print(group1)
# print("---p21m------------------------------------------------------------------------------------")
# p21m = group1.loc[group1["MEETDATUM"] > 20][["PATIENT_ID","MEETDATUM"]].copy()
# print(p21m)
# print("There are only", p21m.shape[0], "patients with 21 or more MEETDATUM entries")
# print("---------------------------------------------------------------------------------------")
# p21m['seq'] = False
# #print(p21m)
# #print("---------------------------------------------------------------------------------------")

# #Loop over the merged data frame to check if data is sequential for the patients in p21m
# from datetime import timedelta
# for patient in p21m["PATIENT_ID"]:
#     #print("Checking if the dates are sequential for patient:", patient)
#     # Get the dates and sort them
#     dates = m2[m2["PATIENT_ID"] == patient]["MEETDATUM"].sort_values()
#     #print(dates)
    
#     start = 0
#     x = 1  
#     for x in range(1,len(dates)):
#         #print('start =', start)
#         #print('x = ', x)
#         if (dates.iloc[start] + timedelta(days=(x-start))) != dates.iloc[(x)]:
#             #print((dates.iloc[start] + timedelta(days=(x-start))), dates.iloc[(x)])
#             print("Break in sequence. Sequence is", x-start, "days long. Updating start to", x, "to continu.")
#             start = x
#     #print("Final sequence was", x-start+1, "day(s) long.")
#     if x-start+1 >= 21:
#         p21m.loc[p21m["PATIENT_ID"]==patient, 'seq'] = True
#     #print("-------------------------------------------------------------------------------")

# print(p21m)
# print("---------------------------------------------------------------------------------------")

# # Drop the patients with less than 21 days sequential
# p21m.drop(p21m[p21m['seq'] == False].index, inplace = True)
# # Retrieve all data for each patient with 21 or more days
# p21 = m2[m2["PATIENT_ID"].isin(p21m["PATIENT_ID"])].sort_values(by=["PATIENT_ID", "MEETDATUM"]).copy()
# print(p21)
# print("--------------------------------------------------------------------------------------")
# print(p21["BRUIKBAAR"].unique())



### Check if the patient ids are the same in all the files I am about to use!
### 196 is missing in df3 and df4
# print("DF1 # unique patient_id's", df1_hvdt["PATIENT_ID"].unique().shape)
# print("DF2 # unique patient_id's", df2_iddt["PATIENT_ID"].unique().shape)
# print("DF3 # unique patient_id's", df3_mdt["PATIENT_ID"].unique().shape)
# print("DF4 # unique patient_id's", df4_pcvdv["PATIENT_ID"].unique().shape)
# print("DF5 # unique patient_id's", df5_pdt["PATIENT_ID"].unique().shape)
# # print("DF7 # unique patient_id's", df7_sdt["PATIENT_ID"].unique().shape)
# print("-------------------------------------------------------------------------------------------")
# df2P = set(df2_iddt["PATIENT_ID"])
# df3P = set(df3_mdt["PATIENT_ID"])
# df4P = set(df4_pcvdv["PATIENT_ID"])
# df5P = set(df5_pdt["PATIENT_ID"])
# print("differences between df2 and df3:", df2P ^ df3P)
# print("differences between df2 and df4:", df2P ^ df4P)
# print("differences between df2 and df5:", df2P ^ df5P)
# print("-------------------------------------------------------------------------------------------")

# df2 has two or more IDs for one patient, how to deal with this?

# merge on PATIENT_ID and when possible, also on MEETDATUM or other elements but never on ID!
# m1 = df2_iddt.merge(df3_mdt, on=["PATIENT_ID"])
# m1 = m1.rename(columns={"ID_x":"ID_df2_iddt", "ID_y":"ID_df3_mdt"})
# print(m1.iloc[0,:])
# print("---------------------------------------------------------------------------------------")
# m2 = pd.merge(df4_pcvdv, m1)#, on=["PATIENT_ID", "MEETDATUM", "EE_BEADEMINGSMACH"])
# print(m2.iloc[0,:])
# print("---------------------------------------------------------------------------------------")
# m3 = pd.merge(m2, df5_pdt)#, on=["PATIENT_ID"])#,'LENGTE', 'GESLACHT', 'IN_LEVEN_3_MAANDEN', 'IN_LEVEN_6_MAANDEN', 'LIGTIJD', 'APACHE_IV_SCORE', 'GEWICHT', 'LEEFTIJD'])
# print(m3.iloc[0,:])
# print("---------------------------------------------------------------------------------------")

# print(list(m2.columns))
# print("------------------")
# print(list(df5_pdt.columns))
# print("------------------")
# print(set(list(m2.columns)).intersection(list(df5_pdt.columns)))

# print("----Getting NaN------------------------------------------------------------------------------------------------")
# print(m3[m3.isna().any(axis=1)])
# print("---------------------------------------------------------------------------------------------------------------")


### Checking date time following thingy
# df = pd.DataFrame({'date': ['3/10/2000', '3/11/2000', '3/12/2000', '3/13/2000', '3/14/2000', '3/16/2000', '3/17/2000', '3/18/2000', '3/19/2000'],'value': [0, 1, 2, 3, 4, 5, 6, 7, 8]})
# df['date'] = pd.to_datetime(df['date'])
# print(df)

# start = 0
# x = 1  
# for x in range(1,len(df['date'])):
#     print('start =', start)
#     print('x = ', x)
#     if (df.iloc[start,0] + timedelta(days=(x-start))) == df.iloc[(x),0]:
#         print((df.iloc[start,0] + timedelta(days=(x-start))), df.iloc[(x),0])
#     else:
#         print((df.iloc[start,0] + timedelta(days=(x-start))), df.iloc[(x),0])
#         print("Break in sequence. Sequence is", x-start, "days long. Updating start to", x, "to continu.")
#         start = x
#     print("--------------------------------------------------------")
# print("Final sequence was", x-start+1, "day(s) long.")        
