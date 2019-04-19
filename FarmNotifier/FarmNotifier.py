import csv
import requests
import datetime
import json

#GlobalVariables
key = '75c67c257927d0e8bbc059b8dd4b227a'
url = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&units=metric&APPID=' + key

#Weather Codes
safeCodes = [800, 801, 802, 803, 804]

def loadFile(filename = 'CSVFile/cityid.csv'):
    citydict = dict()
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        key = headers[1]
        value = headers[0]
        for l in csvreader:
            citydict[l[1].lower()] = l[0]
    return citydict

def Query(city='gurgaon'):
    j = loadFile()
    u = ''
    try:
        u = url % str(j[city.lower()])
    except KeyError as e:
        print('City not present: ', e)
    return u

def callServer(url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Status Not 200')
        print(r.text)
    return r.json()

def getWeatherCodeFromJson(j):
    clist = j['list']
    dateCode = list()
    for l in clist:
        date = l['dt']
        code = l['weather'][0]['id']
        description = l['weather'][0]['main'] + ' - ' +l['weather'][0]['description']
        dateCode.append((date,code, description))
    return dateCode

def filterNormalCodes(dc):
    l = list()
    for date,code,desc in dc:
        if code not in safeCodes:
            l.append((date,code,desc))
    return l

def prettyPrintDateCode(dc):
    getdate = datetime.datetime.utcfromtimestamp
    for date,code,desc in dc:
        d = getdate(date)
        print(d, code, desc, sep='\t')

if __name__ == '__main__':
    q = Query('Cochin')
    j = callServer(q)
    dc = getWeatherCodeFromJson(j)
    prettyPrintDateCode(filterNormalCodes(dc))