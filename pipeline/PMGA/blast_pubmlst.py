#!/usr/bin/env python3
### Import Modules ###
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
import os
import re
import json
from collections import OrderedDict
import operator
import csv
import pprint as pp
import string
import locale
import time
import tempfile
import argparse
import urllib3
import math
import sqlite3
from multiprocessing import Pool, Process, Queue
from subprocess import *
import pandas as pd
#call[("module", "load", "Python/3.4")]
#call[("module", "load", "ncbi-blast+/2.2.29")]
#call[("export", "BLASTDB=/blast/db")]

### SET UP DB connections and dictionaries ###
encoding = locale.getdefaultlocale()[1]
if not encoding:
	encoding ='UTF-8'
VERSION = "3"
_pubmlst_server = "pubmlst.biotech.cdc.gov"
SCRIPT_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.dirname(SCRIPT_PATH))
ABS_PATH = os.path.dirname(SCRIPT_PATH)
MASH_DB = os.path.join(ABS_PATH,"lib","species_db_v1_2.msh")
REFSEQ_DB = os.path.join(ABS_PATH,"lib","RefSeqSketchesDefaults.msh")
OUTPUT_DIR = ""
http = urllib3.PoolManager()
SQLITE_DB = os.path.join(ABS_PATH,"db","pubmlst_annotations")
PUBMLST_DB = os.path.join(ABS_PATH,"pubmlst_dbs_all")
conn = sqlite3.connect(SQLITE_DB)
c = conn.cursor()
SPECIES_DB = os.path.join(ABS_PATH,"db","species_db_v1_2")
conn_2 = sqlite3.connect(SPECIES_DB)
c_2 = conn_2.cursor()
DNA = ["A","T","C","G"]
gene_names ={"NEIS2357":"blaTEM-1","NEIS0123":"rpoB_full","NEIS2210":"tetM","HAEM1876":"ecs1","HAEM1877":"ecs2","HAEM1878":"ecs3","HAEM1879":"ecs4","HAEM1880":"ecs5","HAEM1881":"ecs6","HAEM1882":"ecs7","HAEM1883":"ecs8","HAEM1873":"fcs1","HAEM1874":"fcs2","HAEM1875":"fcs3","HAEM1018":"acrR","HAEM1019":"acrA","HAEM1020":"acrB","HAEM0902":"rplD-L4","HAEM0906":"rplV-L22","HAEM1263":"ftsI_full","HAEM0118":"blaTEM-1","HAEM1147":"hcsB","HAEM1148":"hcsA","HAEM1149":"bcs4","HAEM1150":"bcs3","HAEM1152":"bcs1","HAEM1153":"bexD","HAEM1156":"bexA","HAEM1151":"bcs2","HAEM1154":"bexC","HAEM1155":"bexB","HAEM1157":"hcsB","HAEM1158":"hcsA","HAEM1160":"bcs3","HAEM1161":"bcs2","HAEM1162":"bcs1","HAEM1163":"bexD","HAEM1164":"bexC","HAEM1165":"bexB","HAEM0810":"hpd","NEIS1015":"abcZ_full","NEIS1279":"aceF","NEIS1727":"ackA2","NEIS1729":"acnA","NEIS1492":"acnB","NEIS0486":"adhA","NEIS1241":"adhC","NEIS0767":"adk_full","NEIS1942":"aldA","NEIS1694":"amiC","NEIS0617":"ampD","NEIS1808":"ampG","NEIS1549":"aniA","NEIS2779":"aniA","NEIS1788":"anmK","NEIS0610":"apaH","NEIS1205":"ape1","NEIS0580":"argH","NEIS1810":"aroE_full","NEIS1769":"ArsR","NEIS1566":"AsnC","NEIS1185":"aspA","NEIS2274":"atlA","NEIS1859":"autA","NEIS1676":"bioF","NEIS0363":"carB","NEIS1645":"CcoN","NEIS1643":"CcoO","NEIS2019":"chpA","NEIS0775":"clpS","NEIS1237":"cmk","NEIS2743":"cnl","NEIS1995":"comP","NEIS2157":"csaA","NEIS2158":"csaB","NEIS2159":"csaC","NEIS2160":"csaD","NEIS2161":"csb","NEIS0051":"csc","NEIS2165":"cseA","NEIS2166":"cseB","NEIS2167":"cseC","NEIS2168":"cseD","NEIS2169":"cseE","NEIS2170":"cseF","NEIS2171":"cseG","NEIS2177":"cshC","NEIS2178":"cshD","NEIS2184":"cslA","NEIS2185":"cslB","NEIS2186":"cslC","NEIS2277":"cspA","NEIS0054":"cssA","NEIS0053":"cssB","NEIS0052":"cssC","NEIS0050":"cssE",
"NEIS2164":"cssF","NEIS2162":"csw","NEIS2187":"csxA","NEIS2188":"csxB","NEIS2189":"csxC","NEIS2163":"csy","NEIS2173":"cszA,cshA","NEIS2174":"cszB,cshB","NEIS2175":"cszC","NEIS2176":"cszD","NEIS0055":"ctrA","NEIS0056":"ctrB","NEIS0057":"ctrC","NEIS0058":"ctrD","NEIS0066":"ctrE","NEIS0067":"ctrF","NEIS0049":"ctrG","NEIS2066":"cybB","NEIS1094":"cysD","NEIS1096":"cysG","NEIS1095":"cysH","NEIS1091":"cysI","NEIS1092":"cysJ","NEIS1093":"cysN","NEIS0822":"cysU","NEIS0166":"dadA","NEIS1731":"ddpX","NEIS0321":"dnaN","NEIS1443":"dnaQ","NEIS0273":"dsbA1","NEIS1885":"dsbA2","NEIS1760":"dsbA3","NEIS2260":"dsbC","NEIS1220":"eno","NEIS2311":"eppA","NEIS0366":"ermB","NEIS2487":"ermE","NEIS2133":"etfB","NEIS2521":"exl2","NEIS2276":"exp1","NEIS2278":"exp2","NEIS1853":"farA","NEIS1852":"farB","NEIS0350":"fba","NEIS0004":"fbp","NEIS1022":"fbp","NEIS1963":"fetA","NEIS0340":"fetB2","NEIS0349":"fHbp","NEIS1353":"fis","NEIS1027":"folB","NEIS1609":"folP","NEIS1534":"fumA","NEIS1396":"fumC_full","NEIS0197":"fur","NEIS0062":"galE2","NEIS0048":"galE","NEIS1778":"galM","NEIS0581":"galU","NEIS2137":"gapA2",
"NEIS0199":"gapA","NEIS1290":"gatC","NEIS0419":"gcp","NEIS1331":"gdh_full","NEIS1018":"ggt","NEIS0015":"glmU","NEIS1809":"glnA","NEIS1830":"gloA","NEIS0930":"gltA","NEIS2070":"gmhA","NEIS2014":"gmhB","NEIS2006":"gntP","NEIS1524":"gpm","NEIS1547":"gpxA","NEIS1320":"gyrA","NEIS0204":"gyrB","NEIS2046":"hemk","NEIS0702":"hfq","NEIS0546":"hisE","NEIS0769":"hldA","NEIS2055":"hldC","NEIS0773":"hldD","NEIS1946":"hpuA","NEIS1947":"hpuB","NEIS1070":"hscA","NEIS1319":"hscB","NEIS0897":"icd","NEIS1959":"iga2","NEIS2237":"incC2","NEIS0153":"infA","NEIS0673":"infC","NEIS1218":"kdsA","NEIS0624":"kdsB","NEIS1815":"kdsC","NEIS2152":"kdtA","NEIS2239":"kfrB","NEIS2240":"kfrC","NEIS2236":"kleE","NEIS2235":"korC","NEIS1816":"kpsF","NEIS2199":"lacY","NEIS2200":"lacZ","NEIS1468":"lbpA","NEIS1469":"lbpB","NEIS1902":"lgtA","NEIS1901":"lgtB","NEIS2154":"lgtC","NEIS2155":"lgtD","NEIS1900":"lgtE","NEIS1618":"lgtF","NEIS2011":"lgtG","NEIS0291":"lot","NEIS0924":"lpdA2","NEIS1280":"lpd","NEIS1986":"lpt3","NEIS2012":"lpt6","NEIS1553":"lptA","NEIS1814":"lptC","NEIS0168":"lpxA","NEIS0191":"lpxB","NEIS0001":"lpxC","NEIS0171":"lpxD",
"NEIS0483":"lpxH","NEIS0621":"lpxK","NEIS0421":"lpxL2","NEIS1351":"lpxL","NEIS0384":"lspA","NEIS0899":"lst","NEIS2253":"ltgx","NEIS1162":"LysR","NEIS0488":"macA","NEIS0489":"macB","NEIS0620":"maeA","NEIS1789":"mafA MGI-1","NEIS0596":"mafA MGI-2","NEIS2083":"mafA MGI-3","NEIS0586":"mafB1 MGI-2","NEIS1800":"mafB-CT o1MGI-1","NEIS2575":"mafB-CT o1MGI-2","NEIS2576":"mafB-CT o3MGI-2","NEIS0597":"mafB MGI-1 or mafB2 MGI-2","NEIS2084":"mafB MGI-3","NEIS2574":"mafI1 MGI-2","NEIS0598":"mafI2 MGI-2","NEIS1799":"mafI MGI-1","NEIS0221":"mafI o1MGI-1","NEIS0223":"mafI o1MGI-2","NEIS1795":"mafI o2MGI-2","NEIS2087":"mafI o2MGI-3","NEIS2092":"mafI o3MGI-3","NEIS2577":"mafI o4MGI-3","NEIS2085":"mafI o5MGI-3","NEIS2508":"mafI o6MGI-3","NEIS1777":"mapA","NEIS2216":"marR","NEIS0161":"minD","NEIS0325":"mlp","NEIS2961":"mobA","NEIS2951":"mobC","NEIS1310":"modA","NEIS1194":"modB","NEIS2364":"modD","NEIS0304":"msbA","NEIS1811":"mtgA","NEIS1634":"mtrC","NEIS1633":"mtrD","NEIS1632":"mtrE","NEIS1635":"mtrR","NEIS1336":"mutY","NEIS1969":"nadA","NEIS0469":"nagZ","NEIS1657":"natC","NEIS1244":"ndk","NEIS2109":"nhba","NEIS0772":"nmgI",
"NEIS0763":"norM","NEIS0585":"ntpA","NEIS0238":"nuoB","NEIS0118":"nusG","NEIS1403":"opaA","NEIS1551":"opaB","NEIS2198":"opcA","NEIS1877":"opcB","NEIS1813":"ostA","NEIS0163":"oxyR","NEIS1216":"panD","NEIS2310":"parA","NEIS2238":"parB","NEIS2309":"parB","NEIS1525":"parC","NEIS1600":"parE","NEIS1203":"patA","NEIS1204":"patB","NEIS1278":"pdhC_full","NEIS1753":"penA","NEIS1326":"pgi1","NEIS1837":"pgi2","NEIS2148":"pgk","NEIS0213":"pglA","NEIS2839":"pglB2a","NEIS2840":"pglB2b","NEIS2838":"pglB2","NEIS0399":"pglB","NEIS0379":"pglC","NEIS0397":"pglC","NEIS0396":"pglD","NEIS0568":"pglE","NEIS0402":"pglF","NEIS0401":"pglG","NEIS0400":"pglH","NEIS0380":"pglI","NEIS0539":"pglL","NEIS2846":"pglN2","NEIS2841":"pglN","NEIS1776":"pgm2","NEIS0743":"pgm_full","NEIS0021":"pilA/ftsY","NEIS0020":"pilB/msrAB","NEIS0371":"pilC1","NEIS0033":"pilC2","NEIS1839":"pilD","NEIS0210":"pilE","NEIS1844":"pilF","NEIS1838":"pilG","NEIS0827":"pilH/fimT","NEIS0828":"pilI","NEIS0829":"pilJ","NEIS0830":"pilK","NEIS0412":"pilM","NEIS0411":"pilN","NEIS0410":"pilO","NEIS0409":"pilP","NEIS0408":"pilQ","NEIS0036":"pilT1","NEIS0721":"pilT2","NEIS0035":"pilU","NEIS0487":"pilV",
"NEIS1246":"pilW","NEIS0831":"pilX","NEIS0723":"pilZ","NEIS0905":"pip","NEIS0414":"ponA","NEIS1364":"porA","NEIS2020":"porB","NEIS0323":"ppk","NEIS1033":"proB","NEIS1733":"prpB","NEIS1732":"prpC","NEIS1766":"putA","NEIS0074":"pykA","NEIS2082":"pyrH","NEIS0692":"rbgA","NEIS1415":"recX","NEIS1925":"regF/sspA","NEIS1924":"regG/sspB","NEIS2217":"res","NEIS2134":"rfaC","NEIS1456":"rfaF","NEIS1619":"rfaK","NEIS0046":"rfbA","NEIS0047":"rfbB","NEIS0065":"rfbC2","NEIS0045":"rfbC","NEIS0657":"rlpB","NEIS0637":"rnc","NEIS1440":"rpiA","NEIS0120":"rplA","NEIS0135":"rplB","NEIS0132":"rplC","NEIS0133":"rplD","NEIS0144":"rplE","NEIS0147":"rplF","NEIS1257":"rplI","NEIS0121":"rplJ","NEIS0119":"rplK","NEIS0122":"rplL","NEIS2038":"rplM","NEIS0142":"rplN","NEIS0151":"rplO","NEIS0139":"rplP","NEIS0159":"rplQ","NEIS0148":"rplR","NEIS0531":"rplS","NEIS0675":"rplT","NEIS1847":"rplU","NEIS0137":"rplV","NEIS0134":"rplW","NEIS0143":"rplX","NEIS0817":"rplY","NEIS1848":"rpmA","NEIS1851":"rpmB","NEIS0140":"rpmC","NEIS0150":"rpmD","NEIS1928":"rpmE","NEIS0312":"rpmF","NEIS1850":"rpmG","NEIS0319":"rpmH","NEIS0674":"rpmI","NEIS0154":"rpmJ","NEIS1238":"rpsA","NEIS2080":"rpsB",
"NEIS0138":"rpsC","NEIS0157":"rpsD","NEIS0149":"rpsE","NEIS1260":"rpsF","NEIS0126":"rpsG","NEIS0146":"rpsH","NEIS2037":"rpsI","NEIS0129":"rpsJ","NEIS0156":"rpsK","NEIS0125":"rpsL","NEIS0155":"rpsM","NEIS0145":"rpsN","NEIS0552":"rpsO","NEIS0534":"rpsP","NEIS0141":"rpsQ","NEIS1258":"rpsR","NEIS0136":"rpsS","NEIS1688":"rpsT","NEIS1921":"rpsU","NEIS0927":"sdhA","NEIS0928":"sdhB","NEIS0925":"sdhC","NEIS0926":"sdhD","NEIS0117":"secE","NEIS1554":"serC","NEIS0825":"sodB","NEIS1339":"sodC","NEIS1682":"speA","NEIS1680":"speB","NEIS2303":"ssbB","NEIS2233":"ssb","NEIS2340":"stbB","NEIS2341":"stbC","NEIS0931":"sucA","NEIS0932":"sucB","NEIS0935":"sucC","NEIS0936":"sucD","NEIS1818":"talA","NEIS1690":"tbpA","NEIS1691":"tbpB","NEIS2210":"tetM","NEIS2334":"topA","NEIS2302":"topB","NEIS2255":"traA","NEIS2259":"traB","NEIS2202":"traC","NEIS2262":"traC","NEIS2249":"traD","NEIS2250":"traD","NEIS2248":"traE","NEIS2257":"traE","NEIS2247":"traF","NEIS2271":"traF","NEIS2246":"traG","NEIS2273":"traG","NEIS2272":"traH","NEIS2245":"traI","NEIS2251":"traI","NEIS2244":"traJ","NEIS2243":"traK","NEIS2258":"traK","NEIS2242":"traL","NEIS2256":"traL","NEIS2241":"traM","NEIS2352":"traM",
"NEIS2269":"traN","NEIS2266":"traU","NEIS2261":"traV","NEIS2265":"traW","NEIS2232":"trbA","NEIS2231":"trbB","NEIS2230":"trbC","NEIS2267":"trbC","NEIS2229":"trbD","NEIS2228":"trbE","NEIS2227":"trbF","NEIS2226":"trbG","NEIS2225":"trbH","NEIS2224":"trbI","NEIS2264":"trbI","NEIS2223":"trbJ","NEIS2222":"trbK","NEIS2221":"trbL","NEIS2351":"trbL","NEIS2220":"trbM","NEIS2350":"trbM","NEIS2219":"trbN","NEIS2234":"trfA","NEIS0609":"trkH","NEIS1829":"tspA","NEIS0116":"tuf","NEIS0128":"tuf","NEIS2218":"vapD","NEIS2956":"vapD","NEIS2955":"vapX","NEIS2332":"virB10","NEIS2333":"virB11","NEIS2323":"virB1","NEIS2324":"virB2","NEIS2325":"virB3","NEIS2326":"virB4","NEIS2327":"virB5","NEIS2328":"virB6","NEIS2329":"virB7","NEIS2330":"virB8","NEIS2331":"virB9","NEIS2338":"virBD2","NEIS2335":"virBD4","NEIS1990":"vsr","NEIS0256":"xseB","NEIS2252":"yaf","NEIS2254":"yag","NEIS2263":"ybe","NEIS2268":"ybi","NEIS2270":"ycb","NEIS2312":"ych1","NEIS2275":"ych","NEIS2279":"yda","NEIS2280":"ydbA","NEIS2281":"ydbB","NEIS2282":"ydcA","NEIS2283":"ydcB","NEIS2284":"ydd","NEIS2285":"ydeA","NEIS2286":"ydeB","NEIS2287":"ydf","NEIS2288":"ydg","NEIS2289":"ydhA","NEIS2290":"ydhB","NEIS2291":"ydi",
"NEIS2292":"yea","NEIS2293":"yeb","NEIS2294":"yecA","NEIS2295":"yecB","NEIS2296":"yedA","NEIS2297":"yedB","NEIS2298":"yee","NEIS2204":"yegA","NEIS2299":"yegA","NEIS2300":"yegB","NEIS2301":"yeh","NEIS2304":"yfa","NEIS2305":"yfb","NEIS2488":"yfcA","NEIS2306":"yfd","NEIS2307":"yfeA","NEIS2308":"yfeB","NEIS1812":"yhbG","NEIS0165":"zupT","NEIS0059":"tex"}
overlap_exceptions = ["tbpB","ftsI","porB","ponA","mtrR","parC","23S","rpoB","gyrA","penA","fhbp","fetA","porA","porB","nadA","nhbA","mafI","mafB","fucK","abcZ","adk","aroE","fumC","gdh","pdhC","pgm"]
longer_overlaps = ["csxA","csxB"]
length_exceptions = ["VR","pro","peptide"]
allele_exceptions = ["Promoter","NEIS2157","NEIS2158","NEIS2159","NEIS2160","NEIS0054","NEIS0053","NEIS0052","NEIS2161","NEIS0049","NEIS0051","NEIS0050","NEIS0049","NEIS2165","NEIS2166","NEIS2167","NEIS2168",
"NEIS2169","NEIS2170","NEIS2171","NEIS2173","NEIS2174","NEIS2177","NEIS2178","NEIS2184","NEIS2185","NEIS2186","NEIS2162","NEIS2164","NEIS2187","NEIS2188","NEIS2189","NEIS2163","NEIS2175","NEIS2176",
"NEIS0066","NEIS0067","NEIS0055","NEIS0056","NEIS0057","NEIS0058","NEIS0045","NEIS0046","NEIS0047","NEIS0048","NEIS0062","NEIS0065","Insertion_Element","Insertion_Elements",
"NEIS0351","NEIS1364","NEIS1969","NEIS2109","NadA_peptide","fuck","HAEM1122"]
promoter_regions = ["Promoter","pro_NEIS0349","pro_NEIS0350","pro_NEIS0488","pro_NEIS0763","pro_NEIS1635"]
igr = ["igr_NEIS1364_1365","igr_NEIS1968_1969","igr_NEIS2109_2110","igr_NEIS0405_0406","igr_NEIS0405_0406","igr_up_NEIS0055","igr_up_NEIS0349","igr_up_NEIS0350","igr_up_NEIS0351","igr_up_NEIS1364","igr_up_NEIS1969","igr_up_NEIS2109"]
serogroups = {"A":{"essential":["csaD","csaC","csaB","csaA","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "B":{"essential":["csb","cssC","cssB","cssA","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["ctrG","rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "C":{"essential":["csc","cssC","cssB","cssA","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["cssE","ctrG","rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "W":{"essential":["csw","cssC","cssB","cssA","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["cssF","ctrG","rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "Y":{"essential":["csy","cssC","cssB","cssA","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["cssF","ctrG","rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "E":{"essential":["cseA","cseB","cseC","cseD","cseE","cseG","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["cseF","rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "H":{"essential":["cshA","cshB","cshC","cshD","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "Z":{"essential":["cszA,cshA","cszB,cshB","cszC","cszD","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "I":{"essential":["csiA","csiB","csiC","csiD","csiE","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "K":{"essential":["cskA","cskB","cskC","cskD","cskE","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "L":{"essential":["cslA","cslB","cslC","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "X":{"essential":["csxA","csxB","csxC","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "cnl_1":{"essential":["tex","cnl","ctrE","ctrF"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  "cnl":{"essential":["tex","cnl"],"nonessential":["rfbC","rfbA","rfbB","galE","galE2","rfbB2","rfbA2","rfbC2"]},
			  }
serotypes = {
	"f":{"essential":["fcs1","fcs2","fcs3","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},
	"a":{"essential":["acs1","acs2","acs3","acs4","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},
	"c":{"essential":["ccs1","ccs2","ccs3","ccs4","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},
	"b":{"essential":["bcs1","bcs2","bcs3","bcs4","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},
	"d":{"essential":["dcs1","dcs2","dcs3","dcs4","dcs5","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},
	"e":{"essential":["ecs1","ecs2","ecs3","ecs4","ecs5","ecs6","ecs7","ecs8","bexA","bexB","bexC","bexD","hcsA","hcsB"],"nonessential":[]},	
}
capsule_gene_list = ["csaD","csaC","csaB","csaA","csb","cssC","cssB","cssA","csc","csw","csy","cseA","cseB","cseC","cseD",
						"cseE","cseG","cshA","cshB","cshC","cshD","cszA,cshA","cszB,cshB","cszC","cszD","csiA","csiB","csiC","csiD","csiE",
							"cskA","cskB","cskC","cskD","cskE","cslA","cslB","cslC","csxA","csxB","csxC","ctrA","ctrB","ctrC","ctrD","tex","ctrE","ctrF"]
ST_unique = {"fcs1":"f","fcs2":"f","fcs3":"f",
			"acs1":"a","acs2":"a","acs3":"a","acs4":"a",
			"ccs1":"c","ccs2":"c","ccs3":"c","ccs4":"c",
			"bcs1":"b","bcs2":"b","bcs3":"b","bcs4":"b",
			"dcs1":"d","dcs2":"d","dcs3":"d","dcs4":"d","dcs5":"d",
			"ecs1":"e","ecs2":"e","ecs3":"e","ecs4":"e","ecs5":"e","ecs6":"e","ecs7":"e","ecs8":"e"}

SG_unique = {"csaD":"A","csaC":"A","csaB":"A","csaA":"A",
				"csb":"B",
				"csc":"C",
				"csw":"W",
				"csy":"Y",
				"cseA":"E","cseB":"E","cseC":"E","cseD":"E","cseE":"E","cseG":"E","cseF":"E",
				"cshA":"H","cshB":"H","cshC":"H","cshD":"H",
				"cszC":"Z","cszD":"Z",
				"csiA":"I","csiB":"I","csiC":"I","csiD":"I","csiE":"I",
				"cskA":"K","cskB":"K","cskC":"K","cskD":"K","cskE":"K",
				"cslA":"L","cslB":"L","cslC":"L",
				"csxA":"X","csxB":"X","csxC":"X"}
			
#Change BMScan species names to PubMLST db name
species_dict = {"neisseria":"neisseria","Haemophilus influenzae":"hinfluenzae"}

### Check if output directory exists, if not, create, if yes, set global output to dir ###
def set_output(output):
	global OUTPUT_DIR
	OUTPUT_DIR = output
	if os.path.isdir(output):
		print("Output Directory",output,"already exists, not creating")
	else:
		os.system("mkdir {}".format(output))
		print("Created Output Directory",output)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)		

### Parse blast results, filter for best allele
# Note: input_file is just a key used for the dictionaries
def analyze_blast(results,input_file,seq_dict_fields):
	results_dict = {"species":seq_dict_fields[input_file]["species"],"contigs":{}}
	final_dict = {}
	final_dict[input_file] = {"species":seq_dict_fields[input_file]["species"],"contigs":{}}
	#final_dict[input_file]["species"] = seq_dict[input_file]["species"]
	for item in results:
		for line in item:
			line = line.decode(encoding)
			if line.strip() != "":
				pident = line.split("\t")[2]
				ident = float(pident)
				#only keep hits with 90% or greater identity
				if ident < 50.0:
					continue				
				query_name = line.split("\t")[0]
				contig = query_name
				if contig not in results_dict["contigs"]:
					results_dict["contigs"][contig] = {}
				subject = line.split("\t")[1]
				allele_num = subject.split("_")[-1]
				subject_name = re.sub(r'(_{})$'.format(allele_num),r'',subject)
				if subject_name not in results_dict["contigs"][contig]:
					results_dict["contigs"][contig][subject_name] = {}
				if subject_name in gene_names:
					allele_name = gene_names[subject_name]
				else:
					allele_name = subject_name
				qcovs = line.split("\t")[3]
				qstart = line.split("\t")[6]
				qend = line.split("\t")[7]
				score = float(line.split("\t")[10])
				send = int(line.split("\t")[9])
				sstart = int(line.split("\t")[8])
				a_length = int(line.split("\t")[11])
				s_len = int(line.split("\t")[13])
				q_len = int(line.split("\t")[12])
				qseq = line.split("\t")[15]
				if int(qstart) > int(qend):
					qstart = line.split("\t")[7]
					qend = line.split("\t")[6]
				coordinates = qstart+"*"+qend
				if coordinates not in results_dict["contigs"][contig][subject_name]:
					results_dict["contigs"][contig][subject_name][coordinates] = {}	
				if allele_num not in results_dict["contigs"][contig][subject_name][coordinates]:
					results_dict["contigs"][contig][subject_name][coordinates][allele_num] = []					
				try:
					sframe = str(line.split("\t")[14])
					qframe = str(line.split("\t")[16])
					sminus = "-" in sframe
					qminus = "-" in qframe
					if sminus and qminus:
						strand = '+'
					elif sminus or qminus:
						strand = '-'
					else:
						strand = '+'
				except:
					strand = "+"
				hit_info = {"allele_name":allele_name,"new":False,"length":a_length,"q_length":q_len,"identity":pident,"score":score,"qstart":qstart,"qend":qend,"contig":query_name,"strand":strand,"allele_id":allele_num,"s_length":s_len,"a_length":a_length,"qseq":qseq}
				results_dict["contigs"][contig][subject_name][coordinates][allele_num].append(hit_info)	
		
	complete_cov = {}
	for contig in results_dict["contigs"]:
		final_dict[input_file]["contigs"][contig] = {}
		false_hits = []
		contig_stop = int(seq_dict_fields[input_file]["contigs"][contig]["length"])		
		for allele in sorted(results_dict["contigs"][contig]):
			final_dict[input_file]["contigs"][contig][allele] = []
			for coordinates in sorted(results_dict["contigs"][contig][allele]):
				current_score = 0
				current_identity = 0.0
				current_cov = 0.0
				current_factor = 0.0				
				for allele_id in sorted(results_dict["contigs"][contig][allele][coordinates]):
					for a_num in results_dict["contigs"][contig][allele][coordinates][allele_id]:
						score = int(a_num["score"])
						identity = float(a_num["identity"])
						align_length = float(a_num["a_length"])
						subject_length = float(a_num["s_length"])
						query_length = float(a_num["q_length"])
						allele_name = a_num["allele_name"]
						start = int(a_num["qstart"])
						end = int(a_num["qend"])
						start_stop = str(start)+"*"+str(end)											
						cov = float(align_length/subject_length)
						if cov > 1.0:
							cov = 1.0
						factor = float(cov * identity)
						ident_cutoff = 0
						cov_cutoff = 0.70						   
						# factor is custom scoring (cov * identity) - compares each hit's factor vs current best factor within each allele set that hit the same region				
						if factor >= current_factor:					
							current_score = score
							current_identity = identity
							current_cov = cov
							current_factor = factor
							if end == contig_stop and identity >= 95.0:
								edge_match = True						
							elif start == 1 and identity >= 95.0 and cov < 1.0:
								edge_match = True
							else:
								edge_match = False														
							if a_num["strand"] is "+":
								qseq = seq_dict_fields[input_file]["contigs"][contig]["seq"][start-1:end]
							if a_num["strand"] is "-":												
								qseq = seq_dict_fields[input_file]["contigs"][contig]["seq"][start-1:end].reverse_complement()						
							if (current_identity < ident_cutoff or current_cov < cov_cutoff) and not edge_match and allele not in allele_exceptions:
								false_pos = True
							else:
								false_pos = False
							if current_cov > cov_cutoff:
								if allele not in complete_cov:
									complete_cov[allele] = True							
							remove_these = []			
							best_hit = True				
							#Checks current best allele against previously seen best alleles for this locus, and decides whether or not it remains the best
							if final_dict[input_file]["contigs"][contig][allele]:
								for seen_hits in final_dict[input_file]["contigs"][contig][allele]:
									r_start = int(seen_hits["qstart"])
									r_stop = int(seen_hits["qend"])
									r_score = int(seen_hits["score"])
									r_factor = float(seen_hits["factor"])
									r_length = int(seen_hits["subject_length"])
									if start <= r_start and end <= r_stop and end >= r_start:
										if current_factor > r_factor:
											remove_these.append(seen_hits)
										elif current_factor == r_factor:
											if subject_length < r_length:
												best_hit = False
											else:
												remove_these.append(seen_hits)
										else:
											best_hit = False																							
									elif start >= r_start and start <= r_stop and end >= r_stop:
										if current_factor > r_factor:
											remove_these.append(seen_hits)	
										elif current_factor == r_factor:
											if subject_length < r_length:
												best_hit = False 
											else:
												remove_these.append(seen_hits)
										else:
											best_hit = False																																					
									elif start >= r_start and start <= r_stop and end >= r_start and end <= r_stop:
										if current_factor > r_factor:
											remove_these.append(seen_hits)
										elif current_factor == r_factor:
											if subject_length < r_length:
												best_hit = False 
											else:
												remove_these.append(seen_hits)																						   
										else:
											best_hit = False																																						
									elif start <= r_start and start <= r_stop and end >= r_start and end >= r_stop:
										if current_factor > r_factor:
											remove_these.append(seen_hits)
										elif current_factor == r_factor:
											if subject_length < r_length:
												best_hit = False
											else:
												remove_these.append(seen_hits)												
										else:
											best_hit = False	
										
							if not best_hit:
								false_pos = True																										
							for hits in remove_these:
								final_dict[input_file]["contigs"][contig][allele].remove(hits)	
							if allele in promoter_regions:
								region_type = "PRO"
							elif allele in igr:
								region_type = "IGR"
							elif "Insertion_Element" in allele:
								region_type = "ISE"
							elif "NEISp" in allele:
								region_type = "PEP"
							else:
								region_type = "CDS"
							#Stores metadata in final results dict									
							hit = {"region_type":region_type,"false_pos":false_pos,"allele":allele,"factor":factor,"allele_name":allele_name,"edge":edge_match,"new":False,"qseq":str(qseq),"cov":cov,"subject_length": subject_length, "align_length":align_length,"allele_id":a_num["allele_id"],"identity":current_identity,"score":current_score,"contig":a_num["contig"],"strand":a_num["strand"],"qstart":a_num["qstart"],"qend":a_num["qend"]}
							final_dict[input_file]["contigs"][contig][allele].append(hit)	
																	
	for allele in complete_cov:
		if allele in allele_exceptions:
			continue
		for contig in final_dict[input_file]["contigs"]:
			if contig == "species":
				continue			
			if allele in final_dict[input_file]["contigs"][contig]:
				for hit in final_dict[input_file]["contigs"][contig][allele]:
					if hit["cov"] < cov_cutoff:
						hit["false_pos"] = True		
	return final_dict


#~ c.execute("select * from Gene where name like'{}'".format(edited_allele))
#~ a_result = c.fetchone()
#~ if a_result:
	#~ allele_db_id = a_result[0]
	#~ c.execute("select * from Annotation where gene_id='{}'".format(allele_db_id))
	#~ results = c.fetchall()

def sql_find_allele(edited_allele):
	c.execute("select * from Gene where name like'{}'".format(edited_allele))
	a_result = c.fetchone()
	return a_result
	
def sql_get_annotations(allele_db_id):
	c.execute("select * from Annotation where gene_id='{}'".format(allele_db_id))
	results = c.fetchall()
	return results
	
## Step 2 - finds best hit per coordinate range	and pulls pubmlst info for best hits
def analyze_results(results_dict,threads,internal_stop):
	print("Parsing BLAST data to identify alleles to extract from pubMLST")
	### Gets id-specific allele information such as sequence and flag information from pubMLST for each result ###
	internal_stop_dict = {}
	alleles_to_grab = {}
	allele_info = {}
	allele_count = 0
	allele_annotations = {}	
	for in_file in sorted(results_dict):
		if "species" in results_dict[in_file]:
			species = results_dict[in_file]["species"]
		else:
			results_dict[in_file]["species"] = "neisseria"
			species = results_dict[in_file]["species"]			
		if species not in alleles_to_grab:
			alleles_to_grab[species] = {}			
		false_pos = {}
		edge_cases = {}
		for contig in sorted(results_dict[in_file]["contigs"]):
			if contig == "species": #Legacy compatability
				continue
			edge_cases[contig] = {}
			seen_regions = {}				
			if contig not in false_pos:
				false_pos[contig] = {}
			for allele in sorted(results_dict[in_file]["contigs"][contig]):
				if allele not in false_pos[contig]:
					false_pos[contig][allele] = []
				if allele in gene_names:
					for hit in results_dict[in_file]["contigs"][contig][allele]:
						hit["allele_name"] = gene_names[allele]
				if results_dict[in_file]["contigs"][contig][allele]:				
					for hit in results_dict[in_file]["contigs"][contig][allele]:					
						false_positive = hit["false_pos"]						
						if false_positive:
							false_pos[contig][allele].append(hit)
							continue				
						hits_to_remove = []		
						allele_name = hit["allele_name"]							
						allele_id = hit["allele_id"]				 
						start = int(hit["qstart"])					 
						stop = int(hit["qend"])
						score = float(hit["factor"])
						edge_match = hit["edge"]
						add = False
						found_overlap = False
						if seen_regions:
							for region in sorted(seen_regions):
								add_region = False
								remove_region = True
								replace = False
								current_hit_allele_original = seen_regions[region]["hit"]["allele"]
								current_hit_allele = seen_regions[region]["hit"]["allele_name"]
								r_start = int(region.split("*")[0])					
								r_stop = int(region.split("*")[1])							
								ignore_flag = False
								if (start <= r_start and stop <= r_stop and stop >= r_start) or	(start >= r_start and stop <= r_stop and stop >= r_start):
									distance = int(abs(stop-r_start))
									r_distance = int(r_stop-r_start)
									overlap_frac = float(distance/r_distance)*100
									overlap_dist = max(overlap_frac,50)
									#print("1",start,stop,allele,contig,region,distance,score,seen_regions[region]["score"],overlap_dist)									
									if distance <= 100:
										add_region = True
										remove_region = False
									if allele_name in longer_overlaps and current_hit_allele in longer_overlaps:
										add_region = True
										remove_region = False
									if "NEISp" in current_hit_allele_original:
										#print(in_file,"allele:{}_cha:{}".format(allele,current_hit_allele_original))
										if current_hit_allele_original.replace("NEISp","NEIS").lower() == allele.lower():
											add_region = True
											#print("added")
											remove_region = False
									elif "NEISp" in allele:
										#print(in_file,"allele:{}_cha:{}".format(allele,current_hit_allele_original))								
										if allele.replace("NEISp","NEIS").lower() == current_hit_allele_original.lower():
											add_region = True	
											#print("added")									
											remove_region = False
									for exception in overlap_exceptions:
										if exception.lower() in allele_name.lower() and exception.lower() in current_hit_allele.lower():										
											add_region = True
											remove_region = False	
										elif exception.lower() in current_hit_allele.lower() and allele_name == "Insertion_Element":
											add_region = True			
									if score > seen_regions[region]["score"] or add_region:
										add = True
										if remove_region:
											hits_to_remove.append(region)								
									else:
										false_positive = True
									found_overlap = True									
								if start >= r_start and start <= r_stop and stop >= r_stop:
									distance = int(abs(start-r_stop))
									r_distance = int(r_stop-r_start)
									overlap_dist = float(distance/r_distance)	
									overlap_dist = max(overlap_dist,50)																	
									if distance <= 100:
										add_region = True
										remove_region = False
									if allele_name in longer_overlaps and current_hit_allele in longer_overlaps:
										add_region = True
										remove_region = False										
									for exception in overlap_exceptions:
										if exception.lower() in allele_name.lower() and exception.lower() in current_hit_allele.lower():
											add_region = True
											remove_region = False	
										elif exception.lower() in current_hit_allele.lower() and allele_name == "Insertion_Element":
											add_region = True			
									if score > seen_regions[region]["score"] or add_region:
										add = True
										if remove_region:
											hits_to_remove.append(region)								
									else:
										false_positive = True
									found_overlap = True	
																									
								if start >= r_start and start <= r_stop and stop >= r_start and stop <= r_stop:
									if allele_name in longer_overlaps and current_hit_allele in longer_overlaps:
										add_region = True
										remove_region = False									
									for exception in overlap_exceptions:
										if exception.lower() in allele_name.lower() and exception.lower() in current_hit_allele.lower():										
											add_region = True
											remove_region = False	
										elif exception.lower() in current_hit_allele.lower() and allele_name == "Insertion_Element":
											add_region = True			
									if score > seen_regions[region]["score"] or add_region:
										add = True
										if remove_region:
											hits_to_remove.append(region)								
									else:
										false_positive = True
									found_overlap = True	
																										
								if start <= r_start and start <= r_stop and stop >= r_start and stop >= r_stop:
									if allele_name in longer_overlaps and current_hit_allele in longer_overlaps:
										add_region = True
										remove_region = False																
									for exception in overlap_exceptions:
										if exception.lower() in allele_name.lower() and exception.lower() in current_hit_allele.lower():										
											add_region = True
											remove_region = False	
										elif exception.lower() in current_hit_allele.lower() and allele_name == "Insertion_Element":
											add_region = True			
									if score > seen_regions[region]["score"] or add_region:
										add = True
										if remove_region:
											hits_to_remove.append(region)								
									else:
										false_positive = True
									found_overlap = True	
																																
						else:
							new_region = str(start)+"*"+str(stop)								
							seen_regions[new_region] = {"score":score,"hit":hit}
						if not found_overlap:
							new_region = str(start)+"*"+str(stop)								
							seen_regions[new_region] = {"score":score,"hit":hit}
						if false_positive:
							false_pos[contig][allele].append(hit)
							continue
						if hit["region_type"] == "ISE":
							if float(hit["cov"]) < .05:
								if not hit["edge"]:
									false_pos[contig][allele].append(hit)
						if hit["edge"]:
							if hit["cov"] < 0.10 or len(hit["qseq"]) < 100:
								false_pos[contig][allele].append(hit)
						else:
							for length_name in length_exceptions:
								if length_name in hit["allele_name"]:
									continue
							if hit["cov"] < 0.10 or (len(hit["qseq"]) < 70 and hit["cov"] < .90):
								false_pos[contig][allele].append(hit)
						if add:
							new_region = str(start)+"*"+str(stop)
							for to_remove in hits_to_remove:
								if to_remove in seen_regions:
									hit_to_remove = seen_regions[to_remove]["hit"]
									allele_to_remove = hit_to_remove["allele"]
									allele_id_to_remove = hit_to_remove["allele_id"]
									false_pos[contig][allele_to_remove].append(hit_to_remove)
									seen_regions.pop(to_remove,None)
							seen_regions[new_region] = {"score":score,"hit":hit}									
						if allele not in alleles_to_grab[species]:
							alleles_to_grab[species][allele] = []
							allele_annotations[allele] = ""			
						if allele_id not in alleles_to_grab[species][allele]:
							alleles_to_grab[species][allele].append(allele_id)
						else:
							continue
						edited_allele = allele.replace("'","")
						for i in range(0,10000):
							try:	 
								a_result = sql_find_allele(edited_allele)
								break
							except:
								print("failed to get {} from sql DB, retrying".format(edited_allele))
						if a_result:
							allele_db_id = a_result[0]
							for i in range(0,10000):
								try:
									results = sql_get_annotations(allele_db_id)
									break
								except:
									print("failed to get annotations for {} from sql DB, retrying".format(edited_allele))									
							annotations = []
							for obj in results:
								desc = obj[4]
								if desc not in annotations:
									annotations.append(desc)
							if len(annotations) > 1:
								allele_annotations[allele] = ",".join(annotations)
							elif len(annotations) == 1:
								allele_annotations[allele] = annotations[0]
							else:
								allele_annotations[allele] = "None Found"
						else:
							allele_annotations[allele] = "None Found"
			for allele in false_pos[contig]:
				for hit in false_pos[contig][allele]:
					if hit in results_dict[in_file]["contigs"][contig][allele]:
						results_dict[in_file]["contigs"][contig][allele].remove(hit)
	for species in alleles_to_grab:
		for allele in alleles_to_grab[species]:
			for allele_id in alleles_to_grab[species][allele]:
				allele_count+=1									
	print("Grabbing allele information from pubMLST for {} alleles".format(allele_count))				
	q=0
	for species in alleles_to_grab:
		for allele in alleles_to_grab[species]:
			if allele not in allele_info:
				allele_info[allele] = {}		
			for allele_id in alleles_to_grab[species][allele]:
				if "Haemophilus influenzae" in species:
					temp_species = "hinfluenzae"
				else:
					temp_species = species
				url = "http://{}/db/pubmlst_{}_seqdef/loci/{}/alleles/{}".format(_pubmlst_server,temp_species,allele,allele_id)
				request = http.request('GET',url)
				request_data = json.loads(request.data.decode('utf-8'))					
				#pp.pprint(request_data)
				if allele_id not in allele_info[allele]:
					allele_info[allele][allele_id] = {}
				if "flags" in request_data:
					flags = request_data["flags"]
				else:
					flags = []
				if "comments" in request_data:
					comments = request_data["comments"]
				else:
					comments = []
				for field in request_data:
					if "mutation" in field:
						allele_info[allele][allele_id][field] = request_data[field]
				allele_info[allele][allele_id]["flags"] = flags
				allele_info[allele][allele_id]["comments"] = comments
				q+=1
				if (q%500) == 0:
						print("Completed {} so far".format(str(q)))
		
		
	print("Compiling results")
	for in_file in results_dict:	
		for contig in results_dict[in_file]["contigs"]:
			if contig == "species":
				continue
			q=0			
			for allele in results_dict[in_file]["contigs"][contig]:
				if results_dict[in_file]["contigs"][contig][allele]:
					for hit in results_dict[in_file]["contigs"][contig][allele]:
						q+=1
						false_positive = hit["false_pos"]
						hit["annotations"] = allele_annotations[allele]
						if not false_positive:
							identity = float(hit["identity"])
							edge_match = hit["edge"]
							qseq = hit["qseq"]
							cov = hit["cov"]
							allele_id = hit["allele_id"]
							sequence = qseq
							DNA_flag = True							
							for letter in sequence:
								if letter not in DNA:
									DNA_flag = False
									break
							if DNA_flag:							
								seq_obj = Seq(sequence, IUPAC.unambiguous_dna)	
							if identity < 100.0:				
								hit["new"] = True
								hit["flags"] = []
								hit["allele_id"] = "new_allele_similar_to_{}_identity({})%_cov({})%".format(allele_id,identity,round(cov*100,2))
								allele_id=hit["allele_id"]
							elif cov != 1:	
								if edge_match:
									hit["allele_id"] = "edge_match_partial_cov_({}%)_most_similar_to_{}".format(round(cov*100,2),allele_id)
								else:
									hit["allele_id"] = "partial_cov_({}%)_most_similar_to_{}".format(round(cov*100,2),allele_id)
								hit["flags"] = []
								allele_id = hit["allele_id"]
							else:
								if allele in allele_info:
									hit["flags"] = allele_info[allele][allele_id]["flags"]
									hit["comments"] = allele_info[allele][allele_id]["comments"]
									for field in allele_info[allele][allele_id]:
										if "mutation" in field:
											hit[field] = allele_info[allele][allele_id][field]			
								if sequence != "N/A":
									for letter in sequence:
										if letter not in DNA:
											DNA_flag = False
											break								
							if not edge_match and DNA_flag and sequence != "N/A":
								protein_sequence = seq_obj.translate(table=11)
								if protein_sequence.endswith("*"):
									protein_sequence = protein_sequence[:-1]
								else:
									if "*" in protein_sequence and cov == 1:
										stop_location = protein_sequence.rfind("*")
										stop_location = int(stop_location*3)+3
										new_sequence = sequence[:stop_location]
										hit["qseq"] = new_sequence
										new_end = int(hit["qstart"])+stop_location
										hit["qend"] = new_end
										seq_obj = Seq(new_sequence, IUPAC.unambiguous_dna)
										protein_sequence = seq_obj.translate(table=11)
										protein_sequence = protein_sequence[:-1]								
										if "Adjusted to last stop codon" not in hit["flags"]:
											hit["flags"].append("Adjusted to last stop codon")
									else:
										if "No stop codon detected" not in hit["flags"]:
											hit["flags"].append("No stop codon detected")
										
								internal_stops = int(protein_sequence.count("*"))
								if internal_stops > 0:
									if internal_stop and hit["allele_name"] in capsule_gene_list:
										if in_file not in internal_stop_dict:
											internal_stop_dict[in_file] = {}
										internal_stop_locations = list(find_all(str(protein_sequence),"*"))
										gene_internal_stop_locations = [str(x*3) for x in internal_stop_locations]
										gene_length = len(sequence)
										if hit["allele_name"] not in internal_stop_dict[in_file]:
											internal_stop_dict[in_file][hit["allele_name"]] = {"stops":gene_internal_stop_locations,"length":gene_length}
										else:
											hit_name = "{}_{}".format(hit["allele_name"],q)
											internal_stop_dict[in_file][hit_name] = {"stops":gene_internal_stop_locations,"length":gene_length}
									if "internal stop codon" not in hit["flags"]:
										new_flag = hit["new"]
										hit["flags"].append("internal stop codon")	
										if "N/A" in hit["flags"]:
											hit["flags"].pop("N/A")
																	
								 
	return results_dict,internal_stop_dict
			
def create_gff(results_dict,scheme_data,seq_dict):
	for in_file in results_dict:
		text = ""
		header_info = ""		
		fasta_text = ""
		out_path = os.path.join(OUTPUT_DIR,"gff")
		with open(os.path.join(out_path,"{}.gff".format(in_file.replace(".fasta",""))),"w") as f:	
			print_file = False
			for contig in results_dict[in_file]["contigs"]:
				if contig == "species":
					continue					
				count=0

				for allele in results_dict[in_file]["contigs"][contig]:
					if results_dict[in_file]["contigs"][contig][allele]:
						for hit in results_dict[in_file]["contigs"][contig][allele]:
							if contig in seq_dict[in_file]["contigs"]:
								seq_dict[in_file]["contigs"][contig]["alleles"][count] = hit 
								count+=1
							else:
								print_file = True
			if print_file:
				print(in_file,"needs rerun")
			for contig,_ in sorted(seq_dict[in_file]["contigs"].items(),key=lambda x: int(x[1]["length"]),reverse=True):
				sequence = seq_dict[in_file]["contigs"][contig]["seq"]
				seq_length = seq_dict[in_file]["contigs"][contig]["length"]				
				if seq_dict[in_file]["contigs"][contig]["alleles"]:
					for hit,_ in sorted(seq_dict[in_file]["contigs"][contig]["alleles"].items(),key= lambda x: int(x[1]["qstart"])):			
						allele_name = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["allele_name"]
						allele = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["allele"]
						scheme_list = []
						for scheme in scheme_data:
							if allele in scheme_data[scheme]:
								scheme_list.append(scheme)
						scheme_type = ', '.join(scheme_list) if len(scheme_list) > 0 else 'N/A'
						allele_id = str(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["allele_id"])
						start = str(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["qstart"])						
						stop = str(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["qend"])						
#						score = str(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["score"])						
						strand = str(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["strand"])						
						raw_flags = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["flags"]
						if len(raw_flags) == 1:
							flags = raw_flags[0]
						elif len(raw_flags) > 1:
							flags = ",".join(raw_flags)
						else:
							flags = "N/A"
						if "N/A" in flags and "internal" in flags:
							flags.replace("N/A","")
						annotations = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["annotations"]
						new = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["new"]
						edge_match = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["edge"]
						identity = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["identity"]
#						a_length = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["align_length"]
#						s_length = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["subject_length"]
						region_type = seq_dict[in_file]["contigs"][contig]["alleles"][hit]["region_type"]
						cov = float(seq_dict[in_file]["contigs"][contig]["alleles"][hit]["cov"])
						cov = round(cov,2)
						cov = cov*100.0
						if new and edge_match:
							text += contig +"\t" + "pubMLST" + "\t" + "{}".format(region_type) + "\t" + start + "\t" + stop + "\t" + "." + "\t" + strand + "\t" + "0" + "\t" + "ID={}_{};gene={};allele_id={};inference={};locus_tag={}_{};flags={};product={};scheme={}\n".format(contig,count,allele_name,allele_id,"pubmlst",contig,count,flags,annotations,scheme_type)							
						elif new and not edge_match:
							text += contig +"\t" + "pubMLST" + "\t" + "{}".format(region_type) + "\t" + start + "\t" + stop + "\t" + "." + "\t" + strand + "\t" + "0" + "\t" + "ID={}_{};gene={};allele_id={};inference={};locus_tag={}_{};flags={};product={};scheme={}\n".format(contig,count,allele_name,allele_id,"pubmlst",contig,count,flags,annotations,scheme_type)
						elif cov != 100:
							text += contig +"\t" + "pubMLST" + "\t" + "{}".format(region_type) + "\t" + start + "\t" + stop + "\t" + "." + "\t" + strand + "\t" + "0" + "\t" + "ID={}_{};gene={};allele_id={};inference={};locus_tag={}_{};flags={};product={};scheme={}\n".format(contig,count,allele_name,allele_id,"pubmlst",contig,count,flags,annotations,scheme_type)
						else:
							text += contig +"\t" + "pubMLST" + "\t" + "{}".format(region_type) + "\t" + start + "\t" + stop + "\t" + "." + "\t" + strand + "\t" + "0" + "\t" + "ID={}_{};gene={};allele_id={};inference={};locus_tag={}_{};flags={};product={};scheme={}\n".format(contig,count,allele_name,allele_id,"pubmlst",contig,count,flags,annotations,scheme_type)
						count+=1
				header_info += "##sequence-region {} 1 {}\n".format(contig,str(seq_length))
				fasta_text += ">{}\n".format(contig)
				fasta_text += "{}\n".format(sequence)
			f.write("##gff-version 3\n")
			f.write(header_info)
			f.write(text)
			f.write("##FASTA\n")
			f.write(fasta_text)

def blast_command(blast_db,query_file,threads_to_use,nucl):
	if nucl:
		results = check_output(["blastn","-db",blast_db,"-outfmt","6 qseqid sseqid pident qcovus mismatch gapopen qstart qend sstart send score length qlen slen sframe qseq qframe","-query",query_file,"-num_threads",threads_to_use,"-max_target_seqs","200"], shell=False)
	else:
		results = check_output(["blastx","-db",blast_db,"-outfmt","6 qseqid sseqid pident qcovus mismatch gapopen qstart qend sstart send score length qlen slen sframe qseq qframe","-query",query_file,"-num_threads",threads_to_use,"-query_gencode","11","-max_target_seqs","200","-seg","no"], shell=False)
	return results


def run_blast(working_dir,input_file,threads_to_use,blast_dir,seq_dict,seq_dict_key):
	processes = int(threads_to_use)
	print("Blasting against pubMLST database with",threads_to_use,"workers for file {}".format(input_file))
	## Setup pool for multiprocessing ###
	pool = Pool(processes)	
	folders = {}
	i=0
	### Setup 2d array to arrange jobs for multiprocessing ###
	folders[i] = {}
	folders = []
	for folder in os.listdir(blast_dir):
		folders.append(folder)
	### setup query file path and check if blast DB is protein or nucleotide ###
	query_file = os.path.join(working_dir,input_file)	
	nucl_dict = {}
	for folder in folders:
		nucl = True
		for item in os.listdir(os.path.join(blast_dir,folder)):
			if ".pin" in item:
				nucl = False
		nucl_dict[folder] = nucl
	### list comprehension to launch blast_command for each thread - sends all jobs to pool and pool updates jobs as others finish ###
	blast_time = [pool.apply_async(blast_command,args=(os.path.join(blast_dir,folder,folder),query_file,"1",nucl_dict[folder])) for folder in folders]
	output = [result.get() for result in blast_time]
	blast_final_results = [re.split(b"\n",item.rstrip()) for item in output]
	print("Completed BLAST for",input_file)	
	pool.terminate()  
	final_dict = analyze_blast(
			blast_final_results,
			seq_dict_key,
			seq_dict
			)
	print("BLAST dict has {} records".format(len(final_dict)))
	return final_dict	

def get_schemes():
	print("Obtaining pubMLST schemes")
	### Obtain list of schemes and then each scheme individually from pubMLST for Neisseria sp. and load into dict ###
	schemes = {}
	#scheme_url = "http://{}/db/pubmlst_neisseria_seqdef/schemes".format(_pubmlst_server)
	scheme_url = "http://rest.pubmlst.org/db/pubmlst_neisseria_seqdef/schemes"
	scheme_request = http.request('GET',scheme_url)
	scheme_request_data = json.loads(scheme_request.data.decode('utf-8'))
	#pp.pprint(scheme_request_data)
	for scheme in scheme_request_data["schemes"]:
		url = scheme["scheme"]
		#print(url)
		request = http.request('GET',url)
		request_data = json.loads(request.data.decode('utf-8'))
		#pp.pprint(request_data)
		#~ if "description" not in request_data:
			#~ print(request_data)
		description = request_data["description"]
		if "loci" in request_data:
			schemes[description] = []			
			for loci in request_data["loci"]:
				allele = loci.split("/")[-1]
				schemes[description].append(allele)
	print("Schemes obtained")
	return schemes	

def calc_frequencies(final_results_dict,char_data):
	frequencies = {}
	#pp.pprint(final_results_dict)	
	## Get counts of samples for each group ##
	for entry in char_data:
		group = char_data[entry]
		if group not in frequencies:
			frequencies[group] = {"count":0,"allele":{}}
		frequencies[group]["count"] +=1	
		
	for in_file in final_results_dict:
		file_name = in_file
		allele_seen = {}
		internal_stop_seen = {}
		allele_id_seen = {}
		current_group = char_data[file_name]
		for query in final_results_dict[in_file]["contigs"]:
			if query == "species":
				continue
			for allele in final_results_dict[in_file]["contigs"][query]:
				add = False
				if final_results_dict[in_file]["contigs"][query][allele]:
					for hit in final_results_dict[in_file]["contigs"][query][allele]:
						if hit["region_type"] == "CDS":
							add = True
						else:
							add = False
					if add:
						if allele not in internal_stop_seen:
							internal_stop_seen[allele] = False
						if allele not in allele_seen:
							allele_seen[allele] = False
						if allele not in allele_id_seen:
							allele_id_seen[allele] = []
						for hit in final_results_dict[in_file]["contigs"][query][allele]:
							edge = hit["edge"]
							allele_id = hit["allele_id"]
							raw_flags = hit["flags"]
							if edge:
								if allele in frequencies[current_group]["allele"]:
									continue					
							if len(raw_flags) == 1:
								flags = raw_flags[0]
							elif len(raw_flags) > 1:
								flags = ",".join(raw_flags)
							else:
								flags = "N/A"			
							if allele not in frequencies[current_group]["allele"]:
								frequencies[current_group]["allele"][allele] = {"non_func_count":0,"allele_id":{},"pres_count":0}
							if "internal stop" in flags or "phase" in flags:
								if not internal_stop_seen[allele]:
									frequencies[current_group]["allele"][allele]["non_func_count"]+=1
									internal_stop_seen[allele] = True						
							if allele_id not in frequencies[current_group]["allele"][allele]["allele_id"]:
								frequencies[current_group]["allele"][allele]["allele_id"][allele_id] =1
							#else:
							#	frequencies[current_group]["allele"][allele]["allele_id"][allele_id]+=1
							elif allele_id not in allele_id_seen[allele]:	
								frequencies[current_group]["allele"][allele]["allele_id"][allele_id]+=1
								allele_id_seen[allele].append(allele_id)								
						if not allele_seen[allele]:
							frequencies[current_group]["allele"][allele]["pres_count"]+=1
							allele_seen[allele] = True						
	return frequencies

	
	
def compare_alleles(final_results_dict,frequencies):
	final = {}
	allele_info = {}
	for in_file in final_results_dict:
		for query in final_results_dict[in_file]["contigs"]:
			if query == "species":
				continue
			for allele in final_results_dict[in_file]["contigs"][query]:
				if allele not in allele_info:
					allele_info[allele] = {}
				for hit in final_results_dict[in_file]["contigs"][query][allele]:
					allele_id = hit["allele_id"]
					if allele_id not in allele_info[allele]:
						allele_info[allele][allele_id] = {}
					raw_flags = hit["flags"]
					if len(raw_flags) == 1:
						flags = raw_flags[0]
					elif len(raw_flags) > 1:
						flags = ",".join(raw_flags)
					else:
						flags = "N/A"				
					if "annotations" in hit:
						annotations = hit["annotations"]
					else:
						annotations = "None found"
					allele_info[allele]["annotations"] = annotations
					allele_info[allele][allele_id]["flags"] = flags
		
	for group in frequencies:
		member_count = frequencies[group]["count"]
		for allele in frequencies[group]["allele"]:
			if allele not in final:
				final[allele] = {"allele_id":{},"non_functional":{},"pres_abs":{}}
			frequency = float((frequencies[group]["allele"][allele]["non_func_count"])/member_count)
			final[allele]["non_functional"][group] = frequency
			frequency_pres = float((frequencies[group]["allele"][allele]["pres_count"])/member_count)
			final[allele]["pres_abs"][group] = frequency_pres			
			for allele_id in frequencies[group]["allele"][allele]["allele_id"]:
				flags = allele_info[allele][allele_id]["flags"]
				annotation = allele_info[allele]["annotations"]
				frequency_id = float((frequencies[group]["allele"][allele]["allele_id"][allele_id])/member_count)
				if allele_id not in final[allele]["allele_id"]:
					final[allele]["allele_id"][allele_id] = {}	
				final[allele]["allele_id"][allele_id][group] = frequency_id
	out_path = os.path.join(OUTPUT_DIR,"summary")
		
	with open(os.path.join(out_path,"allele_frequencies_{}.tab".format(time.time())),"w") as f:
		f.write("Allele_ID\tFlags\tFunction")
		groups = {}
		i=0
		for group in frequencies:
			groups[i] = group
			f.write("\t{}".format(group))
			i+=1
		f.write("\n")
		for allele in final:
			for allele_id in final[allele]["allele_id"]:
				if allele not in allele_info:
					allele = "'{}".format(allele)
				function = allele_info[allele]["annotations"]
				flags = allele_info[allele][allele_id]["flags"]
				if allele in gene_names:
					allele_name = gene_names[allele]
				else:
					allele_name = allele				
				f.write("{}_{}\t{}\t{}".format(allele_name,allele_id,flags,function))
				for counter in groups:
					group = groups[counter]					
					if group in final[allele]["allele_id"][allele_id]:
						freq = final[allele]["allele_id"][allele_id][group]
						f.write("\t{}".format(str(freq)))
					else:
						freq = 0
						f.write("\t{}".format(str(freq)))
				f.write("\n")
				
	with open(os.path.join(out_path,"non_functional_alleles_frequencies_{}.tab".format(time.time())),"w") as f:
		f.write("Allele\tFlags\tFunction")
		groups = {}
		i=0
		for group in frequencies:
			groups[i] = group
			f.write("\t{}".format(group))
			i+=1
		f.write("\n")
		for allele in final:
			if allele not in allele_info:
				allele = "'{}".format(allele)
			function = allele_info[allele]["annotations"]
			if allele in gene_names:
				allele_name = gene_names[allele]
			else:
				allele_name = allele	
			f.write("{}\t{}\t{}".format(allele_name,"Not_Functional",function))
			for counter in groups:
				group = groups[counter]
				if group in final[allele]["non_functional"]:
					freq = final[allele]["non_functional"][group]
					f.write("\t{}".format(str(freq)))
				else:
					freq = 0
					f.write("\t{}".format(str(freq)))
			f.write("\n")
			
	with open(os.path.join(out_path,"gene_presence_absence_{}.tab".format(time.time())),"w") as f:
		f.write("Allele\tFlags\tFunction")
		groups = {}
		i=0
		for group in frequencies:
			groups[i] = group
			f.write("\t{}".format(group))
			i+=1
		f.write("\n")
		for allele in final:
			if allele not in allele_info:
				allele = "'{}".format(allele)
			function = allele_info[allele]["annotations"]
			if allele in gene_names:
				allele_name = gene_names[allele]
			else:
				allele_name = allele	
			f.write("{}\t{}\t{}".format(allele_name,"N/A",function))	
			for counter in groups:
				group = groups[counter]
				if allele in frequencies[group]["allele"]:
					freq = final[allele]["pres_abs"][group]		
					f.write("\t{}".format(str(freq)))
				else:
					freq = 0
					f.write("\t{}".format(str(freq)))
			f.write("\n")										

def generate_sg_predictions(data):
	out_path = os.path.join(OUTPUT_DIR,"serogroup")
	neisseria_set = {}
	sg_results = {"Serogroup":[],"Serotype":[]}
	hi_set = {}
	for query in sorted(data):
		species = data[query]["species"]
		if species == "neisseria":
			neisseria_set[query] = data[query]
		elif species == "hinfluenzae":
			hi_set[query] = data[query]
			
	## Neisseria SG Prediction
	if neisseria_set:
		with open(os.path.join(out_path,"serogroup_predictions_{}.tab".format(time.time())),"w") as f:
			f.write("Query\tSG\tGenes_Present\tNotes\n")
			for query in sorted(neisseria_set):
				sg_dict = {"sample_name":query,"predicted_sg":"","baseSG":"","genes":[]}				
				found_result = False			
				partial_set = {}
				seen_genes = {}
				for contig in neisseria_set[query]["contigs"]:
					partial_set[contig] = {}
					for allele in sorted(neisseria_set[query]["contigs"][contig]):
						partial_set[contig][allele] = []
						if neisseria_set[query]["contigs"][contig][allele]:
							for hit in neisseria_set[query]["contigs"][contig][allele]:
								allele_name = hit["allele_name"]
								for sg in serogroups:
									if sg not in seen_genes:
										seen_genes[sg] = {"essential":[],"nonessential":[]}
									for gene in serogroups[sg]["essential"]:
										if gene == "cnl":
											if allele_name == gene:
												if hit["cov"] < 1:
													continue
										if allele_name == gene:
											found_result = True
											if hit["cov"] < 1:
												hit["partial"] = True
												partial_set[contig][allele].append(hit)
											else:
												hit["partial"] = False										
											seen_genes[sg]["essential"].append(hit)
									for n_gene in serogroups[sg]["nonessential"]:
										if allele_name == n_gene:	
											seen_genes[sg]["nonessential"].append(hit)	
				to_remove = []
				for contig in partial_set:
					for allele in partial_set[contig]:
						for partial_hit in partial_set[contig][allele]:
							partial_hit_start = int(partial_hit["qstart"])
							partial_hit_stop = int(partial_hit["qend"])
							partial_hit_name = partial_hit["allele_name"]
							for allele in neisseria_set[query]["contigs"][contig]:
								for hit in neisseria_set[query]["contigs"][contig][allele]:
									hit_type = hit["region_type"]
									if hit_type == "ISE":
										hit_start = int(hit["qstart"])
										hit_name = hit["allele_name"]
										hit_id = str(hit["allele_id"])
										hit_stop = int(hit["qend"])
										start_dist = abs(partial_hit_start - hit_stop)
										stop_dist = abs(partial_hit_stop - hit_start)
										if start_dist < 20 or stop_dist < 20:
											for sg in seen_genes:
												for hit in seen_genes[sg]["essential"]:
													if hit["allele_name"] == partial_hit_name:
														if hit != partial_hit:
															pass
														else:
															hit["disrupted"] = hit_name +"_"+hit_id
				
				current_count = 0
				top_sg = None
				matching_num_sg = 0
				unique_sg = False
				multiple_top_hits = False
				#print(query,found_result)
				#pp.pprint(seen_genes)
				current_sg = ""
				first_sg = True
				contamination = False
				first_seen_unique_partial = False
				seen_sgs = []
				current_gene_list = []
				if found_result:
					for sg in seen_genes:
						for hit in seen_genes[sg]["essential"]:
							allele_name = hit["allele_name"]
							partiality = hit["partial"]
							if allele_name not in current_gene_list:
								current_gene_list.append(allele_name)
							if allele_name in SG_unique:
								if first_sg:
									current_sg = SG_unique[allele_name]
									first_sg = False
									if partiality:
										first_seen_unique_partial = True
									seen_sgs.append(current_sg)
								else:
									if SG_unique[allele_name] != current_sg:
										if partiality and first_seen_unique_partial:
											if (current_sg == "Y" and SG_unique[allele_name] == "W") or (SG_unique[allele_name] == "Y" or current_sg == "W"):
												continue
										else:
											if SG_unique[allele_name] not in seen_sgs:
												seen_sgs.append(SG_unique[allele_name])
											contamination = True
											
					if not contamination:
						for sg in seen_genes:
							gene_list = []
							for hit in seen_genes[sg]["essential"]:
								allele_name = hit["allele_name"]
								partiality = hit["partial"]
								if sg == "cnl" or sg == "cnl_1":
									if allele_name == "cnl":
										if partiality:
											continue
								if allele_name not in gene_list:
									gene_list.append(allele_name)
							if len(gene_list) > current_count:
								multiple_top_hits = False
								top_sg = sg
								current_count = len(gene_list)
								current_gene_list = gene_list
								notes = []		
								seen_alleles = []
								final_sg = top_sg
								to_remove = []
								if top_sg == "cnl_1":
									top_sg = "cnl"
								quality_check = {}
						for hit in seen_genes[top_sg]["essential"]:
							allele_name = hit["allele_name"]
							partiality = hit["partial"]
							if allele_name not in quality_check:
								quality_check[allele_name] = {"full_length_match":False,"list":[]}
							if not partiality:
								quality_check[allele_name]["full_length_match"] = True
							quality_check[allele_name]["list"].append(hit)
						for allele in quality_check:
							if len(quality_check[allele]["list"]) > 1:
								full_length_match = quality_check[allele]["full_length_match"]
								if full_length_match:
									for hit in quality_check[allele]["list"]:
										allele_name = hit["allele_name"]
										if hit["partial"]:
											to_remove.append(hit)
						
						for hit in to_remove:
							allele_name = hit["allele_name"] 
							if hit in seen_genes[top_sg]["essential"]:
								seen_genes[top_sg]["essential"].remove(hit)

					
						for hit in seen_genes[top_sg]["essential"]:
							allele_name = hit["allele_name"]
							if "sequence" in hit:
								hit.pop("sequence")
							sg_dict["genes"].append(hit)							
							partiality = hit["partial"]
							flag_list = hit["flags"]				
							if "disrupted" in hit:
								note_to_add = "{} disrupted by {}".format(allele_name,hit["disrupted"])
								if note_to_add not in notes:
									notes.append(note_to_add)
								final_sg = "NG"
							elif partiality:
								#print(allele_name)
								if not hit["new"] or hit["cov"] < .95:
									final_sg = "NG"
									if allele_name != "cnl":
										hit_cov = round(hit["cov"]*100,2)
										notes.append("{} fragmented ({}% cov)".format(allele_name,hit_cov))
							
							if len(flag_list) > 0:
								if top_sg != "cnl":
									flags = ",".join(flag_list)
									if "phase" in flags:
										final_sg = "NG"
										notes.append("phase variable OFF in {}".format(allele_name))				
									elif "internal stop" in flags:
										final_sg = "NG"
										note = "internal stop in {}".format(allele_name)
										if note not in notes:
											notes.append(note)
									
						for gene in current_gene_list:
							if gene in SG_unique:
								unique_sg = True
					else:
						final_sg = "Contaminated"
						serogroups_found = ",".join(seen_sgs)
						#current_gene_list = []
						final_notes = "Found genes for serogroups {}, possible contamination".format(serogroups_found)
				
				if not contamination:		
					if top_sg == None:
						notes = []
						current_gene_list = []
						final_sg = "NG"
						top_sg = None
						final_genes = None
						notes.append("No Capsule Genes Found")
					if unique_sg == False and top_sg != "cnl" and top_sg != None:
						final_sg = "NG"
						top_sg = "Unclear"
						notes.append("Capsule genes present shared across multiple SGs")
					if unique_sg != False:
						for sg_gene in serogroups[top_sg]["essential"]:
							if sg_gene not in current_gene_list:
								notes.append("missing {}".format(sg_gene))
								final_sg = "NG"				
					if top_sg == "cnl":
						final_sg = "NG"
						notes.append("capsule null locus (cnl)")					

					if len(notes) == 0:
						notes.append("All essential capsule genes intact and present")
						
					if top_sg != "cnl" and top_sg != None:
						final_notes = "{} backbone: ".format(top_sg)+",".join(sorted(notes))
					elif top_sg == None:
						final_notes = "No Backbone: "+",".join(sorted(notes))
					else:
						final_notes = ",".join(sorted(notes))
						
				if all([top_sg != "cnl", top_sg != None, top_sg != "Unclear"]):
					inconclusive = True
					for obj in notes:
						if "missing" in obj:
							inconclusive = False
						elif "essential capsule genes" in obj:
							inconclusive = False
					if inconclusive:
						final_sg = "Inconclusive" 
				
				final_genes = ",".join(sorted(current_gene_list))
				result_line = "{}\t{}\t{}\t{}\n".format(query,final_sg,final_genes,final_notes)
				sg_dict["predicted_sg"] = final_sg
				sg_dict["baseSG"] = top_sg
				sg_results["Serogroup"].append(sg_dict)				
				f.write(result_line)

	if hi_set:
		with open(os.path.join(out_path,"serotype_predictions_{}.tab".format(time.time())),"w") as f:
			f.write("Query\tST\tGenes_Present\tNotes\n")
			for query in sorted(hi_set):
				st_dict = {"sample_name":query,"predicted_st":"","baseST":"","genes":[]}					
				found_result = False			
				partial_set = {}
				seen_genes = {}
				for contig in hi_set[query]["contigs"]:
					partial_set[contig] = {}
					for allele in sorted(hi_set[query]["contigs"][contig]):
						partial_set[contig][allele] = []
						if hi_set[query]["contigs"][contig][allele]:
							for hit in hi_set[query]["contigs"][contig][allele]:
								allele_name = hit["allele_name"]
								for st in serotypes:
									if st not in seen_genes:
										seen_genes[st] = {"essential":[],"nonessential":[]}
									for gene in serotypes[st]["essential"]:
										if allele_name == gene:
											found_result = True
											if hit["cov"] < 1 and not hit["edge"]:
												hit["partial"] = True
												partial_set[contig][allele].append(hit)
											else:
												hit["partial"] = False										
											seen_genes[st]["essential"].append(hit)
									for n_gene in serotypes[st]["nonessential"]:
										if allele_name == n_gene:	
											seen_genes[st]["nonessential"].append(hit)	
				to_remove = []
				for contig in partial_set:
					for allele in partial_set[contig]:
						for partial_hit in partial_set[contig][allele]:
							partial_hit_start = int(partial_hit["qstart"])
							partial_hit_stop = int(partial_hit["qend"])
							partial_hit_name = partial_hit["allele_name"]
							for allele in hi_set[query]["contigs"][contig]:
								for hit in hi_set[query]["contigs"][contig][allele]:
									hit_type = hit["region_type"]
									if hit_type == "ISE":
										hit_start = int(hit["qstart"])
										hit_name = hit["allele_name"]
										hit_id = str(hit["allele_id"])
										hit_stop = int(hit["qend"])
										start_dist = abs(partial_hit_start - hit_stop)
										stop_dist = abs(partial_hit_stop - hit_start)
										if start_dist < 20 or stop_dist < 20:
											for sg in seen_genes:
												for hit in seen_genes[sg]["essential"]:
													if hit["allele_name"] == partial_hit_name:
														if hit != partial_hit:
															pass
														else:
															hit["disrupted"] = hit_name +"_"+hit_id
				
				current_count = 0
				top_st = None
				matching_num_sg = 0
				unique_st = False
				current_st = ""
				first_st = True
				contamination = False
				#first_seen_unique_partial = False
				seen_sts = []
				if found_result:
					for sg in seen_genes:
						for hit in seen_genes[sg]["essential"]:
							allele_name = hit["allele_name"]
							partiality = hit["partial"]
							if allele_name in ST_unique:
								if first_st:
									current_st = ST_unique[allele_name]
									first_st = False
									if partiality:
										first_seen_unique_partial = True
									seen_sts.append(current_st)
								else:
									if ST_unique[allele_name] != current_st:
										if ST_unique[allele_name] not in seen_sts:
											seen_sts.append(ST_unique[allele_name])
										contamination = True
				if not contamination:
					if found_result:
						for st in seen_genes:
							gene_list = []
							for hit in seen_genes[st]["essential"]:
								allele_name = hit["allele_name"]
								partiality = hit["partial"]
								if allele_name not in gene_list:
									gene_list.append(allele_name)
							if len(gene_list) > current_count:
								top_st = st
								current_count = len(gene_list)
								current_gene_list = gene_list
								notes = []		
								seen_alleles = []
								final_st = top_st
								to_remove = []
								quality_check = {}
								flag_list = []
						for hit in seen_genes[top_st]["essential"]:
							allele_name = hit["allele_name"]
							partiality = hit["partial"]
							flags = hit["flags"]
							if allele_name not in quality_check:
								quality_check[allele_name] = {"full_length_match":False,"list":[],"flags":True}
							if not partiality:
								quality_check[allele_name]["full_length_match"] = True
							if len(flags) == 0:
								quality_check[allele_name]["flags"] = False
							quality_check[allele_name]["list"].append(hit)
						for allele in quality_check:
							if len(quality_check[allele]["list"]) > 1:
								full_length_match = quality_check[allele]["full_length_match"]
								if full_length_match:
									for hit in quality_check[allele]["list"]:
										allele_name = hit["allele_name"]
										if hit["partial"]:
											to_remove.append(hit)
								flag_hit = quality_check[allele]["flags"]
								if not flag_hit:
									for hit in quality_check[allele]["list"]:
										allele_name = hit["allele_name"]
										if len(hit["flags"]) > 0:
											to_remove.append(hit)
						for hit in to_remove:
							allele_name = hit["allele_name"] 
							if hit in seen_genes[top_st]["essential"]:
								seen_genes[top_st]["essential"].remove(hit)
						
						for hit in seen_genes[top_st]["essential"]:
							allele_name = hit["allele_name"]
							if "sequence" in hit:
								hit.pop("sequence")
							st_dict["genes"].append(hit)
							partiality = hit["partial"]
							flag_list = hit["flags"]
							if "disrupted" in hit:
								note_to_add = "{} disrupted by {}".format(allele_name,hit["disrupted"])
								if note_to_add not in notes:
									notes.append(note_to_add)
								final_st = "NT"
							elif partiality:
								if not hit["new"] or hit["cov"] < 0.95:
									final_st = "NT"
									hit_cov = round(hit["cov"]*100,2)
									notes.append("{} fragmented ({}% cov)".format(allele_name,hit_cov))
							
							if len(flag_list) > 0:
								flags = ",".join(flag_list)
								if "phase" in flags:
									final_st = "NT"
									notes.append("phase variable OFF in {}".format(allele_name))				
								elif "internal stop" in flags:
									final_st = "NT"
									notes.append("internal stop in {}".format(allele_name))
									
						for gene in current_gene_list:
							if gene in ST_unique:
								unique_st = True
				else:
					final_st = "Contaminated"
					serotypes_found = ",".join(seen_sts)
					current_gene_list = []
					final_notes = "Found genes for serotypes {}, possible contamination".format(serotypes_found)
				if not contamination:
					if top_st == None:
						notes = []
						current_gene_list = []
						final_st = "NT"
						top_st = None
						final_genes = None
						notes.append("No Capsule Genes Found")

					if unique_st == False and current_gene_list:
						final_st = "NT"
						top_st = "Unclear"
						notes.append("Capsule genes present shared across multiple STs")
					if unique_st != False:
						for st_gene in serotypes[top_st]["essential"]:
							if st_gene not in current_gene_list:
								notes.append("missing {}".format(st_gene))
								final_st = "NT"				
						
					if len(notes) == 0:
						notes.append("All essential capsule genes intact and present")
						
					if top_st != None:
						final_notes = "{} backbone: ".format(top_st)+",".join(sorted(notes))
					elif top_st == None:
						final_notes = "No Backbone: "+",".join(sorted(notes))
					else:
						final_notes = ",".join(sorted(notes))
				final_genes = ",".join(sorted(current_gene_list))
				result_line = "{}\t{}\t{}\t{}\n".format(query,final_st,final_genes,final_notes)
				st_dict["predicted_st"] = final_st
				st_dict["baseST"] = final_st
				sg_results["Serotype"].append(st_dict)
				f.write(result_line)
	with open(os.path.join(OUTPUT_DIR,"serogroup","serogroup_results.json"),"w") as f:
		json.dump(sg_results,f)
		
## in development ##
def find_promoters(final_dict,seq_dict):
	promoter_dict = {}
	for query in final_dict:
		promoter_dict[query] = {}
		for contig in final_dict[query]["contigs"]:
			if contig == "species":
				continue				
			promoter_dict[query][contig] = {}
			contig_elements = {}
			sequence = seq_dict[query]["contigs"][contig]["seq"]
			for feature in final_dict[query]["contigs"][contig]:
				if final_dict[query]["contigs"][contig][feature]:
					for allele in final_dict[query]["contigs"][contig][feature]:
						region_type = allele["region_type"]
						allele_name = allele["allele_name"]
						allele_id= allele["allele_id"]
						start_pos = int(allele["qstart"])
						strand = allele["strand"]
						stop_pos = int(allele["qend"])
						allele_identifier = allele_name+"*"+allele_id
						if region_type == "CDS" or region_type == "ISE":
							contig_elements[start_pos] = {"name":allele_identifier,"stop":stop_pos,"strand":strand}
			current_start = 0
			interval = 100
			first = True
			for start_pos in sorted(contig_elements.keys()):
				stop_pos = contig_elements[start_pos]["stop"]
				contig_end = len(sequence)				
				strand = contig_elements[start_pos]["strand"]
				allele_identifier = contig_elements[start_pos]["name"]
				if first:
					if strand == "+":
						if (start_pos-current_start) >= interval:
							igr_region = sequence[current_start:start_pos]
							promoter_dict[query][contig][allele_identifier] = str(igr_region)
							current_start = start_pos
							current_stop = stop_pos
							current_strand = strand
							current_allele = allele_identifier
							first = False
							continue
						else:
							current_start = start_pos
							current_stop = stop_pos
							current_strand = strand
							first = False
							continue						
					else:
							current_start = start_pos
							current_stop = stop_pos
							current_strand = strand							
							current_allele = allele_identifier							
							first = False
							continue
				if strand == "+":
					if (start_pos-current_stop) >= interval:
						igr_region = sequence[current_stop:start_pos]
						promoter_dict[query][contig][allele_identifier] = str(igr_region.reverse_complement())						
						current_start = start_pos
						current_stop = stop_pos
						current_strand = strand						
						current_allele = allele_identifier
					else:
						current_start = start_pos
						current_stop = stop_pos
						current_strand = strand						
						current_allele = allele_identifier										
				else:
					if (start_pos-current_stop) >= interval:
						if strand == current_strand:
							igr_region = sequence[current_stop:start_pos]
							promoter_dict[query][contig][allele_identifier] = str(igr_region.complement())						
							current_start = start_pos
							current_stop = stop_pos	
							current_strand = strand
							current_allele = allele_identifier
						else:
							igr_region = sequence[current_stop:start_pos]
							promoter_dict[query][contig][allele_identifier] = str(igr_region.complement())						
							current_start = start_pos
							current_stop = stop_pos	
							current_strand = strand
							current_allele = allele_identifier	
					else:
						current_start = start_pos
						current_stop = stop_pos	
						current_strand = strand
						current_allele = allele_identifier							
												
	for query in promoter_dict:
		with open(os.path.join(OUTPUT_DIR,"igr","{}_igr.fasta".format(query)),"w") as f:
			for contig in promoter_dict[query]:
				if contig == "species":
					continue					
				for allele_name in promoter_dict[query][contig]:
					if "Insertion_Element" in allele_name:
						continue
					allele_rename = allele_name.replace("*","_")
					f.write(">{}\n".format(allele_rename))
					f.write("{}\n".format(promoter_dict[query][contig][allele_name]))

def output_fastas(final_results_dict):
	for query in final_results_dict:
		type_dict = {}
		edited_query = query
		if not os.path.isdir(os.path.join(OUTPUT_DIR,"feature_fastas",edited_query)):
			os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"feature_fastas",edited_query)))	
					
		for contig in final_results_dict[query]["contigs"]:
			if contig == "species":
				continue				
			for allele in final_results_dict[query]["contigs"][contig]:
				for hit in final_results_dict[query]["contigs"][contig][allele]:
					region_type = hit["region_type"]
					if region_type not in type_dict:
						type_dict[region_type] = {}
					allele_name = hit["allele_name"]
					allele_id = hit["allele_id"]
					sequence = hit["qseq"]
					allele_identifier = allele_name+"_"+allele_id
					if allele_identifier not in type_dict[region_type]:
						type_dict[region_type][allele_identifier] = sequence
						
	#pp.pprint(type_dict)									
		for region_type in type_dict:
			with open(os.path.join(OUTPUT_DIR,"feature_fastas",edited_query,"{}.fasta".format(region_type)),"w") as f:
				for allele in type_dict[region_type]:
					f.write(">{}\n".format(allele))
					f.write("{}\n".format(type_dict[region_type][allele]))
						
#BMScan code - skips if BMScan Json provided										
def obtain_species(input_dir,threads):
	final_sp_dict = {}
	temp_dir = tempfile.mkdtemp()
	sketch_info={}
	thresholds = {}	
	c_2.execute("select g.filepath,o.threshold,o.species,o.genus,s.source_location from Genome g, Organism o, Source s where g.organism_id=o.organism_id and s.source_id=g.source_id")
	org_results = c_2.fetchall()
	for org_id in org_results:
		file_path = org_id[0]
		threshold = org_id[1]
		species = org_id[2]
		genus = org_id[3]
		source = org_id[4]
		if file_path not in thresholds:
			thresholds[file_path] = {"threshold":threshold,"species":species,"genus":genus,"source":source}
	
	def mash_sketch(threads,input_dir,temp_dir,sketch_info):
		kmer_size = 21
		sketch_size = 1000
		sketch_info_dict = {}
		call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"sp_sketch"),os.path.join(input_dir,"*.fasta"))],shell=True,stderr=DEVNULL)
		sketch_info_dict["path"] = temp_dir+"/sp_sketch.msh"
		sketch_info={"sketch_dict":sketch_info_dict,"temp_dir":temp_dir}
		return sketch_info
		
	def mash_dist(sketch,mash_db_name,threads,refseq,thresholds):
		mash_results_dict = {}
		mash_results = check_output(["mash","dist","-p",threads,mash_db_name,sketch],shell=False)
		mash_result = re.split(b"\n",mash_results.rstrip())				
		for line in mash_result:
			if refseq:
				hit = line.decode(encoding).split("\t")[0].split("-")[-1].split(".fna")[0]
				try:
					mash_hit_list = hit.split("_")
					if len(mash_hit_list) > 1:
						hit = mash_hit_list[0] + " " + mash_hit_list[1]
					else:
						hit = mash_hit_list[0]
				except:
					pass		
			else:
				hit = line.decode(encoding).split("\t")[0]
			query_name = line.decode(encoding).split("\t")[1]
			query_name = os.path.basename(query_name)
			if not query_name in mash_results_dict:
				mash_results_dict[query_name] = {"mash_results":{}}
			mash_dist = float(line.decode(encoding).split("\t")[2])
			p_val = line.decode(encoding).split("\t")[3]
			match_hash = line.decode(encoding).split("\t")[4]
			mash_score = (1-mash_dist)
			mash_results_dict[query_name]["mash_results"][hit] = {"score":mash_score,"p_val":p_val,"hash":match_hash,"hit":hit}
		for query in mash_results_dict:
			over_threshold = {}
			mash_results_dict[query]["mash_results"]["Above_Threshold"] = {}		
			current_mash_hit = "N/A"
			current_mash_score = 0
			for hit in mash_results_dict[query]["mash_results"]:
				if hit != "Above_Threshold":
					if not refseq:
						score = mash_results_dict[query]["mash_results"][hit]["score"]	
						threshold = thresholds[hit]["threshold"]										
						if score >= threshold:				
							species = thresholds[hit]["species"]
							p_val = mash_results_dict[query]["mash_results"][hit]["p_val"]
							hash_val = mash_results_dict[query]["mash_results"][hit]["hash"]
							hit_name = mash_results_dict[query]["mash_results"][hit]["hit"]
							source = thresholds[hit]["source"]							
							genus = thresholds[hit]["genus"]
							species = species.lower()
							organism = string.capwords(genus)+" "+species
							if organism not in over_threshold:
								over_threshold[organism] = {"score":score,"p_val":p_val,"hash":hash_val,"hit":hit_name,"source":source}
							else:
								current_score = over_threshold[organism]["score"]
								if score > current_score:
									over_threshold[organism] = {"score":score,"p_val":p_val,"hash":hash_val,"hit":hit_name,"source":source}		
						
					else:
						if mash_results_dict[query]["mash_results"][hit]["score"] > current_mash_score:
							current_mash_score = mash_results_dict[query]["mash_results"][hit]["score"]
							current_mash_hit = hit
			
			if refseq:
				mash_results_dict[query]["mash_results"]["Top Match"] = current_mash_hit
			else:
				mash_results_dict[query]["mash_results"]["Above_Threshold"] = over_threshold
				
		return mash_results_dict
		
	def parse_results(results,input_file,thresholds):
		redo = {}
		for lab_id in results:
			path = os.path.join(input_file,lab_id)
			over_threshold = results[lab_id]["mash_results"]["Above_Threshold"]
			if not over_threshold:
				#print(lab_id,"has no scores over thresholds")
				redo[lab_id] = path
				continue
		return redo		

	def mash_sketch_refseq(threads,redo,temp_dir):
		#print("Scanning low-scoring queries against RefSeq")
		for lab_id in redo:
			file_path = redo[lab_id] 
			call(["cp","{}".format(file_path),"{}/".format(temp_dir)],shell=False)
		threads = threads
		kmer_size = 21
		sketch_size = 1000
		sketch_info_dict = {}
		call(["mash sketch -k {} -p {} -s {} -o {} {}".format(kmer_size,threads,sketch_size,os.path.join(temp_dir,"sp_ref_sketch"),os.path.join(temp_dir,"*.fasta"))], shell=True,stderr=DEVNULL)
		sketch_info_dict["path"] = temp_dir+"/sp_ref_sketch.msh"	
		return sketch_info_dict
		
	def create_json(data,thresholds):
		pre_json = data
		for lab_id in data:
			if lab_id not in pre_json:
				pre_json[lab_id] = {"mash_results":{}}
			over_threshold = data[lab_id]["mash_results"]["Above_Threshold"]
			if not over_threshold:
				notes = "No_hit_above_threshold_from_reference_collection_Reporting_top_refseq_hit"			
				mash_hit = data[lab_id]["mash_results"]["Top Match"]
				if mash_hit != "N/A":
					mash_pval = data[lab_id]["mash_results"][mash_hit]["p_val"]
					mash_hash = data[lab_id]["mash_results"][mash_hit]["hash"]
					mash_score = data[lab_id]["mash_results"][mash_hit]["score"]
					mash_species = mash_hit
				else:
					mash_pval = "N/A"
					mash_hash = "N/A"
					mash_score = "N/A"
					mash_species = "N/A"
				mash_source = "ncbi_refseq"
			else:
				if len(over_threshold) == 1:
					notes = "Hit_above_threshold"				
					for organism in over_threshold:
						mash_species = organism
						mash_hit = over_threshold[organism]["hit"]
						mash_pval = over_threshold[organism]["p_val"]
						mash_hash = over_threshold[organism]["hash"]
						mash_score = over_threshold[organism]["score"]
						mash_source = over_threshold[organism]["source"]							
				elif len(over_threshold) > 1:	
					notes = "multiple_species_above_threshold"				
					current_highest_score = 0.0
					i=1
					for organism in over_threshold:
						notes+= "{}_{}_with_score_{}%_to_hit_{}".format(str(i),organism, str(over_threshold[organism]["score"]),str(over_threshold[organism]["hit"]))
						i+=1
						if over_threshold[organism]["score"] > current_highest_score:
							mash_species = organism
							current_highest_score = over_threshold[organism]["score"]
							mash_score = current_highest_score	
					mash_pval =  over_threshold[mash_species]["p_val"]
					mash_hit =  over_threshold[mash_species]["hit"]
					mash_hash =  over_threshold[mash_species]["hash"]
					mash_source =  over_threshold[mash_species]["source"]
			mash_species_list = mash_species.split(" ")
			if len(mash_species_list) > 1:
				mash_sp = mash_species_list[1].lower()
				mash_species = string.capwords(mash_species_list[0]) + " " + mash_sp
			else:
				mash_species = string.capwords(mash_species_list[0])			

			pre_json[lab_id]["mash_results"] = {"species":mash_species,"top_hit":mash_hit,"mash_pval":mash_pval,"mash_hash":mash_hash,"score":mash_score,"source":mash_source,"notes":notes}
		return pre_json
	
	sketch_creation = mash_sketch(threads,input_dir,temp_dir,sketch_info)
	sketch_path= sketch_creation["sketch_dict"]	
		
	mash_results = mash_dist(sketch_path["path"],MASH_DB,threads,False,thresholds)
	redo_set = parse_results(mash_results,input_dir,thresholds)		
	if redo_set:
		redo_sketch = mash_sketch_refseq(threads,redo_set,temp_dir)
		redo_results = mash_dist(redo_sketch["path"],REFSEQ_DB,threads,True,thresholds)
		for query in redo_results:
			mash_results[query]["mash_results"] = redo_results[query]["mash_results"]
			
	final_results = create_json(mash_results,thresholds)
	for fasta_file in final_results:
		species = final_results[fasta_file]["mash_results"]["species"]
		final_results[fasta_file] = species
	return final_results
	
def count_loci_per_scheme(scheme_data,results_dict):
	out_path = OUTPUT_DIR
	scheme_counter = {}
	schemes_seen = []
	loci_counts = {}
	i=0
	for scheme in scheme_data:
		if scheme not in schemes_seen:
			schemes_seen.append(scheme)
			scheme_counter[i] = scheme
			i+=1
	for in_file in results_dict:
		if in_file not in loci_counts:
			loci_counts[in_file] = {}
		for contig in results_dict[in_file]["contigs"]:
			for allele in results_dict[in_file]["contigs"][contig]:
				if results_dict[in_file]["contigs"][contig][allele]:
					for hit in results_dict[in_file]["contigs"][contig][allele]:
						if hit["cov"] >= .90:
							for scheme in scheme_data:
								if scheme not in loci_counts[in_file]:
									loci_counts[in_file][scheme] = []
								if allele in scheme_data[scheme]:
									if allele not in loci_counts[in_file][scheme]:
										loci_counts[in_file][scheme].append(allele)
	max_length = len(scheme_counter)
	with open(os.path.join(out_path,"loci_counts.tab"),"w") as f:
		f.write("Lab_ID\t")
		for i in range(0,max_length):
			f.write("{}_{}\t".format(scheme_counter[i].replace(" ","_"),len(scheme_data[scheme_counter[i]])))
		f.write("\n")
		for in_file in loci_counts:
			f.write("{}\t".format(in_file))
			for i in range(0,max_length):
				if scheme_counter[i] in loci_counts[in_file]:
					f.write("{}\t".format(len(loci_counts[in_file][scheme_counter[i]])))
				else:
					f.write("0\t")
			f.write("\n")
			
def create_allele_matrix(results_dict):
	genes_seen = []
	genes_counter = {}
	allele_matrix = {}
	new_alleles = {}
	i=0
	q=1
	out_path = OUTPUT_DIR
	for in_file in results_dict:
		if in_file not in allele_matrix:
			allele_matrix[in_file] = {}
		for contig in results_dict[in_file]["contigs"]:
			for allele in results_dict[in_file]["contigs"][contig]:
				if results_dict[in_file]["contigs"][contig][allele]:		
					for hit in results_dict[in_file]["contigs"][contig][allele]:
						region_type = hit["region_type"]
						if region_type == "CDS":
							allele_name = hit["allele_name"]
							cov = hit["cov"]
							allele_id = hit["allele_id"]
							seq = hit["qseq"]
							if cov == 1:
								if allele_name not in genes_seen:
									genes_seen.append(allele_name)
									genes_counter[i] = allele_name
									i+=1
								if "new" in allele_id:
									if seq not in new_alleles:
										new_alleles[seq] = "temp_{}".format(q)
										q+=1
										allele_id = new_alleles[seq]
									else:
										allele_id = new_alleles[seq]
								if allele_name not in allele_matrix[in_file]:
									allele_matrix[in_file][allele_name] = allele_id
	max_length = len(genes_counter)
	with open(os.path.join(out_path,"allele_matrix.tab"),"w") as f:
		f.write("Lab_ID\t")
		for i in range(0,max_length):
			f.write("{}\t".format(genes_counter[i]))
		f.write("\n")
		for in_file in allele_matrix:
			f.write("{}\t".format(in_file))
			for i in range(0,max_length):
				if genes_counter[i] in allele_matrix[in_file]:
					allele_id = allele_matrix[in_file][genes_counter[i]]
				else:
					allele_id = 0
				f.write("{}\t".format(allele_id))
			f.write("\n")
	
def main():	
	parser = argparse.ArgumentParser(description="Script for annotating genomes using PubMLST allele set")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-d','--indir',help="Input Dir")	
	group.add_argument('-x','--xlsx',help="Excel file with Filename column and optional Species column ({})".format(', '.join([k for k in species_dict.keys()]))) #TODO: use species_dict.values
	parser.add_argument('-b','--blastdir',help="Directory containing blast DBs, default to pubmlst_dbs_all")
	parser.add_argument('-c','--char',help="Characterizations File")
	parser.add_argument('-sg','--serogroup',help="Produce SG prediction file",action="store_true")
	parser.add_argument('-pr','--promoters',help="Identify Promoters (Experimental, use at own risk)",action="store_true")
	parser.add_argument('-is','--internalstop',help="Output internal stop locations in capsule genes",action="store_true")
	parser.add_argument('-fa','--fastas',help="Output identified gene sequences as FASTAs",action="store_true")
	parser.add_argument('-fr','--force',help="Force overwrite existing output file",action="store_true")
	parser.add_argument('-p','--pubmlst',help="Use pubmlst rest API instead of local API",action="store_true")
	parser.add_argument('-o','--out',help="Output Directory", required=True)
	parser.add_argument('-j','--jdebug',help="Skip step 1 by providing existing JSON folder with raw blast results")
	parser.add_argument('-jf','--fdebug',help="Skip step 2 by providing existing JSON folder with final results")
	parser.add_argument('-s','--species',help="BMScan Json input to skip running BMScan again")
	parser.add_argument('-sc','--scheme',help="Produce tab-delimited count of loci identified for each gene across all tested genomes",action="store_true")
	parser.add_argument('-a','--allele_matrix',help="Produce tab-delimited matrix containing all alleles identified per tested genome",action="store_true")
	parser.add_argument('-t','--threads',help="Number of Threads to use (default=1)",default="1")
	args = vars(parser.parse_args())
	### Print Args ###
	print ("PubMLST Genome Annotator")
	print("Version {}".format(VERSION))
	print("#######################################################################################################")
	print ("Running with the following parameters:")
	for arg in args:
		print (arg,":",args[arg])
	##################

	### Get working directory, setup temp folder, set output ###
	if args["pubmlst"]:
		global _pubmlst_server
		_pubmlst_server = "rest.pubmlst.org"
	char_data = {}
	temp_dir = tempfile.mkdtemp()
	set_output(args["out"])
	if not args["blastdir"]:
		main_blast_dir = PUBMLST_DB
	else:
		main_blast_dir = args["blastdir"]
	### Characterizations file not implemented yet ###
	if args["char"]:
		with open(args["char"]) as f:
			char_text = f.readlines()
			for line in char_text:
				name = line.split('\t')[0].replace("\n","")
				trait = line.split('\t')[1].replace("\n","")
				char_data[name] = trait
	if args["internalstop"]:
		internal_stop = True
	else:
		internal_stop = False
	##Get files and species for each: by default, the key for each is the filename with no directory and no extension
	if isinstance(args["indir"],str):
		working_dir = args["indir"]
		if not args["species"]:
			species_info = obtain_species(working_dir,args["threads"])
			new_species_dict = {}
			for lab_id in species_info:
				new_lab_id = lab_id.replace(".fasta","").replace(".fna","")
				new_species_dict[new_lab_id] = species_info[lab_id]
			species_info = new_species_dict
		else:
			species_info = {}
			with open(args["species"]) as f:
				temp_species_dict = json.load(f)
			for assembly_file in temp_species_dict:
				assembly_file = assembly_file.replace(".fasta","").replace(".fna","")
				species = temp_species_dict[assembly_file]["mash_results"]["species"]
				species_info[assembly_file] = species
		file_dict = {x.replace(".fasta","").replace(".fna",""):x for x in os.listdir(working_dir) if os.path.splitext(x)[1] in ['.fasta', '.fna']}
	elif isinstance(args["xlsx"],str):
		file_frame = pd.read_excel(args['xlsx'])
		if 'Filename' not in file_frame:
			raise ValueError("Excel frame must have Filename column")
		if "Species" not in file_frame:
			raise ValueError("Excel files must have Species column -- for now")
		if "Lab_ID" not in file_frame:
			file_frame["Lab_ID"] = file_frame.Filename.apply(os.path.basename).str.replace(".fasta","").str.replace(".fna","")
		good_files = file_frame.Filename.apply(os.path.isfile)
		good_species = file_frame.Species.isin([x for x in species_dict])
		good_records = good_files & good_species
		if sum(good_records) == 0:
			print("Excel file did not have proper filenames and species names. Aborting")
			print("\t{} valid filenames".format(sum(good_files)))
			print("\t{} valid species names".format(sum(good_species)))
			sys.exit()
		elif sum(good_records) < len(file_frame):
			print("Warning: Not every record has valid filename and species. Proceeding with {}/{}".format(sum(good_records),len(file_frame)))
		##TODO: check that Lab_ID are unique
		file_dict = file_frame.set_index("Lab_ID").Filename.to_dict()
		#species_lookup = file_frame[good_records].set_index("Filename")
		species_info = file_frame.set_index("Lab_ID").Species.to_dict() 
		working_dir = None
		
		
	### Get pubMLST schemes and store in scheme_data dict ###	
	scheme_data = get_schemes()	
	print("#######################################################################################################")	
	print("Step 1. BLASTing against PubMLST DBs")
	### Setup results variables ### 
	results_dict = {}
	#final_results_dict = {}
	seq_dict = OrderedDict()
		
	### Enable Backwards Compatability ###
	if os.path.isdir(os.path.join(OUTPUT_DIR,"json")):
		for existing_json in os.listdir(os.path.join(OUTPUT_DIR,"json")):
			existing_json_path = os.path.join(OUTPUT_DIR, "json", existing_json)
			if ".fasta" in existing_json:
				new_name = existing_json.replace(".fasta","")
				new_name_path = os.path.join(OUTPUT_DIR,"json",new_name)
				os.rename(existing_json_path,new_name_path)

	#for existing_json in		 
	existing_results = []
	calculated_results = []
	if not os.path.isdir(os.path.join(OUTPUT_DIR,"json")):
		os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"json")))
	else:
		if not args["force"]:
			if not args["jdebug"] and not args["fdebug"]:
				for existing_json in os.listdir(os.path.join(OUTPUT_DIR,"json")):				
					if "raw" in existing_json:
						existing_json = existing_json.split("_raw")[0]
						existing_results.append(existing_json)
	for in_file, file_name in file_dict.items():
		if isinstance(working_dir,str):
			file_dir = working_dir #filename is basename of files within this directory
		else:
			file_dir = os.path.dirname(file_name) #filename is full file path
			file_name = os.path.basename(file_name)		
		seq_dict[in_file] = {"species":"","contigs":{},"file_name":file_name}			
		species = species_info[in_file]
		if "Neisseria" in species:
			species = "neisseria"
		## If DB doesn't exist for species identified, treat as neisseria
		if species in species_dict:
			blast_species = species_dict[species]
		else:
			print("Unknown species ({}). Using neisseria database".format(species))
			#species = "neisseria"
			blast_species = species_dict["neisseria"]				
		blast_dir = os.path.join(main_blast_dir,blast_species)	 
		with open(os.path.join(file_dir,file_name),"rU") as f:							
			for seq_record in SeqIO.parse(f,"fasta"):
				seq_id = seq_record.id					
				if seq_id not in seq_dict[in_file]["contigs"]:
					seq_dict[in_file]["contigs"][seq_id] = {}
				seq = seq_record.seq
				length = len(seq)
				seq_dict[in_file]["contigs"][seq_id]["seq"] = seq
				seq_dict[in_file]["contigs"][seq_id]["file_name"] = in_file
				seq_dict[in_file]["contigs"][seq_id]["length"] = length
				#seq_dict[in_file]["species"] = blast_species
				seq_dict[in_file]["species"] = species
				seq_dict[in_file]["contigs"][seq_id]["alleles"] = {}
		if not args["jdebug"] and not args["fdebug"]:
			if in_file in existing_results:
				print("Found existing BLAST results for {}, using those results (use -fr flag to force overwriting of results)".format(in_file))
			elif in_file in calculated_results:
				print("Found BLAST results with same file basename. The basename must change to run in same batch: {}".format(in_file)) #I don't expect to encounter this error, so I'm not providing any easy fix -ACR
			else:
				final_dict = run_blast(file_dir,file_name,args["threads"],blast_dir,seq_dict,in_file)
				with open(os.path.join(OUTPUT_DIR,"json","{}_raw_results.json".format(in_file)),"w") as f:
					json.dump(final_dict,f)									
	
	raw_json_files = [x for x in os.listdir(os.path.join(OUTPUT_DIR,"json")) if "raw" in x]
	print("Evaluating {} raw json files".format(len(raw_json_files)))
	for raw_json_file in raw_json_files:
		if "raw" in raw_json_file:
			in_file_path = os.path.join(OUTPUT_DIR,"json",raw_json_file)
			with open(in_file_path) as f:
				temp_dict = json.load(f)
				replace = False
				for query in temp_dict:
					if "contigs" not in temp_dict[query]:
						temp_species = ""	
						replace = True					
						for contig in temp_dict[query]:
							for allele in temp_dict[query][contig]:
								if "NEIS" in allele:
									temp_species = "neisseria"
									break
								elif "HAEM" in allele:
									temp_species = "hinfluenzae"
									break
						contig_data = temp_dict[query]
						temp_dict[query] = {"contigs":contig_data,"species":temp_species}
					if ".fasta" in query or ".fna" in query:
						temp_dict[query]["file_name"] = query						
						old_query = query
						query = query.replace(".fasta","").replace(".fna","")
						temp_dict[query] = temp_dict.pop(old_query)
				results_dict.update(temp_dict)
			if replace:
				with open(in_file_path,"w") as f:
					json.dump(temp_dict,f)				
	### Analyze results in results dict ###	
	
	print("#######################################################################################################")	
	print("Step 2. Parsing BLAST results")
	if args["jdebug"]:
		for in_file in os.listdir(args["jdebug"]):
			if "raw" in in_file:
				if ".fasta" in raw_json_file:
					raw_json_file = raw_json_file.replace(".fasta","")				
				in_file_path = os.path.join(args["jdebug"],in_file)
				with open(in_file_path) as f:
					temp_dict = json.load(f)
					replace = False
					for query in temp_dict:
						if "contigs" not in temp_dict[query]:
							temp_species = ""		
							replace = True				
							for contig in temp_dict[query]:
								for allele in temp_dict[query][contig]:
									if "NEIS" in allele:
										temp_species = "neisseria"
										break
									elif "HAEM" in allele:
										temp_species = "hinfluenzae"
										break
							contig_data = temp_dict[query]
							temp_dict[query] = {"contigs":contig_data,"species":temp_species}	
						if ".fasta" in query or ".fna" in query:
							temp_dict[query]["file_name"] = query							
							old_query = query
							query = query.replace(".fasta","").replace(".fna","")
							temp_dict[query] = temp_dict.pop(old_query)																			
					results_dict.update(temp_dict)	
				if replace:
					with open(in_file_path,"w") as f:
						json.dump(temp_dict,f)							
	final_results_dict={}
	if args["fdebug"]:
		for in_file in os.listdir(args["fdebug"]):
			if "final" in in_file:
				if ".fasta" in in_file:
					in_file = in_file.replace(".fasta","")				
				in_file_path = os.path.join(args["fdebug"],in_file)
				with open(in_file_path) as f:
					temp_dict = json.load(f)
					replace = False
					for query in temp_dict:
						if "contigs" not in temp_dict[query]:
							temp_species = ""	
							replace = True					
							for contig in temp_dict[query]:
								for allele in temp_dict[query][contig]:
									if "NEIS" in allele:
										temp_species = "neisseria"
										break
									elif "HAEM" in allele:
										temp_species = "hinfluenzae"
										break
							contig_data = temp_dict[query]
							temp_dict[query] = {"contigs":contig_data,"species":temp_species}	
						if ".fasta" in query or ".fna" in query:
							temp_dict[query]["file_name"] = query
							old_query = query
							query = query.replace(".fasta","").replace(".fna","")
							temp_dict[query] = temp_dict.pop(old_query)										
					final_results_dict.update(temp_dict)
				if replace:
					with open(in_file_path,"w") as f:
						json.dump(temp_dict,f)					
	else:
		final_results_dict,internal_stop_dict = analyze_results(results_dict,args["threads"],internal_stop)
		if internal_stop:
			with open(os.path.join(OUTPUT_DIR,"internal_stops.tab"),"w") as f:
				f.write("ID\tGene\tLength\tInternal_stops\n")
				for in_file in internal_stop_dict:
					for gene in internal_stop_dict[in_file]:
						length = str(internal_stop_dict[in_file][gene]["length"])
						stops = ",".join(internal_stop_dict[in_file][gene]["stops"])
						f.write("{}\t{}\t{}\t{}\n".format(in_file,gene,length,stops))
	print("#######################################################################################################")
	print("Step 3. Running analyses")		
	for in_file in final_results_dict:
		with open(os.path.join(OUTPUT_DIR,"json","{}_final_results.json".format(in_file.replace(".fasta","").replace(".fna",""))),"w") as f:		
			temp_dict = {}
			temp_dict[in_file] = final_results_dict[in_file]			
			json.dump(temp_dict,f)			
	### Prepare json and gff directories if they do not exist ###

	if not os.path.isdir(os.path.join(OUTPUT_DIR,"gff")):
		os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"gff")))

	if args["char"]:
		if not os.path.isdir(os.path.join(OUTPUT_DIR,"summary")):
			os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"summary")))
		frequencies = calc_frequencies(final_results_dict,char_data)
		compare_alleles(final_results_dict,frequencies)
	if args["serogroup"]:
		if not os.path.isdir(os.path.join(OUTPUT_DIR,"serogroup")):
			os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"serogroup")))		
		generate_sg_predictions(final_results_dict)
	if args["promoters"]:
		if not os.path.isdir(os.path.join(OUTPUT_DIR,"igr")):
			os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"igr")))		
		find_promoters(final_results_dict,seq_dict)
	if args["fastas"]:
		if not os.path.isdir(os.path.join(OUTPUT_DIR,"feature_fastas")):
			os.system("mkdir {}".format(os.path.join(OUTPUT_DIR,"feature_fastas")))		
		output_fastas(final_results_dict)
				
	### Create gff and JSON ###
	print("Creating GFF for pubMLST results")
	create_gff(final_results_dict,scheme_data,seq_dict)
	
	if args["scheme"]:
		count_loci_per_scheme(scheme_data,final_results_dict)
	
	if args["allele_matrix"]:
		create_allele_matrix(final_results_dict)



if __name__ == "__main__":
	main()

