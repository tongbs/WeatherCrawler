import time, DAN, requests, random, json
from datetime import datetime
# ServerURL = 'http://IP:9999' #with no secure connection
ServerURL = 'http://weathermap.iottalk.tw' #with SSL connection
Reg_addr = 'TaiwanWeather' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Weather'
DAN.profile['df_list']=['Temperature-I', 'WindSpeed-I','Humidity-I','RainMeter-I']
DAN.profile['d_name']= '1.Weather' # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-45155355-4921-4607-80AC-DC96B3293C8B&format=JSON'

def timestamp_handler(timestamp):
    year = str(datetime.now().year)
    month = timestamp.split()[0].split('/')[0]
    day = timestamp.split()[0].split('/')[1]
    hour = timestamp.split()[1].split(':')[0]
    minute = timestamp.split()[1].split(':')[1]
    second = '00'
    return year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second

time.sleep(10)
while True:
    try:
        data = requests.get(url)
        site_json = json.loads(data.text)
        for i in range(len(site_json['records']['location'])):
            loc = site_json['records']['location'][i]['locationName']         # string format
            loc_lat = float(site_json['records']['location'][i]['lat'])       
            loc_lon = float(site_json['records']['location'][i]['lon'])     
            obs_time = site_json['records']['location'][i]['time']['obsTime'] # string format

            # temperature, windspeed, humidity, rainmeter
            for j in range(len(site_json['records']['location'][i]['weatherElement'])):
                if site_json['records']['location'][i]['weatherElement'][j]['elementName'] == "WDSD":
                    WindSpeed = float(site_json['records']['location'][i]['weatherElement'][j]['elementValue'])
                    print('WindSpeed-I', loc_lat, loc_lon, loc, WindSpeed, obs_time)
                    DAN.push('WindSpeed-I', loc_lat, loc_lon, loc, WindSpeed, obs_time)
                    time.sleep(1)
                elif site_json['records']['location'][i]['weatherElement'][j]['elementName'] == "TEMP":
                    Temperature = float(site_json['records']['location'][i]['weatherElement'][j]['elementValue'])
                    print('Temperature-I', loc_lat, loc_lon, loc, Temperature, obs_time)
                    DAN.push('Temperature-I', loc_lat, loc_lon, loc, Temperature, obs_time)
                    time.sleep(1)
                elif site_json['records']['location'][i]['weatherElement'][j]['elementName'] == "HUMD":
                    Humidity = float(site_json['records']['location'][i]['weatherElement'][j]['elementValue'])
                    print('Humidity-I', loc_lat, loc_lon, loc, Humidity, obs_time)
                    DAN.push('Humidity-I', loc_lat, loc_lon, loc, Humidity, obs_time)
                    time.sleep(1)
                elif site_json['records']['location'][i]['weatherElement'][j]['elementName'] == "H_24R":
                    Rainmeter = float(site_json['records']['location'][i]['weatherElement'][j]['elementValue'])
                    print('RainMeter-I', loc_lat, loc_lon, loc, Rainmeter, obs_time)
                    DAN.push('RainMeter-I', loc_lat, loc_lon, loc, Rainmeter, obs_time)
                    time.sleep(1)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    #計時十分鐘後再抓
    time.sleep(1000)
