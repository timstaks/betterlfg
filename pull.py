import requests, json, csv
from datetime import datetime

#gets access token for oath api requests using my developer creds
def get_access_token():
    creds = open('credentials.txt','r')
    creds = creds.readlines()
    c_id = creds[0].rstrip()
    c_secret = creds[1]
    access_token = requests.post("https://us.battle.net/oauth/token?grant_type=client_credentials&client_id="+c_id+"&client_secret="+c_secret+"").json()["access_token"]
    return access_token

#pulls class of a character if character exists
def retrieve(c_Name,c_Realm,region,apikey):
    try:
        response = requests.get("https://"+region+".api.blizzard.com/profile/wow/character/"+c_Realm+"/"+c_Name+"?namespace=profile-us&locale=en_US&access_token="+apikey+"")
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return '404'
    return response.json()['character_class']['name']

#converts millisecond timestamp to utc date
def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')

#pulls desired rating and date earned stats for a character
def get_pvp_stats(c_Name,c_Realm,region,apikey):
    r = requests.get("https://"+region+".api.blizzard.com/profile/wow/character/"+c_Realm+"/"+c_Name+"/achievements/statistics?namespace=profile-us&locale=en_US&access_token="+apikey+"").json()
    d = [0,None,0,None]

    #clumsy code but functional - seek better method pandas/javascript/idk
    for e in r['categories']:
        if e['id']==21:
            for x in e['sub_categories']:
                if x['id']==152:
                    for q in x['statistics']:
                        if q['id']==595:
                            d[0]=q['quantity']
                            d[1]=convert_timestamp(q['last_updated_timestamp'])
                        if q['id']==370:
                            d[2]=q['quantity']
                            d[3]=convert_timestamp(q['last_updated_timestamp'])
    return d

region="us"
apikey=get_access_token()

#reads a csv of character names and creates data set of class/3v3rating/date/2v2rating/date
def update_char_stats(region,apikey):
    d=[]
    with open('WoWCharacters.csv',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        l_c = 0
        for row in csv_reader:
            realm = row[0].lower()
            name = row[1].lower()
            if l_c!=0:
                job=retrieve(name,realm,region,apikey)
                if job=='404':
                    continue
                pvp=get_pvp_stats(name,realm,region,apikey)
                stats = [name,realm,job]
                for e in pvp:
                    stats.append(e)
                d.append(stats)           
            l_c+=1
            if l_c==101:
                break
    
    with open('lfChar.csv',mode='w',encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file,delimiter=',',quoting=csv.QUOTE_MINIMAL)
        for e in d:
            writer.writerow(e)

update_char_stats(region,apikey)

