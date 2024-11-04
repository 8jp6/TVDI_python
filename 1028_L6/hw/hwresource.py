import requests

def get_selected_data() -> list[list]:
    url = 'https://data.moenv.gov.tw/api/v2/aqx_p_488?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(e)
    else:
        outerlist = []
        for items in data['records']:
            innerlist = [items['sitename'],
                         items['county'],
                         items['aqi'],
                         items['status'],
                         items['pm2.5'],
                         items['datacreationdate'],
                         items['latitude'],
                         items['longitude']]
            outerlist.append(innerlist)
            
        return outerlist