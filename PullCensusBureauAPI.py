import csv
import urllib
import json
import sys, operator
from operator import sub
import re


# Asking to enter year
year = raw_input('Enter Year:')

# Asking to enter geography (ex. county, census tract, zip code)
geog = raw_input('Enter Geography:')

# Asking to enter table type (ex. b, s, dp)
types = raw_input('Enter Table Type:')


# File to write
csvwriter = csv.writer(open(r'C:\FOLDER_NAME\Data_' + geog +'_'+ types +'_'+ year +'.csv', 'w+b'))


# Headers based on the table type
if types == 'b':
    headerB = ['GEOG', 'POP', 'MDNAGEPOP', 'AVEHHSIZE', 'AVEOWOCCHH',
               'AVERNTOCHH', 'TOTVACUNIT', 'MDNHOUSEYR']
    csvwriter.writerow(headerB)

if types == 's':
    headerS = ['GEOG', 'POP60UP', 'POP65UP']
    csvwriter.writerow(headerS)

if types == 'dp':
    headerDP = ['GEOG', 'HHNUMBER', 'FAMHHNMBER', 'NFAMHHNMBR', 'OWOCCUNIT',
               'RNTOCCUNIT', 'OWOCCPCNT', 'RNTOCCPCNT', 'MDNHHINCOM', 'AVGHHINCOM',
               'PCTHHEARN', 'AVEINHHEAR', 'PCTHHCPAI', 'PCTHHSNAP', 'MDINWOREAR',
               'MDINFTMEAR', 'MDINFTFEAR', 'PCTFAMLPOV', 'PCTPPLLPOV', 'PCTP65LPOV',
               'POP16UP', 'LBRFRC', 'LBRFRCRATE', 'LBFCUNEMPL', 'UNEMPLRATE',
               'TOTUNITS', 'VACRATE', 'MDNHMVALUE', 'OWOCCUMRTG', 'PCTOWOCCMG',
               'SMOCAPIWMG', 'SMOCAPINMG', 'GRAPI', 'OWOCMG3034', 'OWOCMG35UP',
               'OWOCNMG3034', 'OWOCNMG35UP', 'RNTPAY3034', 'RNTPAY35UP']
    csvwriter.writerow(headerDP)

    
# Empty lists
raw_data = []
data_final = []
 

# Function to pull the data using census bureau API 
def censusAPI(y,c,g): #y:year, b:profile/subject, c:variable, d:geog
    y = year
    t = types 
    g = geog

# All geographies besides US and State
# If it is detailed table
    if t == 'b':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5?get='+ c +'&for='+ g +':*&in=state:17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is subject table 
    if t == 's':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/subject?get='+ c +'&for='+ g +':*&in=state:17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is profile table 
    if t == 'dp':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/profile?get='+ c +'&for='+ g +':*&in=state:17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# Slightly different if the geography is place
##        q = urllib.urlopen('https://api.census.gov/data/2019  /acs/acs5/profile?get=NAME,DP0&for=place:*&in=state:17 
    
# If it is US geog and detail table
    if t == 'b' and g == 'us':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5?get='+ c +'&for='+ g +':1&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is US geog and subject table
    if t == 's' and g == 'us':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/subject?get='+ c +'&for='+ g +':*&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is US geog and profile table 
    if t == 'dp' and g == 'us':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/profile?get='+ c +'&for='+ g +':*&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
##        print q
        
# If it is state IL geog (17) and detail table
    if t == 'b' and g == 'state':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5?get='+ c +'&for='+ g +':17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is state IL geog and subject table
    if t == 's' and g == 'state':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/subject?get='+ c +'&for='+ g +':17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is state IL geog and profile table 
    if t == 'dp' and g == 'state':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5/profile?get='+ c +'&for='+ g +':17&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
# If it is block group        
    if t == 'b' and g == 'block%20group':
        q = urllib.urlopen('https://api.census.gov/data/'+ y +'/acs/acs5?get='+ c +'&for='+ g +':*&in=state:17&in=county:*&in=tract:*&key=80c94608225bef3ed8c2e24a6f4e7b4ddc1a9a22')
##        q = urllib.urlopen('http://api.census.gov/data/2019/acs/acs5?get=NAME,B01001_001E&for=block%20group:*&in=state:01&in=county:*&in=tract:*')

# Unpacking data    
    qdata = json.load(q)
##    print qdata
    for i in qdata:
        # Extract column 1 
        result = str(i[0])
        # If data has 'None' value, replace it with 0
        if result == '-666666666.0':
            result = '0'
        if result == '-666666666':
            result = '0'
        if result == '-999999999':
            result = '0'
##        print result
            
        # Append the extracted data into empty list
        raw_data.append(result)
##        print raw_data
 
    # Separating the variables from each other based on geography
    if g == 'us':
        n = 2
    if g == 'state':
        n = 2
    if g == 'county':
        n = 103
    if g == 'tract':
        n = 3124
    if g == 'place':
        n = 1370
    if g == 'block%20group':
        n = 9692
    
        
    # Putting each variable in separate list (column)   
    for j in xrange(0, len(raw_data),n):
        # Skip the title
        res = raw_data[j+1:j+n]
    # Append the extracted data into empty list
    data_final.append(res)
##    print data_final


# Name of variables to pull based on table type
bList = ['NAME', 'B01003_001E', 'B01002_001E', 'B25010_001E',
         'B25010_002E', 'B25010_003E', 'B25004_001E', 'B25035_001E']

sList = ['NAME', 'S0101_C01_014E', 'S0101_C01_015E', 'S0101_C01_016E',
         'S0101_C01_017E', 'S0101_C01_018E', 'S0101_C01_019E']  

##
dpList = ['NAME', 'DP02_0001E', 'DP02_0002E', 'DP02_0010E', 'DP04_0046E',
         'DP04_0047E', 'DP04_0046PE', 'DP04_0047PE', 'DP03_0062E', 'DP03_0063E',
         'DP03_0064PE', 'DP03_0065E', 'DP03_0072PE', 'DP03_0074PE', 'DP03_0092E',
         'DP03_0093E', 'DP03_0094E', 'DP03_0119PE', 'DP03_0128PE', 'DP03_0135PE',
         'DP03_0001E', 'DP03_0002E', 'DP03_0002PE', 'DP03_0005E', 'DP03_0009PE',
         'DP04_0001E', 'DP04_0003PE', 'DP04_0089E', 'DP04_0091E', 'DP04_0091PE',
         'DP04_0101E', 'DP04_0109E', 'DP04_0134E', 'DP04_0114PE', 'DP04_0115PE',
         'DP04_0123PE', 'DP04_0124PE', 'DP04_0141PE', 'DP04_0142PE']


t = types
g = geog
if t == 'b':
    ID = bList

if t == 's':
    ID = sList

if t == 'dp':
    ID = dpList

# Calling function 
for i in ID:
    censusAPI(year,i,geog)

if types == 's':
    name = data_final[0]
    # Summarize age, the age is broken into age buckets
    pop60 = map(sum , [map(int,i[1:]) for i in zip(*data_final)][0:] )
    pop65 = map(sum , [map(int,i[2:]) for i in zip(*data_final)][0:] )
    result = zip(*[name, pop60, pop65])
    sort_data = sorted(result, key=operator.itemgetter(0))
    csvwriter.writerows(sort_data)
else:
    result = zip(*data_final)
    sort_data = sorted(result, key=operator.itemgetter(0))
##    print sort_data
    csvwriter.writerows(sort_data)
