## SK WASTE SCRAPPER:

## Summary:

The partial aims of the attempt were:
1. Find a faster way to download data covering annual waste production and managment at SK NUTS3 and SK LAU1.
2. Based on the combination of Aim 1's outcomes and INSPIRE dataset (SK Protected sites) find a way to identify if district with higher percentage of their are covered with protected sites have lower waste produciton.
3. Based on copernicus datasets (eg. Carbon dioxide data from 2002 to present derived from satellite sensors, CAMS Regional Air Quality etc.) identify if waste production has impact on variables (eg. air polution, CO2, Methane etc.).

## Motivation a Target user groups:

The main aim was to use the partial aims' outcomes (listed below) for:
1. Communication with citizens about the impacts of waste production on their living conditions.
2. Creating an easier access to the listed data for non-programers, but still relevant stakeholders:
	a. local public administrators,
	b. academia and environmental researchers.

## Results:
SPOILER ALERT1: Since it was the first time that one of the authors(C) met with NetCDF, copernicus data has been postponed till proper self-tutoring.
SPOILER ALERT2: ST_UNION on the INSPIRE SK protected_sites has not yet finnished (My mistake)

1. sk_lau1_waste_scrapper.py 
	For using (default setting dumps to csv):
	a. add sql_engine.py or drop result to csv
	b. chose type of waste category by calling the function (lines xxxx - xxxx)

# sk_lau1_waste_scrapper: 

a. scraps data on waste from the Slovak Ministry of Environment's Partial Monitoring System of Waste @ http://cms.enviroportal.sk/odpady/verejne-informacie.php? with official sk nuts 3 and lau 1 id and in annual 'series'

b. gives the user to opportunity to dump:
	b1: to sql database with geom,
	b3: csv.

# posts/sk_lau1_waste_scrapper:
A Simple Django app in a simpler template with each waste category represented by a button, that allows the user to download correspondent waste category for all available years and regions at once into .CSV 2 in 60 seconds
Usage:
Unpack posts.rar in the same directory as the other file

pip install --user posts/dist/posts-0.1.tar.gz

- works on locahost just fine,
- works fine on pythonanywhere with a paid account.

#COLUMNS ABBREVIATIONS:
#r_material MEANS material valuation -> column: Zhodnocovonie materiálové
#r_energetic  MEANS  energetic valuation -> column: Zhodnocovanie energetické
#r_other MEANS other valuation -> column: Zhodnocovanie ostatné 
#d_landfilling MEANS  disposal by landfilling -> column: Zneškodňovanie skládkovaním
#d_non_energy_combustion MEANS disposal by disposal by combsution without energetic valuation -> column Zneškodňovanie bez energetického využitia
#d_other MEANS other type of disposal -> column: Zneškodňovanie ostatné
#o_managed MEANS other type of management -> column: Iný spôsob nakladania
#total MEAS total volume of waste ->  column: Spolu

ips_xx_ha = size of protected areas with a date of legal foundation in hectares
Ips_xx_pct = pct coverage of the district by protected sites with a date of legal foundation
Ips_nlf_ha = size of protected areas without a date of legal foundation in hectares 
t_ips_xx_ha = ips_xx_ha + _ips_nlf_ha
