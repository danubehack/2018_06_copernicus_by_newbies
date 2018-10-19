#Author: Csaba Sidor
#IT's not the pythonic way, but it does work
#DISCLAIMER: take care of this and any other trash with reponsibilty

#follow the coments, uncomment stuff to do what is desired

#NOTE1: for exporting edit your own sql engine, or whatver is suitable for you
#NOTE2: all values are in tons

#COLUMNS ABBREVIATIONS:
                                                  #r_material MEANS material valuation -> column: Zhodnocovonie materiálové
                                                  #r_energetic  MEANS  energetic valuation -> column: Zhodnocovanie energetické
                                                  #r_other MEANS other valuation -> column: Zhodnocovanie ostatné 
                                                  #d_landfilling MEANS  disposal by landfilling -> column: Zneškodňovanie skládkovaním
                                                  #d_non_energy_combustion MEANS disposal by disposal by combsution without energetic valuation -> column Zneškodňovanie bez energetického využitia
                                                  #d_other MEANS other type of disposal -> column: Zneškodňovanie ostatné
                                                  #o_managed MEANS other type of management -> column: Iný spôsob nakladania
                                                  #total MEAS total volume of waste ->  column: Spolu

#by default -> prints wc_v

import pygeoj
import pandas as pd
import json
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tabulate import tabulate
from pprint import pprint
import numpy as np
from datetime import datetime
pd.set_option('display.max_columns',14)
pd.set_option('display.width', 1500)
import itertools
from datetime import datetime
startTime = datetime.now()
import itertools
from urllib import parse
import functools
from itertools import groupby
from operator import itemgetter






#Data is available for 
year = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
waste_category = ["v", "O", "N", "01", "0101", "010101", "010102", "0103", "010304", "010305", "010306", "010307", "010308", "010309", "010310", "010399", "0104", "010407", "010408", "010409", "010410", "010411", "010412", "010413", "010499", "0105", "010504", "010505", "010506",
                  "010507", "010508", "010599", "02", "0201", "020101", "020102", "020103", "020104", "020106", "020107", "020108", "020109", "020110", "020199", "0202", "020201", "020202", "020203", "020204", "020299", "0203", "020301", "020302", "020303", "020304", "020305", "020399",
                  "0204", "020401", "020402", "020403", "020499", "0205", "020501", "020502", "020599", "0206", "020601", "020602", "020603", "020699", "0207", "020701", "020702", "020703", "020704", "020705", "020799", "03", "0301", "030101", "030104", "030105", "030199", "0302",
                  "030201", "030202", "030203", "030204", "030205", "030299", "0303", "030301", "030302", "030305", "030307", "030308", "030309", "030310", "030311", "030399", "04", "0401", "040101", "040102", "040103", "040104", "040105", "040106", "040107", "040108", "040109", "040199",
                  "0402", "040209", "040210", "040214", "040215", "040216", "040217", "040219", "040220", "040221", "040222", "040299", "05", "0501", "050102", "050103", "050104", "050105", "050106", "050107", "050108", "050109", "050110", "050111", "050112", "050113", "050114", "050115",
                  "050116", "050117", "050199", "0506", "050601", "050603", "050604", "050699", "0507", "050701", "050702", "050799", "06", "0601", "060101", "060102", "060103", "060104", "060105", "060106", "060199", "0602", "060201", "060203", "060204", "060205", "060299", "0603", "060311",
                  "060313", "060314", "060315", "060316", "060399", "0604", "060403", "060404", "060405", "060499", "0605", "060502", "060503", "0606", "060602", "060603", "060699", "0607", "060701", "060702", "060703", "060704", "060799", "0608", "060802", "060899", "0609", "060902",
                    "060903", "060904", "060999", "0610", "061002", "061099", "0611", "061101", "061199", "0613", "061301", "061302", "061303", "061304", "061305", "061399", "07", "0701", "070101", "070103", "070104", "070107", "070108", "070109", "070110", "070111", "070112", "070199", "0702",
                  "070201", "070203", "070204", "070207", "070208", "070209", "070210", "070211", "070212", "070213", "070214", "070215", "070216", "070217", "070299", "0703", "070301", "070303", "070304", "070307", "070308", "070309", "070310", "070311", "070312", "070399", "0704", "070401",
                  "070403", "070404", "070407", "070408", "070409", "070410", "070411", "070412", "070413", "070499", "0705", "070501", "070503", "070504", "070507", "070508", "070509", "070510", "070511", "070512", "070513", "070514", "070599", "0706", "070601", "070603", "070604", "070607",
                  "070608", "070609", "070610", "070611", "070612", "070699", "0707", "070701", "070703", "070704", "070707", "070708", "070709", "070710", "070711", "070712", "070799", "08", "0801", "080111", "080112", "080113", "080114", "080115", "080116", "080117", "080118", "080119",
                  "080120", "080121", "080199", "0802", "080201", "080202", "080203", "080299", "0803", "080307", "080308", "080312", "080313", "080314", "080315", "080316", "080317", "080318", "080319", "080399", "0804", "080409", "080410", "080411", "080412", "080413", "080414", "080415",
                  "080416", "080417", "080499", "0805", "080501", "09", "0901", "090101", "090102", "090103", "090104", "090105", "090106", "090107", "090108", "090110", "090111", "090112", "090113", "090199", "10", "1001", "100101", "100102", "100103", "100104", "100105", "100106", "100107",
                  "100109", "100113", "100114", "100115", "100116", "100117", "100118", "100119", "100120", "100121", "100122", "100123", "100124", "100125", "100126", "100199", "1002", "100201", "100202", "100207", "100208", "100210", "100211", "100212", "100213", "100214", "100215",
                  "100299", "1003", "100302", "100304", "100305", "100308", "100309", "100315", "100316", "100317", "100318", "100319", "100320", "100321", "100322", "100323", "100324", "100325", "100326", "100327", "100328", "100329", "100330", "100399", "1004", "100401", "100402",
                  "100403", "100404", "100405", "100406", "100407", "100409", "100410", "100499", "1005", "100501", "100503", "100504", "100505", "100506", "100508", "100509", "100510", "100511", "100599", "1006", "100601", "100602", "100603", "100604", "100606", "100607", "100609",
                  "100610", "100699", "1007", "100701", "100702", "100703", "100704", "100705", "100707", "100708", "100799", "1008", "100804", "100808", "100809", "100810", "100811", "100812", "100813", "100814", "100815", "100816", "100817", "100818", "100819", "100820", "100899",
                  "1009", "100903", "100905", "100906", "100907", "100908", "100909", "100910", "100911", "100912", "100913", "100914", "100915", "100916", "100999", "1010", "101003", "101005", "101006", "101007", "101008", "101009", "101010", "101011", "101012", "101013", "101014",
                  "101015", "101016", "101099", "1011", "101103", "101105", "101109", "101110", "101111", "101112", "101113", "101114", "101115", "101116", "101117", "101118", "101119", "101120", "101199", "1012", "101201", "101203", "101205", "101206", "101208", "101209", "101210",
                  "101211", "101212", "101213", "101299", "1013", "101301", "101304", "101306", "101307", "101309", "101310", "101311", "101312", "101313", "101314", "101399", "1014", "101401", "11", "1101", "110105", "110106", "110107", "110108", "110109", "110110", "110111", "110112",
                  "110113", "110114", "110115", "110116", "110198", "110199", "1102", "110202", "110203", "110205", "110206", "110207", "110299", "1103", "110301", "110302", "1105", "110501", "110502", "110503", "110504", "110599", "12", "1201", "120101", "120102", "120103", "120104",
                  "120105", "120106", "120107", "120108", "120109", "120110", "120112", "120113", "120114", "120115", "120116", "120117", "120118", "120119", "120120", "120121", "120199", "1203", "120301", "120302", "13", "1301", "130101", "130104", "130105", "130109", "130110",
                  "130111", "130112", "130113", "1302", "130204", "130205", "130206", "130207", "130208", "1303", "130301", "130306", "130307", "130308", "130309", "130310", "1304", "130401", "130402", "130403", "1305", "130501", "130502", "130503", "130506", "130507", "130508",
                  "1307", "130701", "130702", "130703", "1308", "130801", "130802", "130899", "14", "1406", "140601", "140602", "140603", "140604", "140605", "15", "1501", "150101", "150102", "150103", "150104", "150105", "150106", "150107", "150109", "150110", "150111", "1502", "150202",
                  "150203", "16", "1601", "160103", "160104", "160106", "160107", "160108", "160109", "160110", "160111", "160112", "160113", "160114", "160115", "160116", "160117", "160118", "160119", "160120", "160121", "160122", "160199", "1602", "160209", "160210", "160211", "160212",
                  "160213", "160214", "160215", "160216", "1603", "160303", "160304", "160305", "160306", "160307", "1604", "160401", "160402", "160403", "1605", "160504", "160505", "160506", "160507", "160508", "160509", "1606", "160601", "160602", "160603", "160604", "160605", "160606",
                  "1607", "160708", "160709", "160799", "1608", "160801", "160802", "160803", "160804", "160805", "160806", "160807", "1609", "160901", "160902", "160903", "160904", "1610", "161001", "161002", "161003", "161004", "1611", "161101", "161102", "161103", "161104", "161105",
                  "161106", "17", "1701", "170101", "170102", "170103", "170106", "170107", "1702", "170201", "170202", "170203", "170204", "1703", "170301", "170302", "170303", "1704", "170401", "170402", "170403", "170404", "170405", "170406", "170407", "170409", "170410", "170411", "1705",
                  "170503", "170504", "170505", "170506", "170507", "170508", "1706", "170601", "170603", "170604", "170605", "1708", "170801", "170802", "1709", "170901", "170902", "170903", "170904", "179900", "18", "1801", "180101", "180102", "180103", "180104", "180106", "180107",
                  "180108", "180109", "180110", "1802", "180201", "180202", "180203", "180205", "180206", "180207", "180208", "19", "1901", "190102", "190105", "190106", "190107", "190110", "190111", "190112", "190113", "190114", "190115", "190116", "190117", "190118", "190119", "190199",
                  "1902", "190203", "190204", "190205", "190206", "190207", "190208", "190209", "190210", "190211", "190299", "1903", "190304", "190305", "190306", "190307", "190308", "1904", "190401", "190402", "190403", "190404", "1905", "190501", "190502", "190503", "190599", "1906",
                  "190603", "190604", "190605", "190606", "190699", "1907", "190702", "190703", "1908", "190801", "190802", "190805", "190806", "190807", "190808", "190809", "190810", "190811", "190812", "190813", "190814", "190899", "1909", "190901", "190902", "190903", "190904", "190905",
                  "190906", "190999", "1910", "191001", "191002", "191003", "191004", "191005", "191006", "1911", "191101", "191102", "191103", "191104", "191105", "191106", "191107", "191199", "1912", "191201", "191202", "191203", "191204", "191205", "191206", "191207", "191208", "191209",
                  "191210", "191211", "191212", "1913", "191301", "191302", "191303", "191304", "191305", "191306", "191307", "191308", "20", "2001", "200101", "200102", "200103", "200108", "200110", "200111", "200113", "200114", "200115", "200117", "200119", "200121", "200123", "200125",
                  "200126", "200127", "200128", "200129", "200130", "200131", "200132", "200133", "200134", "200135", "200136", "200137", "200138", "200139", "200140", "20014001", "20014002", "20014003", "20014004", "20014005", "20014006", "20014007", "200141", "200199", "2002", "200201",
                  "200202", "200203", "2003", "200301", "200302", "200303", "200304", "200306", "200307", "200308", "200399"]

region = ["1", "2", "3", "4", "5", "6", "7", "8"]


part_1 = "http://cms.enviroportal.sk/odpady/verejne-informacie.php?rok=B-"
part_2 = "&kr="
part_3 = "&kat%5B%5D="

#region = "v"




region_cat = [year, region,  waste_category]
p_rcy_comb = list(itertools.product(*region_cat))
list_of_lists = [list(elem) for elem in p_rcy_comb]
sorted_l = s = sorted(list_of_lists, key = lambda x: (x[-1], x[1]))


lista_url_1 = []
for url in sorted_l:
     lista_url_1.append(part_1 + url[0] + part_2 + url[1]+ part_3 + url[-1])


    


exec(open("D:\\2018_Python_testovanie\\csb\\04_engine_gis_zaloha.py").read())



extract_names = []

def kokocinka(x, y):
     
     def regionky(stuff):
          stuff.rename(columns = \
                            {'Územie': 'region_name',\
                            'Zhodnocov. materiálové[t]':  'wc_' + kat +  '_' + year +  '_' + 'r_material', \
                            'Zhodnocov. energetické[t]':  'wc_' + kat +  '_' + year +  '_' +  'r_energetic', \
                            'Zhodnocov. ostatné[t]': 'wc_' + kat +  '_' + year +  '_' +  'r_other', \
                            'Zneškod. skládkovaním[t]': 'wc_' + kat +  '_' + year +  '_' +  'd_landfilling', \
                            'Zneškod. spaľovaním bez energetic. využitia[t]': 'wc_' + kat +  '_' + year +  '_' +  'd_non_energy_combustion', \
                            'Zneškod. ostatné[t]': 'wc_' + kat +  '_' + year +  '_' + 'd_other', \
                            'Iný spôsob nakladania[t]': 'wc_' + kat +  '_' + year +  '_' +  'o_managed', \
                            'Spolu[t]': 'wc_' + kat +  '_' + year +  '_' +  'total' }, inplace = True)
          stuff.loc[stuff.region_name == 'Bratislava I', 'region_id'] ='101'
          stuff.loc[stuff.region_name == 'Bratislava II', 'region_id'] ='102'
          stuff.loc[stuff.region_name == 'Bratislava III', 'region_id'] ='103'
          stuff.loc[stuff.region_name == 'Bratislava IV', 'region_id'] ='104'
          stuff.loc[stuff.region_name == 'Bratislava V', 'region_id'] ='105'
          stuff.loc[stuff.region_name == 'Malacky', 'region_id'] ='106'
          stuff.loc[stuff.region_name == 'Pezinok', 'region_id'] ='107'
          stuff.loc[stuff.region_name == 'Senec', 'region_id'] ='108'
          stuff.loc[stuff.region_name == 'Dunajská Streda', 'region_id'] ='201'
          stuff.loc[stuff.region_name == 'Galanta', 'region_id'] ='202'
          stuff.loc[stuff.region_name == 'Hlohovec', 'region_id'] ='203'
          stuff.loc[stuff.region_name == 'Piešťany', 'region_id'] ='204'
          stuff.loc[stuff.region_name == 'Senica', 'region_id'] ='205'
          stuff.loc[stuff.region_name == 'Skalica', 'region_id'] ='206'
          stuff.loc[stuff.region_name == 'Trnava', 'region_id'] ='207'
          stuff.loc[stuff.region_name == 'Bánovce nad Bebravou', 'region_id'] ='301'
          stuff.loc[stuff.region_name == 'Ilava', 'region_id'] ='302'
          stuff.loc[stuff.region_name == 'Myjava', 'region_id'] ='303'
          stuff.loc[stuff.region_name == 'Nové Mesto nad Váhom', 'region_id'] ='304'
          stuff.loc[stuff.region_name == 'Partizánske', 'region_id'] ='305'
          stuff.loc[stuff.region_name == 'Považská Bystrica', 'region_id'] ='306'
          stuff.loc[stuff.region_name == 'Prievidza', 'region_id'] ='307'
          stuff.loc[stuff.region_name == 'Púchov', 'region_id'] ='308'
          stuff.loc[stuff.region_name == 'Trenčín', 'region_id'] ='309'
          stuff.loc[stuff.region_name == 'Komárno', 'region_id'] ='401'
          stuff.loc[stuff.region_name == 'Levice', 'region_id'] ='402'
          stuff.loc[stuff.region_name == 'Nitra', 'region_id'] ='403'
          stuff.loc[stuff.region_name == 'Nové Zámky', 'region_id'] ='404'
          stuff.loc[stuff.region_name == 'Šaľa', 'region_id'] ='405'
          stuff.loc[stuff.region_name == 'Topoľčany', 'region_id'] ='406'
          stuff.loc[stuff.region_name == 'Zlaté Moravce', 'region_id'] ='407'
          stuff.loc[stuff.region_name == 'Bytča', 'region_id'] ='501'
          stuff.loc[stuff.region_name == 'Čadca', 'region_id'] ='502'
          stuff.loc[stuff.region_name == 'Dolný Kubín', 'region_id'] ='503'
          stuff.loc[stuff.region_name == 'Kysucké Nové Mesto', 'region_id'] ='504'
          stuff.loc[stuff.region_name == 'Liptovský Mikuláš', 'region_id'] ='505'
          stuff.loc[stuff.region_name == 'Martin', 'region_id'] ='506'
          stuff.loc[stuff.region_name == 'Námestovo', 'region_id'] ='507'
          stuff.loc[stuff.region_name == 'Ružomberok', 'region_id'] ='508'
          stuff.loc[stuff.region_name == 'Turčianske Teplice', 'region_id'] ='509'
          stuff.loc[stuff.region_name == 'Tvrdošín', 'region_id'] ='510'
          stuff.loc[stuff.region_name == 'Žilina', 'region_id'] ='511'
          stuff.loc[stuff.region_name == 'Banská Bystrica', 'region_id'] ='601'
          stuff.loc[stuff.region_name == 'Banská Štiavnica', 'region_id'] ='602'
          stuff.loc[stuff.region_name == 'Brezno', 'region_id'] ='603'
          stuff.loc[stuff.region_name == 'Detva', 'region_id'] ='604'
          stuff.loc[stuff.region_name == 'Krupina', 'region_id'] ='605'
          stuff.loc[stuff.region_name == 'Lučenec', 'region_id'] ='606'
          stuff.loc[stuff.region_name == 'Poltár', 'region_id'] ='607'
          stuff.loc[stuff.region_name == 'Revúca', 'region_id'] ='608'
          stuff.loc[stuff.region_name == 'Rimavská Sobota', 'region_id'] ='609'
          stuff.loc[stuff.region_name == 'Veľký Krtíš', 'region_id'] ='610'
          stuff.loc[stuff.region_name == 'Zvolen', 'region_id'] ='611'      
          stuff.loc[stuff.region_name == 'Žarnovica', 'region_id'] ='612'
          stuff.loc[stuff.region_name == 'Žiar nad Hronom', 'region_id'] ='613'
          stuff.loc[stuff.region_name == 'Bardejov', 'region_id'] ='701'
          stuff.loc[stuff.region_name == 'Humenné', 'region_id'] ='702'
          stuff.loc[stuff.region_name == 'Kežmarok', 'region_id'] ='703'
          stuff.loc[stuff.region_name == 'Levoča', 'region_id'] ='704'
          stuff.loc[stuff.region_name == 'Medzilaborce', 'region_id'] ='705'
          stuff.loc[stuff.region_name == 'Poprad', 'region_id'] ='706'
          stuff.loc[stuff.region_name == 'Prešov', 'region_id'] ='707'
          stuff.loc[stuff.region_name == 'Sabinov', 'region_id'] ='708'
          stuff.loc[stuff.region_name == 'Snina', 'region_id'] ='709'
          stuff.loc[stuff.region_name == 'Stará Ľubovňa', 'region_id'] ='710'
          stuff.loc[stuff.region_name == 'Stropkov', 'region_id'] ='711'
          stuff.loc[stuff.region_name == 'Svidník', 'region_id'] ='712'
          stuff.loc[stuff.region_name == 'Vranov nad Topľou', 'region_id'] ='713'
          stuff.loc[stuff.region_name == 'Gelnica', 'region_id'] ='801'
          stuff.loc[stuff.region_name == 'Košice I', 'region_id'] ='802'
          stuff.loc[stuff.region_name == 'Košice II', 'region_id'] ='803'
          stuff.loc[stuff.region_name == 'Košice III', 'region_id'] ='804'
          stuff.loc[stuff.region_name == 'Košice IV', 'region_id'] ='805'
          stuff.loc[stuff.region_name == 'Košice - okolie', 'region_id'] ='806'
          stuff.loc[stuff.region_name == 'Michalovce', 'region_id'] ='807'
          stuff.loc[stuff.region_name == 'Rožňava', 'region_id'] ='808'
          stuff.loc[stuff.region_name == 'Sobrance', 'region_id'] ='809'
          stuff.loc[stuff.region_name == 'Spišská Nová Ves', 'region_id'] ='810'
          stuff.loc[stuff.region_name == 'Trebišov', 'region_id'] ='811'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Bratislavský kraj', 'region_id'] ='1'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Trnavský kraj', 'region_id'] ='2'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Trenčiansky kraj', 'region_id'] ='3'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Nitriansky kraj', 'region_id'] ='4'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Žilinský kraj', 'region_id'] ='5'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Banskobystrický kraj', 'region_id'] ='6'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Prešovský kraj', 'region_id'] ='7'
          stuff.loc[stuff.region_name == 'Produkcia odpadov za Košický kraj', 'region_id'] ='8'
          stuff.drop_duplicates(keep = 'first', inplace=True)
     list_tables = []
     for url in lista_url_1[x:y]:
                            
               year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
               kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
               kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
               df_1 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
               print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
               regionky(df_1)
               list_tables.append(df_1)
               final_df_1 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)
               
               if len(final_df_1.columns) == 98:
                    
                    extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))      
                    list_tables = []
                    x = x + 12
                    y = y +12
                    for url in lista_url_1[x:y]:
                         year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                         kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                         kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                         df_2 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                         print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                         regionky(df_2)
                         list_tables.append(df_2)
                         final_df_2 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)
                         
                         if len(final_df_2.columns) == 98:
                              
                              extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))      
                              list_tables = []
                              x =x + 12
                              y = y + 12
                              for url in lista_url_1[x:y]:
                                   year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                   kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                   kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                   df_3 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                   print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                   regionky(df_3)
                                   list_tables.append(df_3)
                                   final_df_3 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)
                                   
                                   if len(final_df_3.columns) == 98:
                                        
                                        extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))     
                                        x = x + 12
                                        y = y + 12
                                        list_tables = []
                                        for url in lista_url_1[x:y]:
                                             year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                             kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                             kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                             df_4 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                             print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                             regionky(df_4)
                                             list_tables.append(df_4)
                                             final_df_4 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)
                                             
                                             if len(final_df_4.columns) == 98:
                                                  extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))
                                                  x = x + 12
                                                  y = y + 12
                                                  list_tables = []
                                                  for url in lista_url_1[x:y]:
                                                       year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                                       kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                                       kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                                       df_5 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                                       print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                                       regionky(df_5)
                                                       list_tables.append(df_5)
                                                       final_df_5 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)

                                                       if len(final_df_5.columns) == 98:
                                                            extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))
                                                            x = x + 12
                                                            y = y + 12
                                                            list_tables = []
                                                            for url in lista_url_1[x:y]:
                                                                 year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                                                 kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                                                 kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                                                 df_6 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                                                 print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                                                 regionky(df_6)
                                                                 list_tables.append(df_6)
                                                                 final_df_6 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)

                                                                 if len(final_df_6.columns) == 98:
                                                                      extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))
                                                                      x = x + 12
                                                                      y = y + 12
                                                                      list_tables = []
                                                                      for url in lista_url_1[x:y]:
                                                                           year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                                                           kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                                                           kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                                                           df_7 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                                                           print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                                                           regionky(df_7)
                                                                           list_tables.append(df_7)
                                                                           final_df_7 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)

                                                                           if len(final_df_7.columns) == 98:
                                                                                extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))
                                                                                x = x + 12
                                                                                y = y + 12
                                                                                list_tables = []
                                                                                for url in lista_url_1[x:y]:
                                                                                     year = parse.parse_qs(parse.urlparse(url).query)['rok'][0].strip('B-')
                                                                                     kat = parse.parse_qs(parse.urlparse(url).query)['kat[]'][0]
                                                                                     kr = parse.parse_qs(parse.urlparse(url).query)['kr'][0]
                                                                                     df_8 = pd.DataFrame(pd.read_html(str(BeautifulSoup((requests.get(url)).content, 'lxml').find_all('table')[1]), thousands='.',decimal=',')[0])
                                                                                     print(str(datetime.now() - startTime) + "    " + " RENAMING TABLE COLUMNS TO FLEXIBLE FORMAT  FROM: " + url +  "  !!!DO NOT PANIC!!! " +  str(datetime.now()) )
                                                                                     regionky(df_8)
                                                                                     list_tables.append(df_8)
                                                                                     final_df_8 = functools.reduce(lambda x, y: pd.merge(x, y, on = ['region_name', 'region_id'], how='outer'), list_tables)
                                                                                     if len(final_df_8.columns) == 98:
                                                                                          extract_names.append("w_distr_"  + str(kr) + "_" + str(kat))
                                                                                          final_table = pd.concat([final_df_1, final_df_2, final_df_3, final_df_4, final_df_5, final_df_6, final_df_7, final_df_8],sort= False)
                                                                                          final_table = final_table.sort_values(['region_id'], ascending = True)
                                                                                          #print(final_table)
                                                                                          
                                                                                          export_df = final_table.iloc[:,np.r_[9:10, 0:1, 2:3,11:12,19:20,27:28,35:36,43:44,51:52,59:60,67:68,75:76,83:84,91:92,\
                                                                                                                               4:5,  13:14,  21:22,  29:30,  37:38,  45:46,  53:54,  61:62,  69:70,  77:78,  85:86,  93:94,\
                                                                                                                               7:8,  16:17,  24:25,  32:33,  40:41,  48:49,  56:57,  64:65,  72:73,  80:81,  88:89,  96:97,\
                                                                                                                               1:2,  10:11,  18:19,  26:27,  34:35,  42:43,  50:51,  58:59,  66:67,  74:75,  82:83,  90:91,\
                                                                                                                               5:6,  14:15,  22:23,  30:31,  38:39,  46:47,  54:55,  62:63,  70:71,  78:79,  86:87,  94:95,\
                                                                                                                               6:7,  15:16,  23:24,  31:32,  39:40,  47:48,  55:56,  63:64,  71:72,  79:80,  87:88,  95:96,\
                                                                                                                               3:4,  12:13,  20:21,  28:29,  36:37,  44:45,  52:53,  60:61,  68:69,  76:77,  84:85,  92:93,\
                                                                                                                               8:9, 17:18,  25:26,  33:34,  41:42,  49:50,  57:58,  65:66,  73:74,  81:82,  89:90,  97:98
                                                                                                                               ]]
                                                                                          #print(export_df)
#EXPORT TO YOUR DATABASE: 
                                                                                          #export_df.to_sql(str(kat), engine, if_exists='replace')
#EXPORT TO A CSV FILE                                                                                          
                                                                                          #export_df.to_csv("waste_category_" + str(kat) + ".csv", sep=';', encoding='utf-8')



# IF ONE DESIRES ONLY CERTAIN TYPES OF WASTE PROCESSING TWO OF THE RELEVANT LINES:
                                                                                          #df_r_energetic = final_table.iloc[:,np.r_[9:10, 0:1, 2:3,11:12,19:20,27:28,35:36,43:44,51:52,59:60,67:68,75:76,83:84,91:92]]
                                                                                          #df_r_energetic.to_sql(str(kat) + "_r_energetic", engine, if_exists='replace')
                                                                                          #df_r_energetic.to_csv(str(kat) + "_r_energetic" + ".csv", sep=';', encoding='utf-8')

                                                                                          #df_d_landfilling = final_table.iloc[:,np.r_[9:10, 0:1, 4:5,  13:14,  21:22,  29:30,  37:38,  45:46,  53:54,  61:62,  69:70,  77:78,  85:86,  93:94]]
                                                                                          #df_d_landfilling.to_sql(str(kat) + "_d_landfilling", engine, if_exists='replace')
                                                                                          #df_d_landfilling.to_csv(str(kat) + "_d_landfilling" + ".csv", sep=';', encoding='utf-8')

                                                                                          #df_o_managed = final_table.iloc[:,np.r_[9:10, 0:1, 7:8,  16:17,  24:25,  32:33,  40:41,  48:49,  56:57,  64:65,  72:73,  80:81,  88:89,  96:97]]
                                                                                          #df_o_managed.to_sql(str(kat) + "_o_managed", engine, if_exists='replace')
                                                                                          #df_o_managed.to_csv(str(kat) + "_o_managed" + ".csv", sep=';', encoding='utf-8')

                                                                                          #df_r_material = final_table.iloc[:,np.r_[9:10, 0:1, 1:2,  10:11,  18:19,  26:27,  34:35,  42:43,  50:51,  58:59,  66:67,  74:75,  82:83,  90:91]]
                                                                                          #df_r_material.to_sql(str(kat) + "_r_material", engine, if_exists='replace')
                                                                                          #df_r_material.to_csv(str(kat) + "_r_material" + ".csv", sep=';', encoding='utf-8')

                                                                                          #df_d_non_energy_combustion = final_table.iloc[:,np.r_[9:10, 0:1, 5:6,  14:15,  22:23,  30:31,  38:39,  46:47,  54:55,  62:63,  70:71,  78:79,  86:87,  94:95 ]]
                                                                                          #df_d_non_energy_combustion.to_sql(str(kat) + "_d_non_energy_combustionl", engine, if_exists='replace')
                                                                                          #df_d_non_energy_combustion.to_csv(str(kat) + "_d_non_energy_combustion" + ".csv", sep=';', encoding='utf-8')

                                                                                          #df_r_other = final_table.iloc[:,np.r_[9:10, 0:1, 6:7,  15:16,  23:24,  31:32,  39:40,  47:48,  55:56,  63:64,  71:72,  79:80,  87:88,  95:96]]
                                                                                          #df_r_other.to_sql(str(kat) + "_r_other", engine, if_exists='replace')
                                                                                          #df_r_other.to_csv(str(kat) + "_r_other" + ".csv", sep=';', encoding='utf-8')


                                                                                          #df_d_other = final_table.iloc[:,np.r_[9:10, 0:1,  3:4,  12:13,  20:21,  28:29,  36:37,  44:45,  52:53,  60:61,  68:69,  76:77,  84:85,  92:93]]
                                                                                          #df_d_other.to_sql(str(kat) + "_d_other", engine, if_exists='replace')
                                                                                          #df_d_other.to_csv(str(kat) + "_d_other" + ".csv", sep=';', encoding='utf-8')


                                                                                          df_total = final_table.iloc[:,np.r_[9:10, 0:1, 8:9, 17:18,  25:26,  33:34,  41:42,  49:50,  57:58,  65:66,  73:74,  81:82,  89:90,  97:98]]
                                                                                          #df_total.to_sql(str(kat) + "_total", engine, if_exists='replace')
                                                                                          df_total.to_csv(str(kat) + "_total" + ".csv", sep=';', encoding='utf-8')
                                                                                          print(df_total)


                                                                                          

                                                                                          
                                                                                          

                                                                                          
#!!!CALL KOKOCINKA TO GET THE DESIRED WASTE CATEGORY !!!                   
#kokocinka(0,12) #  01 - Odpady pochádzajúce z geologického prieskumu, ťažby, úpravy a ďalšieho spraco...
#kokocinka(96,108) #  0101 - Odpady z ťažby nerastov
#kokocinka(192,204) #  010101 - O - Odpad z ťažby rudných nerastov
#kokocinka(288,300) #  010102 - O - Odpad z ťažby nerudných nerastov
#kokocinka(384,396) #  0103 - Odpady z fyzikálneho a chemického spracovania rudných nerastov
#kokocinka(480,492) #  010304 - N - Kyslá hlušina zo spracovania sírnej rudy
#kokocinka(576,588) #  010305 - N - Iná hlušina obsahujúca nebezpečné látky
#kokocinka(672,684) #  010306 - O - Hlušina iná ako uvedená v 010304 a 010305
#kokocinka(768,780) #  010307 - N - Iné odpady obsahujúce nebezpečné látky z fyzikálneho a chemickéhospracovania ...
#kokocinka(864,876) #  010308 - O - Prachový a práškový odpad iný ako uvedený v 010307
#kokocinka(960,972) #  010309 - O - Červený kal z výroby oxidu hlinitého iný ako odpady uvedené v 01 03 10
#kokocinka(1056,1068) #  010310 - N - Červený kal z výroby oxidu hlinitého obsahujúci nebezpečné látky, iný ako odp...
#kokocinka(1152,1164) #  010399 - Odpady inak nešpecifikované
#kokocinka(1248,1260) #  0104 - Odpady z fyzikálneho a chemického spracovania nerudných nerastov
#kokocinka(1344,1356) #  010407 - N - Odpady obsahujúce nebezpečné látky z fyzikálneho a chemického spracovania ner...
#kokocinka(1440,1452) #  010408 - O - Odpadový štrk a drvené horniny iné ako uvedené v 010407
#kokocinka(1536,1548) #  010409 - O - Odpadový piesok a íly
#kokocinka(1632,1644) #  010410 - O - Prachový a práškový odpad iný ako uvedený v 010407
#kokocinka(1728,1740) #  010411 - O - Odpady zo spracovania potaše a kamennej soli iné ako uvedené v 010407
#kokocinka(1824,1836) #  010412 - O - Hlušina a iné odpady z prania a čistenia nerastov iné ako uvedené v 010407 a ...
#kokocinka(1920,1932) #  010413 - O - Odpady z rezania a pílenia kameňa iné ako uvedené v 010407
#kokocinka(2016,2028) #  010499 - Odpady inak nešpecifikované
#kokocinka(2112,2124) #  0105 - Vrtné kaly a iné vrtné odpady
#kokocinka(2208,2220) #  010504 - O - Vrtné kaly a odpady z vodných vrtov
#kokocinka(2304,2316) #  010505 - N - Vrtné kaly obsahujúce ropné látky
#kokocinka(2400,2412) #  010506 - N - Vrtné kaly a iné vrtné odpady obsahujúce nebezpečné látky
#kokocinka(2496,2508) #  010507 - O - Vrtné kaly a odpady s obsahom bária iné ako uvedené v 010505 a 010506
#kokocinka(2592,2604) #  010508 - O - Vrtné kaly a odpady s obsahom chloridov iné ako uvedené v 010505 a 010506
#kokocinka(2688,2700) #  010599 - Odpady inak nešpecifikované
#kokocinka(2784,2796) #  02 - Odpady z poľnohospodárstva, záhradníctva, lesníctva, poľovníctva a rybárstva,...
#kokocinka(2880,2892) #  0201 - Odpady z poľnohospodárstva, záhradníctva, lesníctva, poľovníctva a rybárstva
#kokocinka(2976,2988) #  020101 - O - Kaly z prania a čistenia
#kokocinka(3072,3084) #  020102 - O - Odpadové živočíšne tkanivá
#kokocinka(3168,3180) #  020103 - O - Odpadové rastlinné pletivá
#kokocinka(3264,3276) #  020104 - O - Odpadové plasty (okrem obalov)
#kokocinka(3360,3372) #  020106 - O - Zvierací trus, moč a hnoj (vrátane znečistenej slamy), kvapalné odpady, oddel...
#kokocinka(3456,3468) #  020107 - O - Odpady z lesného hospodárstva
#kokocinka(3552,3564) #  020108 - N - Agrochemické odpady obsahujúce nebezpečné látky
#kokocinka(3648,3660) #  020109 - O - Agrochemické odpady iné ako uvedené v 020108
#kokocinka(3744,3756) #  020110 - O - Odpadové kovy
#kokocinka(3840,3852) #  020199 - Odpady inak nešpecifikované
#kokocinka(3936,3948) #  0202 - Odpady z prípravy a spracovania mäsa, rýb a ostatných potravín živočíšneho pô...
#kokocinka(4032,4044) #  020201 - O - Kaly z prania a čistenia
#kokocinka(4128,4140) #  020202 - O - Odpadové živočíšne tkanivá
#kokocinka(4224,4236) #  020203 - O - Materiál nevhodný na spotrebu alebo spracovanie
#kokocinka(4320,4332) #  020204 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(4416,4428) #  020299 - Odpady inak nešpecifikované
#kokocinka(4512,4524) #  0203 - Odpady zo spracovania ovocia, zeleniny, obilnín, jedlých olejov, kakaa, kávy,...
#kokocinka(4608,4620) #  020301 - O - Kaly z prania, čistenia, lúpania, odstreďovania a separovania
#kokocinka(4704,4716) #  020302 - O - Odpady z konzervačných činidiel
#kokocinka(4800,4812) #  020303 - O - Odpady z extrakcie rozpúšťadlami
#kokocinka(4896,4908) #  020304 - O - Látky nevhodné na spotrebu alebo spracovanie
#kokocinka(4992,5004) #  020305 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(5088,5100) #  020399 - Odpady inak nešpecifikované
#kokocinka(5184,5196) #  0204 - Odpady z cukrovarníckeho priemyslu
#kokocinka(5280,5292) #  020401 - O - Zemina z čistenia a prania repy
#kokocinka(5376,5388) #  020402 - O - Uhličitan vápenatý nevyhovujúcej kvality
#kokocinka(5472,5484) #  020403 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(5568,5580) #  020499 - Odpady inak nešpecifikované
#kokocinka(5664,5676) #  0205 - Odpady z priemyslu mliečnych výrobkov
#kokocinka(5760,5772) #  020501 - O - Látky nevhodné na spotrebu alebo spracovanie
#kokocinka(5856,5868) #  020502 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(5952,5964) #  020599 - Odpady inak nešpecifikované
#kokocinka(6048,6060) #  0206 - Odpady z pekárenského a cukrovinkárskeho priemyslu
#kokocinka(6144,6156) #  020601 - O - Materiály nevhodné na spotrebu alebo spracovanie
#kokocinka(6240,6252) #  020602 - O - Odpady z konzervačných činidiel
#kokocinka(6336,6348) #  020603 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(6432,6444) #  020699 - Odpady inak nešpecifikované
#kokocinka(6528,6540) #  0207 - Odpady z výroby alkoholických a nealkoholických nápojov (okrem kávy, čaju a k...
#kokocinka(6624,6636) #  020701 - O - Odpad z prania, čistenia a mechanického spracovania surovín
#kokocinka(6720,6732) #  020702 - O - Odpad z destilácie liehu
#kokocinka(6816,6828) #  020703 - O - Odpad z chemického spracovania
#kokocinka(6912,6924) #  020704 - O - Materiály nevhodné na spotrebu alebo spracovanie
#kokocinka(7008,7020) #  020705 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(7104,7116) #  020799 - Odpady inak nešpecifikované
#kokocinka(7200,7212) #  03 - Odpady zo spracovania dreva a z výroby papiera, lepenky, celulózy, reziva a n...
#kokocinka(7296,7308) #  0301 - Odpady zo spracovania dreva a z výroby reziva a nábytku
#kokocinka(7392,7404) #  030101 - O - Odpadová kôra a korok
#kokocinka(7488,7500) #  030104 - N - Piliny, hobliny, odrezky, odpadové rezivo alebo drevotrieskové/drevovláknité ...
#kokocinka(7584,7596) #  030105 - O - Piliny, hobliny, odrezky, odpadové rezivo alebo drevotrieskové/drevovláknité ...
#kokocinka(7680,7692) #  030199 - Odpady inak nešpecifikované
#kokocinka(7776,7788) #  0302 - Prostriedky na ochranu dreva inak nešpecifikované
#kokocinka(7872,7884) #  030201 - N - Bezhalogénované organické prostriedky na ochranu dreva
#kokocinka(7968,7980) #  030202 - N - Organochlórované prostriedky na ochranu dreva
#kokocinka(8064,8076) #  030203 - N - Organokovové prostriedky na ochranu dreva
#kokocinka(8160,8172) #  030204 - N - Anorganické prostriedky na ochranu dreva
#kokocinka(8256,8268) #  030205 - N - Iné prostriedky na ochranu dreva obsahujúce nebezpečné látky
#kokocinka(8352,8364) #  030299 - Odpady inak nešpecifikované
#kokocinka(8448,8460) #  0303 - Odpady z výroby a spracovania celulózy, papiera a lepenky
#kokocinka(8544,8556) #  030301 - O - Odpadová kôra a drevo
#kokocinka(8640,8652) #  030302 - O - Usadeniny a kaly zo zeleného výluhu (po úprave čierneho výluhu)
#kokocinka(8736,8748) #  030305 - O - Kaly z odstraňovania tlačiarenských farieb pri recyklácii papiera (deinking)
#kokocinka(8832,8844) #  030307 - O - Mechanicky oddelené výmety z recyklácie papiera a lepenky
#kokocinka(8928,8940) #  030308 - O - Odpady z triedenia papiera a lepenky určených na recykláciu
#kokocinka(9024,9036) #  030309 - O - Odpad z vápennej usadeniny
#kokocinka(9120,9132) #  030310 - O - Výmety z vlákien, plnív a náterov z mechanickej separácie
#kokocinka(9216,9228) #  030311 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(9312,9324) #  030399 - Odpady inak nešpecifikované
#kokocinka(9408,9420) #  04 - Odpady z kožiarskeho, kožušníckeho a textilného priemyslu
#kokocinka(9504,9516) #  0401 - Odpady z kožiarskeho a kožušníckeho priemyslu
#kokocinka(9600,9612) #  040101 - O - Odpadová glejovka a štiepenka
#kokocinka(9696,9708) #  040102 - O - Odpad z lúhovania
#kokocinka(9792,9804) #  040103 - N - Odpady z odmasťovania obsahujúce rozpúšťadlá bez kvapalnej fázy
#kokocinka(9888,9900) #  040104 - O - Činiaca brečka obsahujúca chróm
#kokocinka(9984,9996) #  040105 - O - Činiaca brečka neobsahujúca chróm
#kokocinka(10080,10092) #  040106 - O - Kaly najmä zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce c...
#kokocinka(10176,10188) #  040107 - O - Kaly najmä zo spracovania kvapalného odpadu v mieste jeho vzniku neobsahujúce...
#kokocinka(10272,10284) #  040108 - O - Odpadová vyčinená koža (holina, stružliny, odrezky, brúsny prach) obsahujúca ...
#kokocinka(10368,10380) #  040109 - O - Odpady z vypracúvania a apretácie
#kokocinka(10464,10476) #  040199 - Odpady inak nešpecifikované
#kokocinka(10560,10572) #  0402 - Odpady z textilného priemyslu
#kokocinka(10656,10668) #  040209 - O - Odpad z kompozitných materiálov (impregnovaný textil, elastomér, plastomér)
#kokocinka(10752,10764) #  040210 - O - Organické látky prírodného pôvodu (napr. tuky, vosky)
#kokocinka(10848,10860) #  040214 - N - Odpad z apretácie obsahujúci organické rozpúšťadlá
#kokocinka(10944,10956) #  040215 - O - Odpad z apretácie iný ako uvedený v 040214
#kokocinka(11040,11052) #  040216 - N - Farbivá a pigmenty obsahujúce nebezpečné látky
#kokocinka(11136,11148) #  040217 - O - Farbivá a pigmenty iné ako uvedené v 040216
#kokocinka(11232,11244) #  040219 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(11328,11340) #  040220 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(11424,11436) #  040221 - O - Odpady z nespracovaných textilných vlákien
#kokocinka(11520,11532) #  040222 - O - Odpady zo spracovaných textilných vlákien
#kokocinka(11616,11628) #  040299 - Odpady inak nešpecifikované
#kokocinka(11712,11724) #  05 - Odpady zo spracovania ropy, čistenia zemného plynu a pyrolýzneho spracovania ...
#kokocinka(11808,11820) #  0501 - Odpady zo spracovania ropy
#kokocinka(11904,11916) #  050102 - N - Kaly z odsoľovania
#kokocinka(12000,12012) #  050103 - N - Kaly z dna nádrží
#kokocinka(12096,12108) #  050104 - N - Kaly z kyslej alkylácie
#kokocinka(12192,12204) #  050105 - N - Rozliate ropné látky
#kokocinka(12288,12300) #  050106 - N - Kaly z prevádzkarne, zariadenia a z činností údržby
#kokocinka(12384,12396) #  050107 - N - Kyslé dechty
#kokocinka(12480,12492) #  050108 - N - Iné dechty
#kokocinka(12576,12588) #  050109 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(12672,12684) #  050110 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(12768,12780) #  050111 - N - Odpady z čistenia palív obsahujúce zásady
#kokocinka(12864,12876) #  050112 - N - Ropné látky obsahujúce kyseliny
#kokocinka(12960,12972) #  050113 - O - Kaly z napájacej vody pre kotly
#kokocinka(13056,13068) #  050114 - O - Odpady z chladiacich kolón
#kokocinka(13152,13164) #  050115 - N - Použité filtračné hlinky
#kokocinka(13248,13260) #  050116 - O - Odpady s obsahom síry z odsírovania ropy
#kokocinka(13344,13356) #  050117 - O - Bitúmen
#kokocinka(13440,13452) #  050199 - Odpady inak nešpecifikované
#kokocinka(13536,13548) #  0506 - Odpady z pyrolýzneho spracovania uhlia
#kokocinka(13632,13644) #  050601 - N - Kyslé dechty
#kokocinka(13728,13740) #  050603 - N - Ostatné dechty
#kokocinka(13824,13836) #  050604 - O - Odpad z chladiacich kolón
#kokocinka(13920,13932) #  050699 - Odpady inak nešpecifikovan
#kokocinka(14016,14028) #  0507 - Odpady z čistenia a dopravy zemného plynu
#kokocinka(14112,14124) #  050701 - N - Odpady obsahujúce ortuť
#kokocinka(14208,14220) #  050702 - O - Odpady obsahujúce síru
#kokocinka(14304,14316) #  050799 - Odpady inak nešpecifikované
#kokocinka(14400,14412) #  06 - Odpady z anorganických chemických procesov
#kokocinka(14496,14508) #  0601 - Odpady z výroby, spracovania, distribúcie a používania (vsdp) kyselín
#kokocinka(14592,14604) #  060101 - N - Kyselina sírová a kyselina siričitá
#kokocinka(14688,14700) #  060102 - N - Kyselina chlorovodíková
#kokocinka(14784,14796) #  060103 - N - Kyselina fluorovodíková
#kokocinka(14880,14892) #  060104 - N - Kyselina fosforečná a kyselina fosforitá
#kokocinka(14976,14988) #  060105 - N - Kyselina dusičná a kyselina dusitá
#kokocinka(15072,15084) #  060106 - N - Iné kyseliny
#kokocinka(15168,15180) #  060199 - Odpady inak nešpecifikované
#kokocinka(15264,15276) #  0602 - Odpady z vsdp zásad (alkálií)
#kokocinka(15360,15372) #  060201 - N - Hydroxid vápenatý
#kokocinka(15456,15468) #  060203 - N - Hydroxid amónny
#kokocinka(15552,15564) #  060204 - N - Hydroxid sodný a hydroxid draselný
#kokocinka(15648,15660) #  060205 - N - Iné zásady
#kokocinka(15744,15756) #  060299 - Odpady inak nešpecifikované
#kokocinka(15840,15852) #  0603 - Odpady z vsdp solí, ich roztokov a oxidov kovov
#kokocinka(15936,15948) #  060311 - N - Tuhé soli a roztoky obsahujúce kyanidy
#kokocinka(16032,16044) #  060313 - N - Tuhé soli a roztoky obsahujúce ťažké kovy
#kokocinka(16128,16140) #  060314 - O - Tuhé soli a roztoky iné ako uvedené v 060311 a 060313
#kokocinka(16224,16236) #  060315 - N - Oxidy kovov obsahujúce ťažké kovy
#kokocinka(16320,16332) #  060316 - O - Oxidy kovov iné ako uvedené v 060315
#kokocinka(16416,16428) #  060399 - Odpady inak nešpecifikované
#kokocinka(16512,16524) #  0604 - Odpady obsahujúce kovy iné ako uvedené v 0603
#kokocinka(16608,16620) #  060403 - N - Odpady obsahujúce arzén
#kokocinka(16704,16716) #  060404 - N - Odpady obsahujúce ortuť
#kokocinka(16800,16812) #  060405 - N - Odpady obsahujúce iné ťažké kovy
#kokocinka(16896,16908) #  060499 - Odpady inak nešpecifikované
#kokocinka(16992,17004) #  0605 - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(17088,17100) #  060502 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(17184,17196) #  060503 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(17280,17292) #  0606 - Odpady z vsdp chemikálií obsahujúcich síru, zo sírnych chemických procesov a ...
#kokocinka(17376,17388) #  060602 - N - Odpady obsahujúce nebezpečné sulfidy
#kokocinka(17472,17484) #  060603 - O - Odpady obsahujúce sulfidy iné ako uvedené v 060602
#kokocinka(17568,17580) #  060699 - Odpady inak nešpecifikované
#kokocinka(17664,17676) #  0607 - Odpady z vsdp halogénov a halogénových chemických procesov
#kokocinka(17760,17772) #  060701 - N - Odpady z elektrolýzy obsahujúce azbest
#kokocinka(17856,17868) #  060702 - N - Aktívne uhlie z výroby chlóru
#kokocinka(17952,17964) #  060703 - N - Kal sulfátu bárnatého obsahujúci ortuť
#kokocinka(18048,18060) #  060704 - N - Roztoky a kyseliny, napr. kontaktná kyselina
#kokocinka(18144,18156) #  060799 - Odpady inak nešpecifikované
#kokocinka(18240,18252) #  0608 - Odpady z vsdp kremíka a jeho derivátov
#kokocinka(18336,18348) #  060802 - N - Odpady obsahujúce nebezpečné silikóny
#kokocinka(18432,18444) #  060899 - Odpady inak nešpecifikované
#kokocinka(18528,18540) #  0609 - Odpady z vsdp chemikálií obsahujúcich fosfor a z chemických procesov fosforu
#kokocinka(18624,18636) #  060902 - O - Troska obsahujúca fosfor
#kokocinka(18720,18732) #  060903 - N - Odpady z reakcií na báze vápnika obsahujúce nebezpečné látky alebo nimi konta...
#kokocinka(18816,18828) #  060904 - O - Odpady z reakcií na báze vápnika iné ako uvedené v 060903
#kokocinka(18912,18924) #  060999 - Odpady inak nešpecifikované
#kokocinka(19008,19020) #  0610 - Odpady z vsdp chemikálií obsahujúcich dusík, chemických procesov dusíka a výr...
#kokocinka(19104,19116) #  061002 - N - Odpady obsahujúce nebezpečné látky
#kokocinka(19200,19212) #  061099 - Odpady inak nešpecifikované
#kokocinka(19296,19308) #  0611 - Odpady z výroby anorganických pigmentov a kalív
#kokocinka(19392,19404) #  061101 - O - Odpady z reakcií výroby oxidu titaničitého na báze vápnika
#kokocinka(19488,19500) #  061199 - Odpady inak nešpecifikované
#kokocinka(19584,19596) #  0613 - Odpady z anorganických chemických procesov inak nešpecifikované
#kokocinka(19680,19692) #  061301 - N - Anorganické prostriedky na ochranu rastlín, prostriedky na ochranu dreva a in...
#kokocinka(19776,19788) #  061302 - N - Použité aktívne uhlie (okrem 060702)
#kokocinka(19872,19884) #  061303 - O - Priemyselné sadze
#kokocinka(19968,19980) #  061304 - N - Odpady zo spracovania azbestu
#kokocinka(20064,20076) #  061305 - N - Sadze z pecí a komínov
#kokocinka(20160,20172) #  061399 - Odpady inak nešpecifikované
#kokocinka(20256,20268) #  07 - Odpady z organických chemických procesov
#kokocinka(20352,20364) #  0701 - Odpady z výroby, spracovania, distribúcie a používania (vsdp) základných orga...
#kokocinka(20448,20460) #  070101 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(20544,20556) #  070103 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(20640,20652) #  070104 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(20736,20748) #  070107 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(20832,20844) #  070108 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(20928,20940) #  070109 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(21024,21036) #  070110 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(21120,21132) #  070111 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(21216,21228) #  070112 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(21312,21324) #  070199 - Odpady inak nešpecifikované
#kokocinka(21408,21420) #  0702 - Odpady z vsdp plastov, syntetického kaučuku a syntetických vlákien
#kokocinka(21504,21516) #  070201 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(21600,21612) #  070203 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(21696,21708) #  070204 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(21792,21804) #  070207 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(21888,21900) #  070208 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(21984,21996) #  070209 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(22080,22092) #  070210 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(22176,22188) #  070211 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(22272,22284) #  070212 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(22368,22380) #  070213 - O - Odpadový plast
#kokocinka(22464,22476) #  070214 - N - Odpadové prísady (aditíva) obsahujúce nebezpečné látky
#kokocinka(22560,22572) #  070215 - O - Odpadové prísady iné ako uvedené v 070214
#kokocinka(22656,22668) #  070216 - N - Odpady obsahujúce silikóny
#kokocinka(22752,22764) #  070217 - O - Odpady obsahujúce silikóny iné ako uvedené v 070216
#kokocinka(22848,22860) #  070299 - Odpady inak nešpecifikované
#kokocinka(22944,22956) #  0703 - Odpady z vsdp organických farbív a pigmentov (okrem 0611)
#kokocinka(23040,23052) #  070301 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(23136,23148) #  070303 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(23232,23244) #  070304 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(23328,23340) #  070307 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(23424,23436) #  070308 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(23520,23532) #  070309 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(23616,23628) #  070310 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(23712,23724) #  070311 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(23808,23820) #  070312 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(23904,23916) #  070399 - Odpady inak nešpecifikované
#kokocinka(24000,24012) #  0704 - Odpady z vsdp organických výrobkov na ochranu rastlín (okrem 020108 a 020109)...
#kokocinka(24096,24108) #  070401 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(24192,24204) #  070403 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(24288,24300) #  070404 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(24384,24396) #  070407 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(24480,24492) #  070408 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(24576,24588) #  070409 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(24672,24684) #  070410 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(24768,24780) #  070411 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(24864,24876) #  070412 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(24960,24972) #  070413 - N - Tuhé odpady obsahujúce nebezpečné látky
#kokocinka(25056,25068) #  070499 - Odpady inak nešpecifikované
#kokocinka(25152,25164) #  0705 - Odpady z vsdp farmaceutických výrobkov
#kokocinka(25248,25260) #  070501 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(25344,25356) #  070503 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(25440,25452) #  070504 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(25536,25548) #  070507 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(25632,25644) #  070508 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(25728,25740) #  070509 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(25824,25836) #  070510 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(25920,25932) #  070511 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(26016,26028) #  070512 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(26112,26124) #  070513 - N - Tuhé odpady obsahujúce nebezpečné látky
#kokocinka(26208,26220) #  070514 - O - Tuhé odpady iné ako uvedené v 070513
#kokocinka(26304,26316) #  070599 - Odpady inak nešpecifikované
#kokocinka(26400,26412) #  0706 - Odpady z vsdp tukov, mazív, mydiel, detergentov, dezinfekčných a kozmetických...
#kokocinka(26496,26508) #  070601 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(26592,26604) #  070603 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(26688,26700) #  070604 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(26784,26796) #  070607 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(26880,26892) #  070608 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(26976,26988) #  070609 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(27072,27084) #  070610 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(27168,27180) #  070611 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(27264,27276) #  070612 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(27360,27372) #  070699 - Odpady inak nešpecifikované
#kokocinka(27456,27468) #  0707 - Odpady z vsdp čistých chemikálií a chemických výrobkov inak nešpecifikovaných
#kokocinka(27552,27564) #  070701 - N - Vodné premývacie kvapaliny a matečné lúhy
#kokocinka(27648,27660) #  070703 - N - Organické halogénované rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(27744,27756) #  070704 - N - Iné organické rozpúšťadlá, premývacie kvapaliny a matečné lúhy
#kokocinka(27840,27852) #  070707 - N - Halogénované destilačné zvyšky a reakčné splodiny
#kokocinka(27936,27948) #  070708 - N - Iné destilačné zvyšky a reakčné splodiny
#kokocinka(28032,28044) #  070709 - N - Halogénované filtračné koláče a použité absorbenty
#kokocinka(28128,28140) #  070710 - N - Iné filtračné koláče a použité absorbenty
#kokocinka(28224,28236) #  070711 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(28320,28332) #  070712 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(28416,28428) #  070799 - Odpady inak nešpecifikované
#kokocinka(28512,28524) #  08 - Odpady z výroby, spracovania, distribúcie a používania (vsdp) náterových hmôt...
#kokocinka(28608,28620) #  0801 - Odpady z vsdp a odstraňovania farieb a lakov
#kokocinka(28704,28716) #  080111 - N - Odpadové farby a laky obsahujúce organické rozpúšťadlá alebo iné nebezpečné l...
#kokocinka(28800,28812) #  080112 - O - Odpadové farby a laky iné ako uvedené v 080111
#kokocinka(28896,28908) #  080113 - N - Kaly z farby alebo laku obsahujúce organické rozpúšťadlá alebo iné nebezpečné...
#kokocinka(28992,29004) #  080114 - O - Kaly z farby alebo laku iné ako uvedené v 080113
#kokocinka(29088,29100) #  080115 - N - Vodné kaly obsahujúce farby alebo laky, ktoré obsahujú organické rozpúšťadlá ...
#kokocinka(29184,29196) #  080116 - O - Vodné kaly obsahujúce farby alebo laky, iné ako uvedené v 080115
#kokocinka(29280,29292) #  080117 - N - Odpady z odstraňovania farby alebo laku obsahujúce organické rozpúšťadlá aleb...
#kokocinka(29376,29388) #  080118 - O - Odpady z odstraňovania farby alebo laku iné ako uvedené v 080117
#kokocinka(29472,29484) #  080119 - N - Vodné suspenzie obsahujúce farby alebo laky, ktoré obsahujú organické rozpúšť...
#kokocinka(29568,29580) #  080120 - O - Vodné suspenzie obsahujúce farby alebo laky, iné ako uvedené v 080119
#kokocinka(29664,29676) #  080121 - N - Odpadový odstraňovač farby alebo laku
#kokocinka(29760,29772) #  080199 - Odpady inak nešpecifikované
#kokocinka(29856,29868) #  0802 - Odpady z vsdp iných náterových hmôt (vrátane keramických materiálov)
#kokocinka(29952,29964) #  080201 - O - Odpadové náterové prášky
#kokocinka(30048,30060) #  080202 - O - Vodné kaly obsahujúce keramické materiály
#kokocinka(30144,30156) #  080203 - O - Vodné suspenzie obsahujúce keramické materiály
#kokocinka(30240,30252) #  080299 - Odpady inak nešpecifikované
#kokocinka(30336,30348) #  0803 - Odpady z vsdp tlačiarenských farieb
#kokocinka(30432,30444) #  080307 - O - Vodné kaly obsahujúce tlačiarenskú farbu
#kokocinka(30528,30540) #  080308 - O - Vodný kvapalný odpad obsahujúci tlačiarenskú farbu
#kokocinka(30624,30636) #  080312 - N - Odpadová tlačiarenská farba obsahujúca nebezpečné látky
#kokocinka(30720,30732) #  080313 - O - Odpadová tlačiarenská farba iná ako uvedená v 080312
#kokocinka(30816,30828) #  080314 - N - Kaly z tlačiarenskej farby obsahujúce nebezpečné látky
#kokocinka(30912,30924) #  080315 - O - Kaly z tlačiarenskej farby iné ako uvedené v 080314
#kokocinka(31008,31020) #  080316 - N - Odpadové leptavé roztoky
#kokocinka(31104,31116) #  080317 - N - Odpadový toner do tlačiarne obsahujúci nebezpečné látky
#kokocinka(31200,31212) #  080318 - O - Odpadový toner do tlačiarne iný ako uvedený v 080317
#kokocinka(31296,31308) #  080319 - N - Disperzný olej
#kokocinka(31392,31404) #  080399 - Odpady inak nešpecifikované
#kokocinka(31488,31500) #  0804 - Odpady z vsdp lepidiel a tesniacich materiálov (vrátane vodotesniacich výrobkov)
#kokocinka(31584,31596) #  080409 - N - Odpadové lepidlá a tesniace materiály obsahujúce organické rozpúšťadlá alebo ...
#kokocinka(31680,31692) #  080410 - O - Odpadové lepidlá a tesniace materiály iné ako uvedené v 080409
#kokocinka(31776,31788) #  080411 - N - Kaly z lepidiel a tesniacich materiálov obsahujúce organické rozpúšťadlá aleb...
#kokocinka(31872,31884) #  080412 - O - Kaly z lepidiel a tesniacich materiálov iné ako uvedené v 080411
#kokocinka(31968,31980) #  080413 - N - Vodné kaly obsahujúce lepidlá alebo tesniace materiály, ktoré obsahujú organi...
#kokocinka(32064,32076) #  080414 - O - Vodné kaly obsahujúce lepidlá alebo tesniace materiály, iné ako uvedené v 080413
#kokocinka(32160,32172) #  080415 - N - Vodný kvapalný odpad obsahujúci lepidlá alebo tesniace materiály, ktoré obsah...
#kokocinka(32256,32268) #  080416 - O - Vodný kvapalný odpad obsahujúci lepidlá alebo tesniace materiály, iný ako uve...
#kokocinka(32352,32364) #  080417 - N - Živičný olej
#kokocinka(32448,32460) #  080499 - Odpady inak nešpecifikované
#kokocinka(32544,32556) #  0805 - Odpady inak nešpecifikované v 08
#kokocinka(32640,32652) #  080501 - N - Odpadové izokyanáty
#kokocinka(32736,32748) #  09 - Odpady z fotografického priemyslu
#kokocinka(32832,32844) #  0901 - Odpady z fotografického priemyslu
#kokocinka(32928,32940) #  090101 - N - Roztoky vodorozpustných vývojok a aktivátorov
#kokocinka(33024,33036) #  090102 - N - Roztoky vodorozpustných vývojok ofsetových dosiek
#kokocinka(33120,33132) #  090103 - N - Roztoky vývojok rozpustných v rozpúšťadlách
#kokocinka(33216,33228) #  090104 - N - Roztoky ustaľovačov
#kokocinka(33312,33324) #  090105 - N - Bieliace roztoky a roztoky bieliacich ustalovačov
#kokocinka(33408,33420) #  090106 - N - Odpady zo spracovania fotografických odpadov v mieste ich vzniku obsahujúce s...
#kokocinka(33504,33516) #  090107 - O - Fotografický film a papiere obsahujúce striebro alebo zlúčeniny striebra
#kokocinka(33600,33612) #  090108 - O - Fotografický film a papiere neobsahujúce striebro alebo zlúčeniny striebra
#kokocinka(33696,33708) #  090110 - O - Jednorazové kamery bez batérií
#kokocinka(33792,33804) #  090111 - N - Jednorazové kamery s batériami zaradené do160601, 160602 alebo 160603
#kokocinka(33888,33900) #  090112 - O - Jednorazové kamery s batériami iné ako uvedené v 090111
#kokocinka(33984,33996) #  090113 - N - Vodný kvapalný odpad z regenerácie striebra v mieste regenerácie iný ako uved...
#kokocinka(34080,34092) #  090199 - Odpady inak nešpecifikované
#kokocinka(34176,34188) #  10 - Odpady z tepelných procesov
#kokocinka(34272,34284) #  1001 - Odpady z elektrární a iných spayovacích zariadení (okrem19)
#kokocinka(34368,34380) #  100101 - O - Popol, škvára a prach z kotlov (okrem prachu z kotlov uvedeného v 100104)
#kokocinka(34464,34476) #  100102 - O - Popolček z uhlia
#kokocinka(34560,34572) #  100103 - O - Popolček z rašeliny a (neupraveného) dreva
#kokocinka(34656,34668) #  100104 - N - Popolček a prach z kotlov zo spaľovania oleja
#kokocinka(34752,34764) #  100105 - O - Tuhé reakčné splodiny z odsírovania dymových plynov na báze vápnika
#kokocinka(34848,34860) #  100106 - O - Popol z neošetreného dreva
#kokocinka(34944,34956) #  100107 - O - Reakčné splodiny z odsírovania dymových plynov na báze vápnika vo forme kalu
#kokocinka(35040,35052) #  100109 - N - Kyselina sírová
#kokocinka(35136,35148) #  100113 - N - Popolček z emulgovaných uhľovodíkov použitých ako palivo
#kokocinka(35232,35244) #  100114 - N - Popol, škvára a prach z kotlov zo spaľovania odpadov obsahujúce nebezpečné látky
#kokocinka(35328,35340) #  100115 - O - Popol, škvára a prach z kotlov zo spaľovania odpadov iné ako uvedené v 100114
#kokocinka(35424,35436) #  100116 - N - Popolček zo spaľovania odpadov obsahujúci nebezpečné látky
#kokocinka(35520,35532) #  100117 - O - Popolček zo spaľovania odpadov iný ako uvedený v 100116
#kokocinka(35616,35628) #  100118 - N - Odpady z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(35712,35724) #  100119 - O - Odpady z čistenia plynu iné ako uvedené v 100105, 100107 a 100118
#kokocinka(35808,35820) #  100120 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(35904,35916) #  100121 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(36000,36012) #  100122 - N - Vodné kaly z čistenia kotlov obsahujúce nebezpečné látky
#kokocinka(36096,36108) #  100123 - O - Vodné kaly z čistenia kotlov iné ako uvedené v 100122
#kokocinka(36192,36204) #  100124 - O - Piesky z fluidnej vrstvy
#kokocinka(36288,36300) #  100125 - O - Odpady zo skladovania a úpravy pre uhoľné elektrárne
#kokocinka(36384,36396) #  100126 - O - Odpady z úpravy chladiacej vody
#kokocinka(36480,36492) #  100199 - Odpady inak nešpecifikované
#kokocinka(36576,36588) #  1002 - Odpady zo železiarskeho a oceliarskeho priemyslu
#kokocinka(36672,36684) #  100201 - O - Odpad zo spracovania trosky
#kokocinka(36768,36780) #  100202 - O - Nespracovaná troska
#kokocinka(36864,36876) #  100207 - N - Tuhé odpady z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(36960,36972) #  100208 - O - Tuhé odpady z čistenia plynu iné ako uvedené v 100207
#kokocinka(37056,37068) #  100210 - O - Okuje z valcovania
#kokocinka(37152,37164) #  100211 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(37248,37260) #  100212 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100211
#kokocinka(37344,37356) #  100213 - N - Kaly a filtračné koláče z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(37440,37452) #  100214 - O - Kaly a filtračné koláče z čistenia plynov iné ako uvedené v 100213
#kokocinka(37536,37548) #  100215 - O - Iné kaly a filtračné koláče
#kokocinka(37632,37644) #  100299 - Odpady inak nešpecifikované
#kokocinka(37728,37740) #  1003 - Odpady z termickej metalurgie hliníka
#kokocinka(37824,37836) #  100302 - O - Anódový šrot
#kokocinka(37920,37932) #  100304 - N - Trosky z prvého tavenia
#kokocinka(38016,38028) #  100305 - O - Odpadový oxid hlinitý
#kokocinka(38112,38124) #  100308 - N - Soľné trosky z druhého tavenia
#kokocinka(38208,38220) #  100309 - N - Čierne stery z druhého tavenia
#kokocinka(38304,38316) #  100315 - N - Peny, ktoré sú horľavé alebo ktoré pri styku s vodou uvoľňujú horľavé plyny v...
#kokocinka(38400,38412) #  100316 - O - Peny iné ako uvedené v 100315
#kokocinka(38496,38508) #  100317 - N - Odpady obsahujúce decht z výroby anód
#kokocinka(38592,38604) #  100318 - O - Odpady obsahujúce uhlík z výroby anód iné ako uvedené v 100317
#kokocinka(38688,38700) #  100319 - N - Prach z dymových plynov obsahujúci nebezpečné látky
#kokocinka(38784,38796) #  100320 - O - Prach z dymových plynov iný ako uvedený v 100319
#kokocinka(38880,38892) #  100321 - N - Iné tuhé znečisťujúce látky a prach (vrátane prachu z guľových mlynov) obsahu...
#kokocinka(38976,38988) #  100322 - O - Iné tuhé znečisťujúce látky a prach (vrátane prachu z guľových mlynov) iné ak...
#kokocinka(39072,39084) #  100323 - N - Tuhé odpady z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(39168,39180) #  100324 - O - Tuhé odpady z čistenia plynu iné ako uvedené v 100323
#kokocinka(39264,39276) #  100325 - N - Kaly a filtračné koláče z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(39360,39372) #  100326 - O - Kaly a filtračné koláče z čistenia plynu iné ako uvedené v 100325
#kokocinka(39456,39468) #  100327 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(39552,39564) #  100328 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100327
#kokocinka(39648,39660) #  100329 - N - Odpady z úpravy soľných trosiek a čiernych sterov obsahujúce nebezpečné látky
#kokocinka(39744,39756) #  100330 - O - Odpady z úpravy soľných trosiek a čiernych sterov iné ako uvedené v 100329
#kokocinka(39840,39852) #  100399 - Odpady inak nešpecifikované
#kokocinka(39936,39948) #  1004 - Odpady z termickej metalurgie olova
#kokocinka(40032,40044) #  100401 - N - Trosky z prvého a druhého tavenia
#kokocinka(40128,40140) #  100402 - N - Stery a peny z prvého a druhého tavenia
#kokocinka(40224,40236) #  100403 - N - Arzeničnan vápenatý
#kokocinka(40320,40332) #  100404 - N - Prach z dymových plynov
#kokocinka(40416,40428) #  100405 - N - Iné tuhé znečisťujúce látky a prach
#kokocinka(40512,40524) #  100406 - N - Tuhé odpady z čistenia plynov
#kokocinka(40608,40620) #  100407 - N - Kaly a filtračné koláče z čistenia plynov
#kokocinka(40704,40716) #  100409 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(40800,40812) #  100410 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100409
#kokocinka(40896,40908) #  100499 - Odpady inak nešpecifikované
#kokocinka(40992,41004) #  1005 - Odpady z termickej metalurgie zinku
#kokocinka(41088,41100) #  100501 - O - Trosky z prvého a druhého tavenia
#kokocinka(41184,41196) #  100503 - N - Prach z dymových plynov
#kokocinka(41280,41292) #  100504 - O - Iné tuhé znečisťujúce látky a prach
#kokocinka(41376,41388) #  100505 - N - Tuhý odpad z čistenia plynov
#kokocinka(41472,41484) #  100506 - N - Kaly a filtračné koláče z čistenia plynov
#kokocinka(41568,41580) #  100508 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(41664,41676) #  100509 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100508
#kokocinka(41760,41772) #  100510 - N - Stery a peny, ktoré sú horľavé alebo ktoré pri styku s vodou uvoľňujú horľavé...
#kokocinka(41856,41868) #  100511 - O - Stery a peny iné ako uvedené v 100510
#kokocinka(41952,41964) #  100599 - Odpady inak nešpecifikované
#kokocinka(42048,42060) #  1006 - Odpady z termickej metalurgie medi
#kokocinka(42144,42156) #  100601 - O - Trosky z prvého a druhého tavenia
#kokocinka(42240,42252) #  100602 - O - Stery a peny z prvého a druhého tavenia
#kokocinka(42336,42348) #  100603 - N - Prach z dymových plynov
#kokocinka(42432,42444) #  100604 - O - Iné tuhé znečisťujúce látky a prach
#kokocinka(42528,42540) #  100606 - N - Tuhé odpady z čistenia plynov
#kokocinka(42624,42636) #  100607 - N - Kaly a filtračné koláče zo spracovania plynu
#kokocinka(42720,42732) #  100609 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(42816,42828) #  100610 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100609
#kokocinka(42912,42924) #  100699 - Odpady inak nešpecifikované
#kokocinka(43008,43020) #  1007 - Odpady z termickej metalurgie striebra, zlata a platiny
#kokocinka(43104,43116) #  100701 - O - Trosky z prvého a druhého tavenia
#kokocinka(43200,43212) #  100702 - O - Stery a peny z prvého a druhého tavenia
#kokocinka(43296,43308) #  100703 - O - Tuhé odpady z čistenia plynov
#kokocinka(43392,43404) #  100704 - O - Iné tuhé znečisťujúce látky a prach
#kokocinka(43488,43500) #  100705 - O - Kaly a filtračné koláče z čistenia plynov
#kokocinka(43584,43596) #  100707 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(43680,43692) #  100708 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100707
#kokocinka(43776,43788) #  100799 - Odpady inak nešpecifikované
#kokocinka(43872,43884) #  1008 - Odpady z termickej metalurgie iných neželezných kovov
#kokocinka(43968,43980) #  100804 - O - Tuhé znečisťujúce látky a prach
#kokocinka(44064,44076) #  100808 - N - Soľná troska z prvého a druhého tavenia
#kokocinka(44160,44172) #  100809 - O - Iné trosky
#kokocinka(44256,44268) #  100810 - N - Stery a peny, ktoré sú horľavé alebo ktoré pri styku s vodou uvoľňujú horľavé...
#kokocinka(44352,44364) #  100811 - O - Stery a peny iné ako uvedené v 100810
#kokocinka(44448,44460) #  100812 - N - Odpady obsahujúce decht z výroby anód
#kokocinka(44544,44556) #  100813 - O - Odpady obsahujúce uhlík z výroby anód, iné ako uvedené v 100812
#kokocinka(44640,44652) #  100814 - O - Anódový šrot
#kokocinka(44736,44748) #  100815 - N - Prach z dymových plynov obsahujúci nebezpečné látky
#kokocinka(44832,44844) #  100816 - O - Prach z dymových plynov iný ako uvedený v 100815
#kokocinka(44928,44940) #  100817 - N - Kaly a filtračné koláče z čistenia dymových plynov obsahujúce nebezpečné látky
#kokocinka(45024,45036) #  100818 - O - Kaly a filtračné koláče z čistenia dymových plynov iné ako uvedené v 100817
#kokocinka(45120,45132) #  100819 - N - Odpady z úpravy chladiacej vody obsahujúce olej
#kokocinka(45216,45228) #  100820 - O - Odpady z úpravy chladiacej vody iné ako uvedené v 100819
#kokocinka(45312,45324) #  100899 - Odpady inak nešpecifikované
#kokocinka(45408,45420) #  1009 - Odpady zo zlievania železných kovov
#kokocinka(45504,45516) #  100903 - O - Pecná troska
#kokocinka(45600,45612) #  100905 - N - Odlievacie jadrá a formy nepoužité na odlievanie, obsahujúce nebezpečné látky
#kokocinka(45696,45708) #  100906 - O - Odlievacie jadrá a formy nepoužité na odlievanie, iné ako uvedené v 100905
#kokocinka(45792,45804) #  100907 - N - Odlievacie jadrá a formy použité na odlievanie, obsahujúce nebezpečné látky
#kokocinka(45888,45900) #  100908 - O - Odlievacie jadrá a formy použité na odlievanie, iné ako uvedené v 100907
#kokocinka(45984,45996) #  100909 - N - Prach z dymových plynov obsahujúci nebezpečné látky
#kokocinka(46080,46092) #  100910 - O - Prach z dymových plynov iný ako uvedený v 100909
#kokocinka(46176,46188) #  100911 - N - Iné tuhé znečisťujúce látky obsahujúce nebezpečné látky
#kokocinka(46272,46284) #  100912 - O - Iné tuhé znečisťujúce látky iné ako uvedené v 100911
#kokocinka(46368,46380) #  100913 - N - Odpadové spojivá obsahujúce nebezpečné látky
#kokocinka(46464,46476) #  100914 - O - Odpadové spojivá iné ako uvedené v 100913
#kokocinka(46560,46572) #  100915 - N - Odpad z prostriedkov na indikáciu trhlín obsahujúci nebezpečné látky
#kokocinka(46656,46668) #  100916 - O - Odpad z prostriedkov na indikáciu trhlín iný ako uvedený v 100915
#kokocinka(46752,46764) #  100999 - Odpady inak nešpecifikované
#kokocinka(46848,46860) #  1010 - Odpady zo zlievania neželezných kovov
#kokocinka(46944,46956) #  101003 - O - Pecná troska
#kokocinka(47040,47052) #  101005 - N - Odlievacie jadrá a formy nepoužité na odlievanie, obsahujúce nebezpečné látky
#kokocinka(47136,47148) #  101006 - O - Odlievacie jadrá a formy nepoužité na odlievanie, iné ako uvedené v 101005
#kokocinka(47232,47244) #  101007 - N - Odlievacie jadrá a formy použité na odlievanie, obsahujúce nebezpečné látky
#kokocinka(47328,47340) #  101008 - O - Odlievacie jadrá a formy použité na odlievanie, iné ako uvedené v 101007
#kokocinka(47424,47436) #  101009 - N - Prach z dymových plynov obsahujúci nebezpečné látky
#kokocinka(47520,47532) #  101010 - O - Prach z dymových plynov iný ako uvedený v 101009
#kokocinka(47616,47628) #  101011 - N - Iné tuhé znečisťujúce látky obsahujúce nebezpečné látky
#kokocinka(47712,47724) #  101012 - O - Iné tuhé znečisťujúce látky iné ako uvedené v 101011
#kokocinka(47808,47820) #  101013 - N - Odpadové spojivá obsahujúce nebezpečné látky
#kokocinka(47904,47916) #  101014 - O - Odpadové spojivá iné ako uvedené v 101013
#kokocinka(48000,48012) #  101015 - N - Odpad z prostriedkov na indikáciu trhlín obsahujúci nebezpečné látky
#kokocinka(48096,48108) #  101016 - O - Odpad z prostriedkov na indikáciu trhlín iný ako uvedený v 101015
#kokocinka(48192,48204) #  101099 - Odpady inak nešpecifikované
#kokocinka(48288,48300) #  1011 - Odpady z výroby skla a sklených výrobkov
#kokocinka(48384,48396) #  101103 - O - Odpadové vláknité materiály na báze skla
#kokocinka(48480,48492) #  101105 - O - Tuhé znečisťujúce látky a prach
#kokocinka(48576,48588) #  101109 - N - Odpad zo surovinovej zmesi pred tepelným spracovaním obsahujúci nebezpečné látky
#kokocinka(48672,48684) #  101110 - O - Odpad zo surovinovej zmesi pred tepelným spracovaním iný ako uvedený v 101109
#kokocinka(48768,48780) #  101111 - N - Sklený odpad v malých časticiach a sklený prach obsahujúce ťažké kovy (napr. ...
#kokocinka(48864,48876) #  101112 - O - Odpadové sklo iné ako uvedené v 101111
#kokocinka(48960,48972) #  101113 - N - Kal z leštenia a brúsenia skla obsahujúci nebezpečné látky
#kokocinka(49056,49068) #  101114 - O - Kal z leštenia a brúsenia skla iný ako uvedený v 101113
#kokocinka(49152,49164) #  101115 - N - Tuhé odpady z čistenia dymových plynov obsahujúce nebezpečné látky
#kokocinka(49248,49260) #  101116 - O - Tuhé odpady z čistenia dymových plynov iné ako uvedené v 101115
#kokocinka(49344,49356) #  101117 - N - Kaly a filtračné koláče z čistenia dymových plynov obsahujúce nebezpečné látky
#kokocinka(49440,49452) #  101118 - O - Kaly a filtračné koláče z čistenia dymových plynov iné ako uvedené v 101117
#kokocinka(49536,49548) #  101119 - N - Tuhé odpady zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce ...
#kokocinka(49632,49644) #  101120 - O - Tuhé odpady zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uve...
#kokocinka(49728,49740) #  101199 - Odpady inak nešpecifikované
#kokocinka(49824,49836) #  1012 - Odpady z výroby keramiky, tehál, obkladačiek a dlaždíc a stavebných výrobkov
#kokocinka(49920,49932) #  101201 - O - Odpad zo surovinovej zmesi pred tepelným spracovaním
#kokocinka(50016,50028) #  101203 - O - Tuhé znečisťujúce látky a prach
#kokocinka(50112,50124) #  101205 - O - Kaly a filtračné koláče z čistenia plynov
#kokocinka(50208,50220) #  101206 - O - Vyradené formy
#kokocinka(50304,50316) #  101208 - O - Odpadová keramika, odpadové tehly, odpadové obkladačky a dlaždice a odpadová ...
#kokocinka(50400,50412) #  101209 - N - Tuhé odpady z čistenia plynov obsahujúce nebezpečné látky
#kokocinka(50496,50508) #  101210 - O - Tuhé odpady z čistenia plynov iné ako uvedené v 101209
#kokocinka(50592,50604) #  101211 - N - Odpady z glazúry obsahujúce ťažké kovy
#kokocinka(50688,50700) #  101212 - O - Odpady z glazúry iné ako uvedené v 101211
#kokocinka(50784,50796) #  101213 - O - Kal zo spracovania kvapalného odpadu v mieste jeho vzniku
#kokocinka(50880,50892) #  101299 - Odpady inak nešpecifikované
#kokocinka(50976,50988) #  1013 - Odpady z výroby cementu, páleného vápna a sadry a výrobkov z nich
#kokocinka(51072,51084) #  101301 - O - Odpad zo surovinovej zmesi pred tepelným spracovaním
#kokocinka(51168,51180) #  101304 - O - Odpady z pálenia a hasenia vápna
#kokocinka(51264,51276) #  101306 - O - Tuhé znečisťujúce látky a prach iné ako uvedené v 101312 a 101313
#kokocinka(51360,51372) #  101307 - O - Kaly a filtračné koláče z čistenia plynov
#kokocinka(51456,51468) #  101309 - N - Odpady z výroby azbestocementu obsahujúce azbesty
#kokocinka(51552,51564) #  101310 - O - Odpady z výroby azbestocementu iné ako uvedené v 101309
#kokocinka(51648,51660) #  101311 - O - Odpady z kompozitných materiálov na báze cementu iné ako uvedené v 101309 a 1...
#kokocinka(51744,51756) #  101312 - N - Tuhé odpady z čistenia plynu obsahujúce nebezpečné látky
#kokocinka(51840,51852) #  101313 - O - Tuhé odpady z čistenia plynu iné ako uvedené v 101312
#kokocinka(51936,51948) #  101314 - O - Odpadový betón a betónový kal
#kokocinka(52032,52044) #  101399 - Odpady inak nešpecifikované
#kokocinka(52128,52140) #  1014 - Odpady z krematórií
#kokocinka(52224,52236) #  101401 - N - Odpady z čistenia plynu obsahujúce ortuť
#kokocinka(52320,52332) #  11 - Odpady z chemickej povrchovej úpravy kovov a nanášania kovov a iných materiál...
#kokocinka(52416,52428) #  1101 - Odpady z chemickej povrchovej úpravy kovov a nanášania kovov a iných materiál...
#kokocinka(52512,52524) #  110105 - N - Kyslé moriace roztoky
#kokocinka(52608,52620) #  110106 - N - Kyseliny inak nešpecifikované
#kokocinka(52704,52716) #  110107 - N - Alkalické moriace roztoky
#kokocinka(52800,52812) #  110108 - N - Kaly z fosfátovania
#kokocinka(52896,52908) #  110109 - N - Kaly a filtračné koláče obsahujúce nebezpečné látky
#kokocinka(52992,53004) #  110110 - O - Kaly a filtračné koláče iné ako uvedené v 110109
#kokocinka(53088,53100) #  110111 - N - Vodné oplachovacie kvapaliny obsahujúce nebezpečné látky
#kokocinka(53184,53196) #  110112 - O - Vodné oplachovacie kvapaliny iné ako uvedené v 110111
#kokocinka(53280,53292) #  110113 - N - Odpady z odmasťovania obsahujúce nebezpečné látky
#kokocinka(53376,53388) #  110114 - O - Odpady z odmasťovania iné ako uvedené v 110113
#kokocinka(53472,53484) #  110115 - N - Eluáty a kaly z membránových alebo iontomeničových systémov obsahujúce nebezp...
#kokocinka(53568,53580) #  110116 - N - Nasýtené alebo použité iontomeničové živice
#kokocinka(53664,53676) #  110198 - N - Iné odpady obsahujúce nebezpečné látky
#kokocinka(53760,53772) #  110199 - Odpady inak nešpecifikované
#kokocinka(53856,53868) #  1102 - Odpady z procesov hydrometalurgie neželezných kovov
#kokocinka(53952,53964) #  110202 - N - Kaly z hydrometalurgie zinku (vrátane jarositu, goethitu)
#kokocinka(54048,54060) #  110203 - O - Odpady z výroby anód pre vodné elektrolytické procesy
#kokocinka(54144,54156) #  110205 - N - Odpady z procesov hydrometalurgie medi obsahujúce nebezpečné látky
#kokocinka(54240,54252) #  110206 - O - Odpady z procesov hydrometalurgie medi iné ako uvedené v 110205
#kokocinka(54336,54348) #  110207 - N - Iné odpady obsahujúce nebezpečné látky
#kokocinka(54432,54444) #  110299 - Odpady inak nešpecifikované
#kokocinka(54528,54540) #  1103 - Kaly a tuhé látky z popúšťacích procesov
#kokocinka(54624,54636) #  110301 - N - Odpady obsahujúce kyanidy
#kokocinka(54720,54732) #  110302 - N - Iné odpady
#kokocinka(54816,54828) #  1105 - Odpady z galvanických procesov
#kokocinka(54912,54924) #  110501 - O - Tvrdý zinok
#kokocinka(55008,55020) #  110502 - O - Zinkový popol
#kokocinka(55104,55116) #  110503 - N - Tuhé odpady z čistenia plynu
#kokocinka(55200,55212) #  110504 - N - Použité tavivo
#kokocinka(55296,55308) #  110599 - Odpady inak nešpecifikované
#kokocinka(55392,55404) #  12 - Odpady z tvarovania, fyzikálnej a mechanickej úpravy povrchov kovov a plastov
#kokocinka(55488,55500) #  1201 - Odpady z tvarovania a fyzikálnej a mechanickej úpravy povrchov kovov a plastov
#kokocinka(55584,55596) #  120101 - O - Piliny a triesky zo železných kovov
#kokocinka(55680,55692) #  120102 - O - Prach a zlomky zo železných kovov
#kokocinka(55776,55788) #  120103 - O - Piliny a triesky z neželezných kovov
#kokocinka(55872,55884) #  120104 - O - Prach a zlomky z neželezných kovov
#kokocinka(55968,55980) #  120105 - O - Hobliny a triesky z plastov
#kokocinka(56064,56076) #  120106 - N - Minerálne rezné oleje obsahujúce halogény okrem emulzií a roztokov
#kokocinka(56160,56172) #  120107 - N - Minerálne rezné oleje neobsahujúce halogény okrem emulzií a roztokov
#kokocinka(56256,56268) #  120108 - N - Rezné emulzie a roztoky obsahujúce halogény
#kokocinka(56352,56364) #  120109 - N - Rezné emulzie a roztoky neobsahujúce halogény
#kokocinka(56448,56460) #  120110 - N - Syntetické rezné oleje
#kokocinka(56544,56556) #  120112 - N - Použité vosky a tuky
#kokocinka(56640,56652) #  120113 - O - Odpady zo zvárania
#kokocinka(56736,56748) #  120114 - N - Kaly z obrábania obsahujúce nebezpečné látky
#kokocinka(56832,56844) #  120115 - O - Kaly z obrábania iné ako uvedené v 120114
#kokocinka(56928,56940) #  120116 - N - Odpadový pieskovací materiál obsahujúci nebezpečné látky
#kokocinka(57024,57036) #  120117 - O - Odpadový pieskovací materiál iný ako uvedený v 120116
#kokocinka(57120,57132) #  120118 - N - Kovový kal z brúsenia, honovania a lapovania obsahujúci olej
#kokocinka(57216,57228) #  120119 - N - Biologicky ľahko rozložitelný strojový olej
#kokocinka(57312,57324) #  120120 - N - Použité brúsne nástroje a brúsne materiály obsahujúce nebezpečné látky
#kokocinka(57408,57420) #  120121 - O - Použité brúsne nástroje a brúsne materiály iné ako uvedené v 120120
#kokocinka(57504,57516) #  120199 - Odpady inak nešpecifikované
#kokocinka(57600,57612) #  1203 - Odpady z procesov odmasťovania vodou a parou (okrem11)
#kokocinka(57696,57708) #  120301 - N - Vodné pracie kvapaliny
#kokocinka(57792,57804) #  120302 - N - Odpady z odmasťovania parou
#kokocinka(57888,57900) #  13 - Odpady z olejov a kvapalných palív (okrem jedlých olejov, 05 , 12)
#kokocinka(57984,57996) #  1301 - Odpadové hydraulické oleje
#kokocinka(58080,58092) #  130101 - N - Hydraulické oleje obsahujúce pcb
#kokocinka(58176,58188) #  130104 - N - Chlórované emulzie
#kokocinka(58272,58284) #  130105 - N - Nechlórované emulzie
#kokocinka(58368,58380) #  130109 - N - Chlórované minerálne hydraulické oleje
#kokocinka(58464,58476) #  130110 - N - Nechlórované minerálne hydraulické oleje
#kokocinka(58560,58572) #  130111 - N - Syntetické hydraulické oleje
#kokocinka(58656,58668) #  130112 - N - Biologicky ľahko rozložitelné hydraulické oleje
#kokocinka(58752,58764) #  130113 - N - Iné hydraulické oleje
#kokocinka(58848,58860) #  1302 - Odpadové motorové, prevodové a mazacie oleje
#kokocinka(58944,58956) #  130204 - N - Chlórované minerálne motorové, prevodové a mazacie oleje
#kokocinka(59040,59052) #  130205 - N - Nechlórované minerálne motorové, prevodové a mazacie oleje
#kokocinka(59136,59148) #  130206 - N - Syntetické motorové, prevodové a mazacie oleje
#kokocinka(59232,59244) #  130207 - N - Biologicky ľahko rozložitelné syntetické motorové, prevodové a mazacie oleje
#kokocinka(59328,59340) #  130208 - N - Iné motorové, prevodové a mazacie oleje
#kokocinka(59424,59436) #  1303 - Odpadové izolačné oleje a oleje na prenos tepla a iné kvapaliny
#kokocinka(59520,59532) #  130301 - N - Izolačné oleje alebo oleje obsahujúce pcb
#kokocinka(59616,59628) #  130306 - N - Chlórované minerálne izolačné a teplonosné oleje iné ako uvedené v 130301
#kokocinka(59712,59724) #  130307 - N - Nechlórované minerálne izolačné a teplonosné oleje
#kokocinka(59808,59820) #  130308 - N - Syntetické izolačné a teplonosné oleje
#kokocinka(59904,59916) #  130309 - N - Biologicky ľahko rozložitelné izolačné a teplonosné oleje
#kokocinka(60000,60012) #  130310 - N - Iné izolačné a teplonosné oleje
#kokocinka(60096,60108) #  1304 - Odpadové oleje z prevádzky lodí
#kokocinka(60192,60204) #  130401 - N - Odpadové oleje z prevádzky lodí vnútrozemskej plavby
#kokocinka(60288,60300) #  130402 - N - Odpadové oleje z prístavných kanálov
#kokocinka(60384,60396) #  130403 - N - Odpadové oleje z prevádzky iných lodí
#kokocinka(60480,60492) #  1305 - Odpady z odlučovačov oleja z vody
#kokocinka(60576,60588) #  130501 - N - Tuhé látky z lapačov piesku a odlučovačov oleja z vody
#kokocinka(60672,60684) #  130502 - N - Kaly z odlučovačov oleja z vody
#kokocinka(60768,60780) #  130503 - N - Kaly z lapačov nečistôt
#kokocinka(60864,60876) #  130506 - N - Olej z odlučovačov oleja z vody
#kokocinka(60960,60972) #  130507 - N - Voda obsahujúca olej z odlučovačov oleja z vody
#kokocinka(61056,61068) #  130508 - N - Zmesi odpadov z lapačov piesku a odlučovačov oleja z vody
#kokocinka(61152,61164) #  1307 - Odpady z kvapalných palív
#kokocinka(61248,61260) #  130701 - N - Vykurovací olej a motorová nafta
#kokocinka(61344,61356) #  130702 - N - Benzín
#kokocinka(61440,61452) #  130703 - N - Iné palivá (vrátane zmesí)
#kokocinka(61536,61548) #  1308 - Olejové odpady inak nešpecifikované
#kokocinka(61632,61644) #  130801 - N - Kaly alebo emulzie z odsoľovacích zariadení
#kokocinka(61728,61740) #  130802 - N - Iné emulzie
#kokocinka(61824,61836) #  130899 - Odpady inak nešpecifikované
#kokocinka(61920,61932) #  14 - Odpady z organických rozpúšťadiel, chladiacich médií a propelentov (okrem 07 ...
#kokocinka(62016,62028) #  1406 - Odpady z organických rozpúšťadiel, chladiacich médií a pien a aerosólov z pro...
#kokocinka(62112,62124) #  140601 - N - Chlórfluórované uhľovodíky, hcfc, hfc
#kokocinka(62208,62220) #  140602 - N - Iné halogénované rozpúšťadlá a zmesi rozpúšťadiel
#kokocinka(62304,62316) #  140603 - N - Iné rozpúšťadlá a zmesi rozpúšťadiel
#kokocinka(62400,62412) #  140604 - N - Kaly alebo tuhé odpady obsahujúce halogénované rozpúšťadlá
#kokocinka(62496,62508) #  140605 - N - Kaly alebo tuhé odpady obsahujúce iné rozpúšťadlá
#kokocinka(62592,62604) #  15 - Odpadové obaly, absorbenty, handry na čistenie, filtračný materiál a ochranné...
#kokocinka(62688,62700) #  1501 - Obaly (vrátane odpadových obalov zo separovaného zberu komunálnych odpadov)
#kokocinka(62784,62796) #  150101 - O - Obaly z papiera a lepenky
#kokocinka(62880,62892) #  150102 - O - Obaly z plastov
#kokocinka(62976,62988) #  150103 - O - Obaly z dreva
#kokocinka(63072,63084) #  150104 - O - Obaly z kovu
#kokocinka(63168,63180) #  150105 - O - Kompozitné obaly
#kokocinka(63264,63276) #  150106 - O - Zmiešané obaly
#kokocinka(63360,63372) #  150107 - O - Obaly zo skla
#kokocinka(63456,63468) #  150109 - O - Obaly z textilu
#kokocinka(63552,63564) #  150110 - N - Obaly obsahujúce zvyšky nebezpečných látok alebo kontaminované nebezpečnými l...
#kokocinka(63648,63660) #  150111 - N - Kovové obaly obsahujúce nebezpečný tuhý pórovitý základný materiál (napr. azb...
#kokocinka(63744,63756) #  1502 - Absorbenty, filtračné materiály, handry na čistenie a ochranné odevy
#kokocinka(63840,63852) #  150202 - N - Absorbenty, filtračné materiály vrátane olejových filtrov inak nešpecifikovan...
#kokocinka(63936,63948) #  150203 - O - Absorbenty, filtračné materiály, handry na čistenie a ochranné odevy iné ako ...
#kokocinka(64032,64044) #  16 - Odpady inak nešpecifikované v tomto katalógu
#kokocinka(64128,64140) #  1601 - Staré vozidlá z rozličných dopravných prostriedkov (vrátane strojov neurčenýc...
#kokocinka(64224,64236) #  160103 - O - Opotrebované pneumatiky
#kokocinka(64320,64332) #  160104 - N - Staré vozidlá
#kokocinka(64416,64428) #  160106 - O - Staré vozidlá neobsahujúce kvapaliny a iné nebezpečné dielce
#kokocinka(64512,64524) #  160107 - N - Olejové filtre
#kokocinka(64608,64620) #  160108 - N - Dielce obsahujúce ortuť
#kokocinka(64704,64716) #  160109 - N - Dielce obsahujúce pcb
#kokocinka(64800,64812) #  160110 - N - Výbušné časti (napr. bezpečnostné vzduchové vankúše)
#kokocinka(64896,64908) #  160111 - N - Brzdové platničky a obloženie obsahujúce azbest
#kokocinka(64992,65004) #  160112 - O - Brzdové platničky a obloženie iné ako uvedené v 160111
#kokocinka(65088,65100) #  160113 - N - Brzdové kvapaliny
#kokocinka(65184,65196) #  160114 - N - Nemrznúce kvapaliny obsahujúce nebezpečné látky
#kokocinka(65280,65292) #  160115 - O - Nemrznúce kvapaliny iné ako uvedené v 160114
#kokocinka(65376,65388) #  160116 - O - Nádrže na skvapalnený plyn
#kokocinka(65472,65484) #  160117 - O - Železné kovy
#kokocinka(65568,65580) #  160118 - O - Neželezné kovy
#kokocinka(65664,65676) #  160119 - O - Plasty
#kokocinka(65760,65772) #  160120 - O - Sklo
#kokocinka(65856,65868) #  160121 - N - Nebezpečné dielce iné ako uvedené v 160107 až 160111, 160113 a 160114
#kokocinka(65952,65964) #  160122 - O - Časti inak nešpecifikované
#kokocinka(66048,66060) #  160199 - Odpady inak nešpecifikované
#kokocinka(66144,66156) #  1602 - Odpady z elektrických a elektronických zariadení
#kokocinka(66240,66252) #  160209 - N - Transformátory a kondenzátory obsahujúce pcb
#kokocinka(66336,66348) #  160210 - N - Vyradené zariadenia obsahujúce alebo znečistené pcb, iné ako uvedené v 160209
#kokocinka(66432,66444) #  160211 - N - Vyradené zariadenia obsahujúce chlórfluórované uhľovodíky, hcfc, hfc
#kokocinka(66528,66540) #  160212 - N - Vyradené zariadenia obsahujúce voľný azbest
#kokocinka(66624,66636) #  160213 - N - Vyradené zariadenia obsahujúce nebezpečné časti, iné ako uvedené v 160209 až ...
#kokocinka(66720,66732) #  160214 - O - Vyradené zariadenia iné ako uvedené v 160209 až 160213
#kokocinka(66816,66828) #  160215 - N - Nebezpečné časti odstránené z vyradených zariadení
#kokocinka(66912,66924) #  160216 - O - Časti odstránené z vyradených zariadení, iné ako uvedené v 160215
#kokocinka(67008,67020) #  1603 - Výrobné šarže a nepoužité výrobky nevyhovujúcej kvality
#kokocinka(67104,67116) #  160303 - N - Anorganické odpady obsahujúce nebezpečné látky
#kokocinka(67200,67212) #  160304 - O - Anorganické odpady iné ako uvedené v 160303
#kokocinka(67296,67308) #  160305 - N - Organické odpady obsahujúce nebezpečné látky
#kokocinka(67392,67404) #  160306 - O - Organické odpady iné ako uvedené v 160305
#kokocinka(67488,67500) #  160307 - N - Kovová ortuť
#kokocinka(67584,67596) #  1604 - Odpady z výbušnín
#kokocinka(67680,67692) #  160401 - N - Odpadové strelivo
#kokocinka(67776,67788) #  160402 - N - Pyrotechnické odpady
#kokocinka(67872,67884) #  160403 - N - Iné odpadové výbušniny
#kokocinka(67968,67980) #  1605 - Plyny v tlakových nádobách a vyradené chemikálie
#kokocinka(68064,68076) #  160504 - N - Plyny v tlakových nádobách vrátane halónov obsahujúce nebezpečné látky
#kokocinka(68160,68172) #  160505 - O - Plyny v tlakových nádobách iné ako uvedené v 160504
#kokocinka(68256,68268) #  160506 - N - Laboratórne chemikálie pozostávajúce z nebezpečných látok alebo obsahujúce ne...
#kokocinka(68352,68364) #  160507 - N - Vyradené anorganické chemikálie pozostávajúce z nebezpečných látok alebo obsa...
#kokocinka(68448,68460) #  160508 - N - Vyradené organické chemikálie pozostávajúce z nebezpečných látok alebo obsahu...
#kokocinka(68544,68556) #  160509 - O - Vyradené chemikálie iné ako uvedené v 160506, 160507 alebo 160508
#kokocinka(68640,68652) #  1606 - Batérie a akumulátory
#kokocinka(68736,68748) #  160601 - N - Olovené batérie
#kokocinka(68832,68844) #  160602 - N - Niklovo-kadmiové batérie
#kokocinka(68928,68940) #  160603 - N - Batérie obsahujúce ortuť
#kokocinka(69024,69036) #  160604 - O - Alkalické batérie iné ako uvedené v 160603
#kokocinka(69120,69132) #  160605 - O - Iné batérie a akumulátory
#kokocinka(69216,69228) #  160606 - N - Oddelene zhromažďovaný elektrolyt z batérií a akumulátorov
#kokocinka(69312,69324) #  1607 - Odpady z čistenia prepravných nádrží, skladovacích nádrží a sudov (okrem 05 a...
#kokocinka(69408,69420) #  160708 - N - Odpady obsahujúce olej
#kokocinka(69504,69516) #  160709 - N - Odpady obsahujúce iné nebezpečné látky
#kokocinka(69600,69612) #  160799 - Odpady inak nešpecifikované
#kokocinka(69696,69708) #  1608 - Použité katalyzátory
#kokocinka(69792,69804) #  160801 - O - Použité katalyzátory obsahujúce zlato, striebro, rénium, ródium, paládium, ir...
#kokocinka(69888,69900) #  160802 - N - Použité katalyzátory obsahujúce nebezpečné prechodné kovy alebo nebezpečné zl...
#kokocinka(69984,69996) #  160803 - O - Použité katalyzátory obsahujúce prechodné kovy alebo zlúčeniny prechodných ko...
#kokocinka(70080,70092) #  160804 - O - Použité katalyzátory z krakovacích procesov okrem 160807
#kokocinka(70176,70188) #  160805 - N - Použité katalyzátory obsahujúce kyselinu fosforečnú
#kokocinka(70272,70284) #  160806 - N - Použité kvapaliny využité ako katalyzátor
#kokocinka(70368,70380) #  160807 - N - Použité katalyzátory kontaminované nebezpečnými látkami
#kokocinka(70464,70476) #  1609 - Oxidujúce látky
#kokocinka(70560,70572) #  160901 - N - Manganistany, napr. manganistan draselný (hypermangán)
#kokocinka(70656,70668) #  160902 - N - Chrómany, napr. chróman draselný, dvojchróman draselný alebo sodný
#kokocinka(70752,70764) #  160903 - N - Peroxidy, napr. peroxid vodíka
#kokocinka(70848,70860) #  160904 - N - Oxidujúce látky inak nešpecifikované
#kokocinka(70944,70956) #  1610 - Vodné kvapalné odpady určené na spracovanie mimo miesta ich vzniku
#kokocinka(71040,71052) #  161001 - N - Vodné kvapalné odpady obsahujúce nebezpečné látky
#kokocinka(71136,71148) #  161002 - O - Vodné kvapalné odpady iné ako uvedené v 161001
#kokocinka(71232,71244) #  161003 - N - Vodné koncentráty obsahujúce nebezpečné látky
#kokocinka(71328,71340) #  161004 - O - Vodné koncentráty iné ako uvedené v 161003
#kokocinka(71424,71436) #  1611 - Odpadové výmurovky a žiaruvzdorné materiály
#kokocinka(71520,71532) #  161101 - N - Výmurovky a žiaruvzdorné materiály na báze uhlíka z metalurgických procesov o...
#kokocinka(71616,71628) #  161102 - O - Výmurovky a žiaruvzdorné materiály na báze uhlíka z metalurgických procesov i...
#kokocinka(71712,71724) #  161103 - N - Iné výmurovky a žiaruvzdorné materiály z metalurgických procesov obsahujúce n...
#kokocinka(71808,71820) #  161104 - O - Iné výmurovky a žiaruvzdorné materiály z metalurgických procesov iné ako uved...
#kokocinka(71904,71916) #  161105 - N - Výmurovky a žiaruvzdorné materiály z nemetalurgických procesov obsahujúce neb...
#kokocinka(72000,72012) #  161106 - O - Výmurovky a žiaruvzdorné materiály z nemetalurgických procesov iné ako uveden...
#kokocinka(72096,72108) #  17 - Stavebné odpady a odpady z demolácií (vrátane výkopovej zeminy z kontaminovan...
#kokocinka(72192,72204) #  1701 - Betón, tehly, dlaždice, obkladačky a keramika
#kokocinka(72288,72300) #  170101 - O - Betón
#kokocinka(72384,72396) #  170102 - O - Tehly
#kokocinka(72480,72492) #  170103 - O - Obkladačky, dlaždice a keramika
#kokocinka(72576,72588) #  170106 - N - Zmesi alebo oddelené zložky betónu, tehál, obkladačiek, dlaždíc a keramiky ob...
#kokocinka(72672,72684) #  170107 - O - Zmesi betónu, tehál, obkladačiek, dlaždíc a keramiky iné ako uvedené v 170106
#kokocinka(72768,72780) #  1702 - Drevo, sklo a plasty
#kokocinka(72864,72876) #  170201 - O - Drevo
#kokocinka(72960,72972) #  170202 - O - Sklo
#kokocinka(73056,73068) #  170203 - O - Plasty
#kokocinka(73152,73164) #  170204 - N - Sklo, plasty a drevo obsahujúce nebezpečné látky alebo kontaminované nebezpeč...
#kokocinka(73248,73260) #  1703 - Bitúmenové zmesi, uhoľný decht a dechtové výrobky
#kokocinka(73344,73356) #  170301 - N - Bitúmenové zmesi obsahujúce uhoľný decht
#kokocinka(73440,73452) #  170302 - O - Bitúmenové zmesi iné ako uvedené v 170301
#kokocinka(73536,73548) #  170303 - N - Uhoľný decht a dechtové výrobky
#kokocinka(73632,73644) #  1704 - Kovy (vrátane ich zliatin)
#kokocinka(73728,73740) #  170401 - O - Meď, bronz, mosadz
#kokocinka(73824,73836) #  170402 - O - Hliník
#kokocinka(73920,73932) #  170403 - O - Olovo
#kokocinka(74016,74028) #  170404 - O - Zinok
#kokocinka(74112,74124) #  170405 - O - Železo a oceľ
#kokocinka(74208,74220) #  170406 - O - Cín
#kokocinka(74304,74316) #  170407 - O - Zmiešané kovy
#kokocinka(74400,74412) #  170409 - N - Kovový odpad kontaminovaný nebezpečnými látkami
#kokocinka(74496,74508) #  170410 - N - Káble obsahujúce olej, uhoľný decht a iné nebezpečné látky
#kokocinka(74592,74604) #  170411 - O - Káble iné ako uvedené v 170410
#kokocinka(74688,74700) #  1705 - Zemina (vrátane výkopovej zeminy z kontaminovaných plôch), kamenivo a materiá...
#kokocinka(74784,74796) #  170503 - N - Zemina a kamenivo obsahujúce nebezpečné látky
#kokocinka(74880,74892) #  170504 - O - Zemina a kamenivo iné ako uvedené v 170503
#kokocinka(74976,74988) #  170505 - N - Výkopová zemina obsahujúca nebezpečné látky
#kokocinka(75072,75084) #  170506 - O - Výkopová zemina iná ako uvedená v 170505
#kokocinka(75168,75180) #  170507 - N - Štrk zo železničného zvršku obsahujúci nebezpečné látky
#kokocinka(75264,75276) #  170508 - O - Štrk zo železničného zvršku iný ako uvedený v 170507
#kokocinka(75360,75372) #  1706 - Izolačné materiály a stavebné materiály obsahujúce azbest
#kokocinka(75456,75468) #  170601 - N - Izolačné materiály obsahujúce azbest
#kokocinka(75552,75564) #  170603 - N - Iné izolačné materiály pozostávajúce z nebezpečných látok alebo obsahujúce ne...
#kokocinka(75648,75660) #  170604 - O - Izolačné materiály iné ako uvedené v 170601 a 170603
#kokocinka(75744,75756) #  170605 - N - Stavebné materiály obsahujúce azbest
#kokocinka(75840,75852) #  1708 - Stavebný materiál na báze sadry
#kokocinka(75936,75948) #  170801 - N - Stavebné materiály na báze sadry kontaminované nebezpečnými látkami
#kokocinka(76032,76044) #  170802 - O - Stavebné materiály na báze sadry iné ako uvedené v 170801
#kokocinka(76128,76140) #  1709 - Iné odpady zo stavieb a demolácií
#kokocinka(76224,76236) #  170901 - N - Odpady zo stavieb a demolácií obsahujúce ortuť
#kokocinka(76320,76332) #  170902 - N - Odpady zo stavieb a demolácií obsahujúce pcb (napr. tesniace materiály obsahu...
#kokocinka(76416,76428) #  170903 - N - Iné odpady zo stavieb a demolácií vrátane zmiešaných odpadov obsahujúce nebez...
#kokocinka(76512,76524) #  170904 - O - Zmiešané odpady zo stavieb a demolácií iné ako uvedené v 170901, 170902 a 170903
#kokocinka(76608,76620) #  179900 - O - Drobný stavebný odpad
#kokocinka(76704,76716) #  18 - Odpady zo zdravotnej alebo veterinárnej starostlivosti alebo s nimi súvisiace...
#kokocinka(76800,76812) #  1801 - Odpady z pôrodníckej starostlivosti, diagnostiky, liečby alebo zdravotnej pre...
#kokocinka(76896,76908) #  180101 - O - Ostré predmety okrem 180103
#kokocinka(76992,77004) #  180102 - O - Časti a orgány tiel vrátane krvných vreciek a krvných konzerv okrem 180103
#kokocinka(77088,77100) #  180103 - N - Odpady, ktorých zber a zneškodňovanie podliehajú osobitným požiadavkám z hľad...
#kokocinka(77184,77196) #  180104 - O - Odpady, ktorých zber a zneškodňovanie nepodliehajú osobitným požiadavkám z hľ...
#kokocinka(77280,77292) #  180106 - N - Chemikálie pozostávajúce z nebezpečných látok alebo obsahujúce nebezpečné látky
#kokocinka(77376,77388) #  180107 - O - Chemikálie iné ako uvedené v 180106
#kokocinka(77472,77484) #  180108 - N - Cytotoxické a cytostatické liečivá
#kokocinka(77568,77580) #  180109 - O - Liečivá iné ako uvedené v 180108
#kokocinka(77664,77676) #  180110 - N - Amalgámový odpad z dentálnej starostlivosti
#kokocinka(77760,77772) #  1802 - Odpady z veterinárneho výskumu, diagnostiky, liečby a preventívnej starostliv...
#kokocinka(77856,77868) #  180201 - O - Ostré predmety okrem 180202
#kokocinka(77952,77964) #  180202 - N - Odpady, ktorých zber a zneškodňovanie podliehajú osobitným požiadavkám z hľad...
#kokocinka(78048,78060) #  180203 - O - Odpady, ktorých zber a zneškodňovanie nepodliehajú osobitným požiadavkám z hľ...
#kokocinka(78144,78156) #  180205 - N - Chemikálie pozostávajúce z nebezpečných látok alebo obsahujúce nebezpečné látky
#kokocinka(78240,78252) #  180206 - O - Chemikálie iné ako uvedené v 180205
#kokocinka(78336,78348) #  180207 - N - Cytotoxické a cytostatické liečivá
#kokocinka(78432,78444) #  180208 - O - Liečivá iné ako uvedené v 180207
#kokocinka(78528,78540) #  19 - Odpady zo zariadení na úpravu odpadu, z čistiarní odpadových vôd mimo miesta ...
#kokocinka(78624,78636) #  1901 - Odpady zo spayovania alebo pyrolýzy odpadu
#kokocinka(78720,78732) #  190102 - O - Železné materiály odstránené z popola
#kokocinka(78816,78828) #  190105 - N - Filtračný koláč z čistenia plynov
#kokocinka(78912,78924) #  190106 - N - Vodný kvapalný odpad z čistenia plynov a iný vodný kvapalný odpad
#kokocinka(79008,79020) #  190107 - N - Tuhý odpad z čistenia plynov
#kokocinka(79104,79116) #  190110 - N - Použité aktívne uhlie z čistenia dymových plynov
#kokocinka(79200,79212) #  190111 - N - Popol a škvára obsahujúce nebezpečné látky
#kokocinka(79296,79308) #  190112 - O - Popol a škvára iné ako uvedené v 190111
#kokocinka(79392,79404) #  190113 - N - Popolček obsahujúci nebezpečné látky
#kokocinka(79488,79500) #  190114 - O - Popolček iný ako uvedený v 190113
#kokocinka(79584,79596) #  190115 - N - Kotolný prach obsahujúci nebezpečné látky
#kokocinka(79680,79692) #  190116 - O - Kotolný prach iný ako uvedený v 190115
#kokocinka(79776,79788) #  190117 - N - Odpad z pyrolýzy obsahujúci nebezpečné látky
#kokocinka(79872,79884) #  190118 - O - Odpad z pyrolýzy iný ako uvedený v 190117
#kokocinka(79968,79980) #  190119 - O - Piesky z fluidnej vrstvy
#kokocinka(80064,80076) #  190199 - Odpady inak nešpecifikované
#kokocinka(80160,80172) #  1902 - Odpady z fyzikálnej alebo chemickej úpravy odpadu (vrátane odstraňovania chró...
#kokocinka(80256,80268) #  190203 - O - Predbežne zmiešaný odpad zložený len z odpadov neoznačených ako nebezpečné
#kokocinka(80352,80364) #  190204 - N - Predbežne zmiešaný odpad zložený len z odpadov, z ktorých aspoň jeden odpad j...
#kokocinka(80448,80460) #  190205 - N - Kaly z fyzikálno-chemického spracovania obsahujúce nebezpečné látky
#kokocinka(80544,80556) #  190206 - O - Kaly z fyzikálno-chemického spracovania iné ako uvedené v 190205
#kokocinka(80640,80652) #  190207 - N - Ropné látky a koncentráty zo separácie (separačných procesov)
#kokocinka(80736,80748) #  190208 - N - Kvapalné horľavé odpady obsahujúce nebezpečné látky
#kokocinka(80832,80844) #  190209 - N - Tuhé horľavé odpady obsahujúce nebezpečné látky
#kokocinka(80928,80940) #  190210 - O - Horľavé odpady iné ako uvedené v 190208 a 190209
#kokocinka(81024,81036) #  190211 - N - Iné odpady obsahujúce nebezpečné látky
#kokocinka(81120,81132) #  190299 - Odpady inak nešpecifikované
#kokocinka(81216,81228) #  1903 - Stabilizované a solidifikované odpady
#kokocinka(81312,81324) #  190304 - N - Čiastočne stabilizované odpady označené ako nebezpečné
#kokocinka(81408,81420) #  190305 - O - Stabilizované odpady iné ako uvedené v 190304
#kokocinka(81504,81516) #  190306 - N - Solidifikované odpady označené ako nebezpečné
#kokocinka(81600,81612) #  190307 - O - Solidifikované odpady iné ako uvedené v 190306
#kokocinka(81696,81708) #  190308 - N - Čiastočne stabilizovaná ortuť
#kokocinka(81792,81804) #  1904 - Vitrifikovaný odpad a odpad z vitrifikácie
#kokocinka(81888,81900) #  190401 - O - Vitrifikovaný odpad
#kokocinka(81984,81996) #  190402 - N - Popolček a iný odpad z úpravy dymových plynov
#kokocinka(82080,82092) #  190403 - N - Nevitrifikovaná tuhá fáza
#kokocinka(82176,82188) #  190404 - O - Vodný kvapalný odpad z ochladzovania vitrifikovaného odpadu
#kokocinka(82272,82284) #  1905 - Odpady z aeróbnej úpravy tuhých odpadov
#kokocinka(82368,82380) #  190501 - O - Nekompostované zložky komunálnych odpadov a podobných odpadov
#kokocinka(82464,82476) #  190502 - O - Nekompostované zložky živočíšneho a rastlinného odpadu
#kokocinka(82560,82572) #  190503 - O - Kompost nevyhovujúcej kvality
#kokocinka(82656,82668) #  190599 - Odpady inak nešpecifikované
#kokocinka(82752,82764) #  1906 - Odpady z anaeróbnej úpravy odpadu
#kokocinka(82848,82860) #  190603 - O - Kvapaliny z anaeróbnej úpravy komunálnych odpadov
#kokocinka(82944,82956) #  190604 - O - Zvyšky kvasenia z anaeróbnej úpravy komunálnych odpadov
#kokocinka(83040,83052) #  190605 - O - Kvapaliny z anaeróbnej úpravy živočíšneho a rastlinného odpadu
#kokocinka(83136,83148) #  190606 - O - Zvyšky kvasenia a kal z anaeróbnej úpravy živočíšneho a rastlinného odpadu
#kokocinka(83232,83244) #  190699 - Odpady inak nešpecifikované
#kokocinka(83328,83340) #  1907 - Priesaková kvapalina zo skládok odpadov
#kokocinka(83424,83436) #  190702 - N - Priesaková kvapalina zo skládky odpadov obsahujúca nebezpečné látky
#kokocinka(83520,83532) #  190703 - O - Priesaková kvapalina zo skládky odpadov iná ako uvedená v 190702
#kokocinka(83616,83628) #  1908 - Odpady z čistiarní odpadových vôd inak nešpecifikované
#kokocinka(83712,83724) #  190801 - O - Zhrabky z hrablíc
#kokocinka(83808,83820) #  190802 - O - Odpad z lapačov piesku
#kokocinka(83904,83916) #  190805 - O - Kaly z čistenia komunálnych odpadových vôd
#kokocinka(84000,84012) #  190806 - N - Nasýtené alebo použité iontomeničové živice
#kokocinka(84096,84108) #  190807 - N - Roztoky a kaly z regenerácie iontomeničov
#kokocinka(84192,84204) #  190808 - N - Odpad z membránových systémov s obsahom ťažkých kovov
#kokocinka(84288,84300) #  190809 - O - Zmesi tukov a olejov z odlučovačov oleja z vody obsahujúce jedlé oleje a tuky
#kokocinka(84384,84396) #  190810 - N - Zmesi tukov a olejov z odlučovačov oleja z vody iné ako uvedené v 190809
#kokocinka(84480,84492) #  190811 - N - Kaly obsahujúce nebezpečné látky z biologickej úpravy priemyselných odpadovýc...
#kokocinka(84576,84588) #  190812 - O - Kaly z biologickej úpravy priemyselných odpadových vôd iné ako uvedené v 190811
#kokocinka(84672,84684) #  190813 - N - Kaly obsahujúce nebezpečné látky z inej úpravy priemyselných odpadových vôd
#kokocinka(84768,84780) #  190814 - O - Kaly z inej úpravy priemyselných odpadových vôd iné ako uvedené v 190813
#kokocinka(84864,84876) #  190899 - Odpady inak nešpecifikované
#kokocinka(84960,84972) #  1909 - Odpady z úpravy pitnej vody alebo vody na priemyselné použitie
#kokocinka(85056,85068) #  190901 - O - Tuhé odpady z primárnych filtrov a hrablíc
#kokocinka(85152,85164) #  190902 - O - Kaly z čírenia vody
#kokocinka(85248,85260) #  190903 - O - Kaly z dekarbonizácie
#kokocinka(85344,85356) #  190904 - O - Použité aktívne uhlie
#kokocinka(85440,85452) #  190905 - O - Nasýtené alebo použité iontomeničové živice
#kokocinka(85536,85548) #  190906 - O - Roztoky a kaly z regenerácie iontomeničov
#kokocinka(85632,85644) #  190999 - Odpady inak nešpecifikované
#kokocinka(85728,85740) #  1910 - Odpady zo šrotovania kovových odpadov
#kokocinka(85824,85836) #  191001 - O - Odpad zo železa a z ocele
#kokocinka(85920,85932) #  191002 - O - Odpad z neželezných kovov
#kokocinka(86016,86028) #  191003 - N - Úletová frakcia a prach obsahujúce nebezpečné látky
#kokocinka(86112,86124) #  191004 - O - Úletová frakcia a prach iné ako uvedené v 191003
#kokocinka(86208,86220) #  191005 - N - Iné frakcie obsahujúce nebezpečné látky
#kokocinka(86304,86316) #  191006 - O - Iné frakcie iné ako uvedené v 191005
#kokocinka(86400,86412) #  1911 - Odpady z regenerácie olejov
#kokocinka(86496,86508) #  191101 - N - Použité filtračné hlinky
#kokocinka(86592,86604) #  191102 - N - Kyslé dechty
#kokocinka(86688,86700) #  191103 - N - Vodné kvapalné odpady
#kokocinka(86784,86796) #  191104 - N - Odpady z čistenia paliva zásadami
#kokocinka(86880,86892) #  191105 - N - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku obsahujúce nebezpe...
#kokocinka(86976,86988) #  191106 - O - Kaly zo spracovania kvapalného odpadu v mieste jeho vzniku iné ako uvedené v ...
#kokocinka(87072,87084) #  191107 - N - Odpady z čistenia dymových plynov
#kokocinka(87168,87180) #  191199 - Odpady inak nešpecifikované
#kokocinka(87264,87276) #  1912 - Odpady z mechanického spracovania odpadu (napr. triedenia, drvenia, lisovania...
#kokocinka(87360,87372) #  191201 - O - Papier a lepenka
#kokocinka(87456,87468) #  191202 - O - Železné kovy
#kokocinka(87552,87564) #  191203 - O - Neželezné kovy
#kokocinka(87648,87660) #  191204 - O - Plasty a guma
#kokocinka(87744,87756) #  191205 - O - Sklo
#kokocinka(87840,87852) #  191206 - N - Drevo obsahujúce nebezpečné látky
#kokocinka(87936,87948) #  191207 - O - Drevo iné ako uvedené v 191206
#kokocinka(88032,88044) #  191208 - O - Textílie
#kokocinka(88128,88140) #  191209 - O - Minerálne látky (napr. piesok, kamenivo)
#kokocinka(88224,88236) #  191210 - O - Horľavý odpad (palivo z odpadov)
#kokocinka(88320,88332) #  191211 - N - Iné odpady vrátane zmiešaných materiálov z mechanického spracovania odpadu ob...
#kokocinka(88416,88428) #  191212 - O - Iné odpady vrátane zmiešaných materiálov z mechanického spracovania odpadu in...
#kokocinka(88512,88524) #  1913 - Odpady zo sanácie pôdy a podzemnej vody
#kokocinka(88608,88620) #  191301 - N - Tuhé odpady zo sanácie pôdy obsahujúce nebezpečné látky
#kokocinka(88704,88716) #  191302 - O - Odpady zo sanácie pôdy iné ako uvedené v 191301
#kokocinka(88800,88812) #  191303 - N - Kaly zo sanácie pôdy obsahujúce nebezpečné látky
#kokocinka(88896,88908) #  191304 - O - Kaly zo sanácie pôdy iné ako uvedené v 191303
#kokocinka(88992,89004) #  191305 - N - Kaly zo sanácie podzemnej vody obsahujúce nebezpečné látky
#kokocinka(89088,89100) #  191306 - O - Kaly zo sanácie podzemnej vody iné ako uvedené v 191305
#kokocinka(89184,89196) #  191307 - N - Vodné kvapalné odpady a vodné koncentráty zo sanácie podzemnej vody obsahujúc...
#kokocinka(89280,89292) #  191308 - O - Vodné kvapalné odpady a vodné koncentráty zo sanácie podzemnej vody iné ako u...
#kokocinka(89376,89388) #  20 - Komunálne odpady (odpady z domácností a podobné odpady z obchodu, priemyslu a...
#kokocinka(89472,89484) #  2001 - Separovane zbierané zložky komunálnych odpadov (okrem 1501)
#kokocinka(89568,89580) #  200101 - O - Papier a lepenka
#kokocinka(89664,89676) #  200102 - O - Sklo
#kokocinka(89760,89772) #  200103 - O - Viacvrstvové kombinované materiály na báze lepenky (kompozity na báze lepenky)
#kokocinka(89856,89868) #  200108 - O - Biologicky rozložiteľný kuchynský a reštauračný odpad
#kokocinka(89952,89964) #  200110 - O - Šatstvo
#kokocinka(90048,90060) #  200111 - O - Textílie
#kokocinka(90144,90156) #  200113 - N - Rozpúšťadlá
#kokocinka(90240,90252) #  200114 - N - Kyseliny
#kokocinka(90336,90348) #  200115 - N - Zásady
#kokocinka(90432,90444) #  200117 - N - Fotochemické látky
#kokocinka(90528,90540) #  200119 - N - Pesticídy
#kokocinka(90624,90636) #  200121 - N - Žiarivky a iný odpad obsahujúci ortuť
#kokocinka(90720,90732) #  200123 - N - Vyradené zariadenia obsahujúce chlórfluórované uhľovodíky
#kokocinka(90816,90828) #  200125 - O - Jedlé oleje a tuky
#kokocinka(90912,90924) #  200126 - N - Oleje a tuky iné ako uvedené v 200125
#kokocinka(91008,91020) #  200127 - N - Farby, tlačiarenské farby, lepidlá a živice obsahujúce nebezpečné látky
#kokocinka(91104,91116) #  200128 - O - Farby, tlačiarenské farby, lepidlá a živice iné ako uvedené v 200127
#kokocinka(91200,91212) #  200129 - N - Detergenty obsahujúce nebezpečné látky
#kokocinka(91296,91308) #  200130 - O - Detergenty iné ako uvedené v 200129
#kokocinka(91392,91404) #  200131 - N - Cytotoxické a cytostatické liečivá
#kokocinka(91488,91500) #  200132 - O - Liečivá iné ako uvedené v 200131
#kokocinka(91584,91596) #  200133 - N - Batérie a akumulátory uvedené v 160601, 160602 alebo 160603 a netriedené baté...
#kokocinka(91680,91692) #  200134 - O - Batérie a akumulátory iné ako uvedené v 200133)
#kokocinka(91776,91788) #  200135 - N - Vyradené elektrické a elektronické zariadenia iné ako uvedené v 200121 a 2001...
#kokocinka(91872,91884) #  200136 - O - Vyradené elektrické a elektronické zariadenia iné ako uvedené v 200121, 20012...
#kokocinka(91968,91980) #  200137 - N - Drevo obsahujúce nebezpečné látky
#kokocinka(92064,92076) #  200138 - O - Drevo iné ako uvedené v 200137
#kokocinka(92160,92172) #  200139 - O - Plasty
#kokocinka(92256,92268) #  200140 - O - Kovy
#kokocinka(92352,92364) #  20014001 - O - Meď, bronz, mosadz
#kokocinka(92448,92460) #  20014002 - O - Hliník
#kokocinka(92544,92556) #  20014003 - O - Olovo
#kokocinka(92640,92652) #  20014004 - O - Zinok
#kokocinka(92736,92748) #  20014005 - O - Železo a oceľ
#kokocinka(92832,92844) #  20014006 - O - Cín
#kokocinka(92928,92940) #  20014007 - O - Zmiešané kovy
#kokocinka(93024,93036) #  200141 - O - Odpady z vymetania komínov
#kokocinka(93120,93132) #  200199 - Odpady inak nešpecifikované
#kokocinka(93216,93228) #  2002 - Odpady zo záhrad a z parkov (vrátane odpadu z cintorínov)
#kokocinka(93312,93324) #  200201 - O - Biologicky rozložiteľný odpad
#kokocinka(93408,93420) #  200202 - O - Zemina a kamenivo
#kokocinka(93504,93516) #  200203 - O - Iné biologicky nerozložiteľné odpady
#kokocinka(93600,93612) #  2003 - Iné komunálne odpady
#kokocinka(93696,93708) #  200301 - O - Zmesový komunálny odpad
#kokocinka(93792,93804) #  200302 - O - Odpad z trhovísk
#kokocinka(93888,93900) #  200303 - O - Odpad z čistenia ulíc
#kokocinka(93984,93996) #  200304 - O - Kal zo septikov
#kokocinka(94080,94092) #  200306 - O - Odpad z čistenia kanalizácie
#kokocinka(94176,94188) #  200307 - O - Objemný odpad
#kokocinka(94272,94284) #  200308 - O - Drobný stavebný odpad
#kokocinka(94368,94380) #  200399 - Komunálne odpady inak nešpecifikované
#kokocinka(94464,94476) #  N - Nebezpečné odpady
#kokocinka(94560,94572) #  O - Ostatné odpady
kokocinka(94656,94668) #  v - Všetky odpady






#SOME OLD TRASH
print("GOOD BYE WORLD")

