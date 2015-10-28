import urllib2
import json
import polyline.codec 
import os
import numpy as np

def get_poly(dest, orig, waypoint=0.0):
    '''
    where dest and orig look like '40.813456,-73.956435' ...
    '''

    key_file = open( os.path.join(os.path.dirname(os.path.abspath(__file__)), 'google_api_key.txt') )
    api_key = key_file.read().strip()
    
    combined_dict = {}
    combined_dict['origin'] = dest
    combined_dict['destination'] = orig
    combined_dict['mode'] = 'walking'
    if waypoint !=0.0:
        origin = np.array([ float(orig.split(',')[0]), float(orig.split(',')[1]) ])
        destination = np.array([ float(dest.split(',')[0]), float(dest.split(',')[1]) ])
        mean = (origin + destination)/2.0
        diff = destination - origin
        diff_perp = np.array( [diff[1],-diff[0]] )
        extra = mean + waypoint*diff_perp

        combined_dict['waypoints'] = '%f,%f'%(extra[0],extra[1])

    sparams = {}
    sparams['type'] = 'json'
    sparams['api_key'] = api_key
    sparams['combined_dict'] = ''.join(['%s=%s&'%(key, combined_dict[key]) for key in combined_dict])
    
    poly_search_api_url = "https://maps.googleapis.com/maps/api/directions/{0[type]}?{0[combined_dict]}key={0[api_key]}".format(sparams)
    
    dirparams = {}
    dirparams['api_key'] = api_key
    dirparams['combined_dict'] = ''.join(['&'+'%s=%s'%(key, combined_dict[key]) for key in combined_dict])

    embed_dir_search_api_url = "https://www.google.com/maps/embed/v1/directions?key={0[api_key]}{0[combined_dict]}".format(dirparams)

    response = urllib2.urlopen(poly_search_api_url)
    json_data = json.load(response)

    poly_line = []
    for i in range(len(json_data['routes'])):
        for j in range(len(json_data['routes'][i]['legs'])):
            for k in range(len(json_data['routes'][i]['legs'][j]['steps'])):
                points_str = json_data['routes'][i]['legs'][j]['steps'][k]['polyline']['points']
                points = polyline.codec.PolylineCodec().decode( points_str )
                poly_line += points

    return np.array(poly_line), poly_search_api_url, embed_dir_search_api_url


def get_javascript_api_url():
    key_file = open( os.path.join(os.path.dirname(os.path.abspath(__file__)), 'google_api_key.txt') )
    api_key = key_file.read().strip()
     
    combined_dict = {}
    combined_dict['signed_in'] = 'true'
    combined_dict['libraries'] = 'visualization'
    combined_dict['callback'] = 'initMap'

    sparams = {}
    sparams['type'] = 'js'
    sparams['api_key'] = api_key
    sparams['combined_dict'] = ''.join(['&'+'%s=%s'%(key, combined_dict[key]) for key in combined_dict])
    
    javascript_api_url = "https://maps.googleapis.com/maps/api/{0[type]}?key={0[api_key]}{0[combined_dict]}".format(sparams)
   
    return javascript_api_url


def get_twitter_api_url():
    #twitter_api_url = "https://stream.twitter.com/1.1/statuses/filter.json?track=twitter&locations=-122.75,36.8,-121.75,37.8".format(sparams)
    twitter_api_url = "https://api.twitter.com/1.1/geo/search.json?place_id=-122.75,36.8,-121.75,37.8".format(sparams)
 
    response = urllib2.urlopen(twitter_api_url)
    json_data = json.load(response)

  
    return twitter_api_url


