import django_pandas.io

import mainapp.models

import numpy as np
import pandas as pd
import datetime

#, sys
#sys.path.append( os.path.dirname(os.path.realpath(__file__)) + '/something' )

def get_crimes_around(bot_x=-122.5228, top_x=-122.3511, bot_y=37.6980, top_y=37.8097, start_date=None, end_date=None, epsilon=1, grid_size = 100, time_grid_size = 24):
    '''
    returns dataframe of crime points within the specified bounds plus a local grid
    '''
    EXTRA_MARGIN = 0.01
    
    # constructing grid
    x_a = np.linspace( bot_x-EXTRA_MARGIN, top_x+EXTRA_MARGIN, grid_size)
    y_a = np.linspace( bot_y-EXTRA_MARGIN, top_y+EXTRA_MARGIN, grid_size)
    t_a = np.linspace( 0, (time_grid_size-1)*epsilon, time_grid_size)
    t,x,y = np.meshgrid(t_a,x_a,y_a, sparse=False, indexing='ij')

    nearby_grid = np.array([[[[t[k,j,i],x[k,j,i],y[k,j,i]] for i in range(grid_size)]for j in range(grid_size)]for k in range(time_grid_size)])

    # constructing dataframe
    qs = mainapp.models.Crimes.objects.all()
    filtered_qs = qs.filter(datetime__gte=start_date, datetime__lte=end_date, x__lte=top_x+EXTRA_MARGIN, x__gte=bot_x-EXTRA_MARGIN, y__lte=top_y+EXTRA_MARGIN, y__gte=bot_y-EXTRA_MARGIN)
    
    nearby_crimes = django_pandas.io.read_frame(filtered_qs)

    print str(len(nearby_crimes)) + ' crimes found '
    
    return nearby_crimes, nearby_grid

def get_tweets_around(bot_x=-122.5228, top_x=-122.3511, bot_y=37.6980, top_y=37.8097, start_date=None, end_date=None, epsilon=1, grid_size = 100, time_grid_size = 24):
    '''
    returns dataframe of crime points within the specified bounds plus a local grid
    '''
    EXTRA_MARGIN = 0.01
    
    # constructing grid
    x_a = np.linspace( bot_x-EXTRA_MARGIN, top_x+EXTRA_MARGIN, grid_size)
    y_a = np.linspace( bot_y-EXTRA_MARGIN, top_y+EXTRA_MARGIN, grid_size)
    t_a = np.linspace( 0, (time_grid_size-1)*epsilon, time_grid_size)
    t,x,y = np.meshgrid(t_a,x_a,y_a, sparse=False, indexing='ij')

    nearby_grid = np.array([[[[t[k,j,i],x[k,j,i],y[k,j,i]] for i in range(grid_size)]for j in range(grid_size)]for k in range(time_grid_size)])

    # constructing dataframe
    qs = mainapp.models.Tweets.objects.all()
    filtered_qs = qs.filter( x__lte=top_x+EXTRA_MARGIN, x__gte=bot_x-EXTRA_MARGIN, y__lte=top_y+EXTRA_MARGIN, y__gte=bot_y-EXTRA_MARGIN)
    #ns_datetime__gte=start_date, ns_datetime__lte=end_date,
    
    nearby_tweets = django_pandas.io.read_frame(filtered_qs)

    print str(len(nearby_tweets)) + ' tweets found '
    
    return nearby_tweets, nearby_grid
  
def get_population_around(bot_x=-122.5228, top_x=-122.3511, bot_y=37.6980, top_y=37.8097, start_date=None, end_date=None, epsilon=1, grid_size = 100, time_grid_size = 24):
    '''
    returns dataframe of population points within the specified bounds plus a local grid
    '''
    EXTRA_MARGIN = 0.005

    # constructing grid
    x_a = np.linspace( bot_x-EXTRA_MARGIN, top_x+EXTRA_MARGIN, grid_size)
    y_a = np.linspace( bot_y-EXTRA_MARGIN, top_y+EXTRA_MARGIN, grid_size)
    t_a = np.linspace( 0, (time_grid_size-1)*epsilon, time_grid_size)
    t,x,y = np.meshgrid(t_a,x_a,y_a, sparse=False, indexing='ij')

    nearby_grid = np.array([[[[t[k,j,i],x[k,j,i],y[k,j,i]] for i in range(grid_size)]for j in range(grid_size)]for k in range(time_grid_size)])

    # constructing dataframe
    qs = mainapp.models.PopDensity.objects.all()
    
    filtered_qs = qs.filter(x__lte=top_x+EXTRA_MARGIN, x__gte=bot_x-EXTRA_MARGIN, y__lte=top_y+EXTRA_MARGIN, y__gte=bot_y-EXTRA_MARGIN)
    #filtered_qs = qs.filter(datetime__gte=start_date, datetime__lte=end_date, x__lte=top_x, x__gte=bot_x, y__lte=top_y, y__gte=bot_y)
    
    nearby_population = django_pandas.io.read_frame(filtered_qs)

    nearby_populations = []
    for t in range(time_grid_size):
        nearby_population_temp = np.array(nearby_population[['x','y','density']])

        nearby_population_temp = np.hstack([np.ones((len(nearby_population_temp),1))*t, nearby_population_temp])
        nearby_populations.append( nearby_population_temp )
    
    nearby_population = np.vstack(nearby_populations) 
    nearby_population = pd.DataFrame( nearby_population, columns=['ns_time','x','y','density'])

    nearby_population['density'] = 3000*nearby_population['density']/np.sum(nearby_population['density'])
    
    print str(len(nearby_population)) + ' population points found'

    ###? here I'm representing the pop weight of the points by adding a proportional nb of points... annoying
    nearby_population_weighted = []
    for i in range(len(nearby_population)):
        for n in range(int(nearby_population[['ns_time','x','y','density']].loc[i][['density']])):
            nearby_population_weighted.append( np.array(nearby_population[['ns_time','x','y','density']].loc[i][['ns_time','x','y']]) )
    nearby_population_weighted = pd.DataFrame( nearby_population_weighted, columns=['ns_time','x','y'])
    
    return nearby_population_weighted, nearby_grid


def uniform_poly(poly):
    '''
    returns a uni_poly (np.array of shape (n,2)) of consecutive points at distance less than DELTA from each other
    *longitude becomes first
    '''
    #btw, the output has its x coordinates first
    DELTA = 0.0004 #not so related to EPSILON
    uni_poly = []
                
    for i in range(1,len(poly)):
        disp = np.linalg.norm(poly[i]-poly[i-1])
        to_add = [poly[i-1]]
        to_add += [poly[i-1]+ j*DELTA*(poly[i]-poly[i-1])/disp for j in range(int(disp/DELTA))]
        uni_poly += to_add
                                                            
    uni_poly.append(poly[-1])
    uni_poly = [[uni_poly[i][1],uni_poly[i][0]] for i in range(len(uni_poly))]

    return np.array(uni_poly)

def get_bot_top( uni_polys ):
    '''
    returns the coordinate extrema from a collection of uni_polys
    '''
    x_bot = 1000
    x_top = -1000
    y_bot = 1000
    y_top = -1000 

    for uni_poly in uni_polys:
        x_bot = min( np.min(uni_poly[:,0]), x_bot)
        y_bot = min( np.min(uni_poly[:,1]), y_bot)
        x_top = max( np.max(uni_poly[:,0]), x_top)
        y_top = max( np.max(uni_poly[:,1]), y_top)

    return x_bot, x_top, y_bot, y_top

def project_on_grid(uni_poly, grid):
    '''
    returns the points of grid close to a point of uni_poly
    '''
    t_n, x_n, y_n = grid.shape[0:3]
    t_n = t_n - 1
    x_n = x_n - 1
    y_n = y_n - 1
    t_max, x_max, y_max = grid[-1,-1,-1]
    t_min, x_min, y_min = grid[0,0,0]
    delta_t = t_max - t_min
    delta_x = x_max - x_min
    delta_y = y_max - y_min
    
    grid_points = np.array([ grid[ int( t_n*(uni_poly[i][0]-t_min)/delta_t ), int( x_n*(uni_poly[i][1]-x_min)/delta_x ), int( y_n*(uni_poly[i][2]-y_min)/delta_y ) ] for i in range(len(uni_poly)) ]) 
    #grid_points = pd.DataFrame( grid_points, columns=['x','y'] )
    #grid_points.drop_duplicates() #?
    
    return grid_points

def dist_seg_pt(pt,endpt_1,endpt_2):
    if ( (np.dot(endpt_2-endpt_1,pt-endpt_1) >= 0) and ( np.dot(endpt_1-endpt_2,pt-endpt_2) >= 0 ) ):
        normal = np.array([-(endpt_2-endpt_1)[1],(endpt_2-endpt_1)[0]])
        normal = normal/ math.sqrt( np.dot(normal,normal) )

        dist_line = abs(np.dot(pt-endpt_1,normal))
        return dist_line
    else:
        dist_endpt_1 = math.sqrt(np.dot(pt-endpt_1,pt-endpt_1))
        dist_endpt_2 = math.sqrt(np.dot(pt-endpt_2,pt-endpt_2))
        return min(dist_endpt_1,dist_endpt_2)

def get_random_coord(x_min, x_max, y_min, y_max, max_dist):
    '''
    returns two points in the rectangle x_min, x_max, y_min, y_max not further than max_dist from each other
    '''
    repeat = True
    while repeat == True:
        x_rand = np.random.uniform(x_min, x_max, 2)
        y_rand = np.random.uniform(y_min, y_max, 2)

        d2 = ((x_rand[1]-x_rand[0])**2 +(y_rand[1]-y_rand[0])**2)
        if d2 < (max_dist)**2:
            repeat = False
    return [[x_rand[0],y_rand[0]], [x_rand[1],y_rand[1]]] 


