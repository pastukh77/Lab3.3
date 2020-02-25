import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium

from opencage.geocoder import OpenCageGeocode

key = '80242c705fa94567b6bc8935ffad37b1'
geocoder = OpenCageGeocode(key)

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py


def main(acct):
    '''
    This function reads IP, gets json file and saves a map with Twitter friends location
    '''

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '110'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])

    my_map = folium.Map(zoom_start=2)
    fg = folium.FeatureGroup(name='Markers')

    for u in js['users']:
        try:
            query = u['location']
            results = geocoder.geocode(query)
            try:
                location = [results[0]['geometry']['lat'], results[0]['geometry']['lng']]
                fg.add_child(folium.Marker(location=location, icon=folium.Icon(icon='cloud', color='orange'), popup=u['screen_name']))

            except IndexError:
                continue
        except AttributeError:
            continue

    my_map.add_child(fg)
    my_map.add_child(folium.LayerControl())
    my_map.save('templates/{0}.html'.format(acct))




