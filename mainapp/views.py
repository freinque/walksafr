import django.http
import django.template
import django.forms
import django.contrib

import django_pandas.io

import mainapp.forms
import mainapp.models
import mainapp.api.api_script
import mainapp.walksafr
import website.settings

import numpy as np
import pandas as pd
import os
import datetime

import sklearn.neighbors 
import sklearn.grid_search 

#import sys
#sys.path.append( os.path.dirname(os.path.realpath(__file__)) + '/something' )

def pdf_view(request):
    file_path = os.path.join(website.settings.STATIC_ROOT, 'mainapp/Francois_Charest_demo_5.pdf')
    with open(file_path, 'rb') as pdf:
        response = django.http.HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=walk_safr_slides.pdf'
        return response
    pdf.closed

def form_input(request):
    if request.method == 'GET':
        form = mainapp.forms.EndsForm()
        template = django.template.loader.get_template('mainapp/form_input.html')
        context = django.template.RequestContext(request, {'form': form,})
        
        return django.http.HttpResponse(template.render(context))

    if request.method == 'POST':
        form = mainapp.forms.EndsForm()
        template = django.template.loader.get_template('mainapp/form_input.html')
        context = django.template.RequestContext(request, {'form': form,})
        
        return django.http.HttpResponse(template.render(context))

def form_output(request):
    if request.method == 'GET':
        form = mainapp.forms.EndsForm()
        template = django.template.loader.get_template('mainapp/form_input.html')
        context = django.template.RequestContext(request, {'form': form,})

        return django.http.HttpResponse(template.render(context))

    if request.method == 'POST':
        form = mainapp.forms.EndsForm(request.POST)
        
        ###if address not valid
        if (not form.is_valid()):
            form = mainapp.forms.EndsForm()
            template = django.template.loader.get_template('mainapp/form_input.html')
            context = django.template.RequestContext(request, {'form': form,})
        
            django.contrib.messages.add_message(request, django.contrib.messages.ERROR, 'Invalid input. Make sure that you\'re entering valid and complete SF (strictly) addresses and datetime. The address autocomplete should help.')
            
            return django.http.HttpResponse(template.render(context))
        
        ###tweaking form
        ends = form.save(commit=False)
        ends.ends_datetime = datetime.datetime.combine(ends.ends_date, ends.ends_time)
        ends.orig_city = ends.orig_city.lower()
        ends.dest_city = ends.dest_city.lower()
        #form = mainapp.forms.EndsForm(request.POST, instance=ends)
        
        ###random orig and dest used to test
        #MAX_DIST = 0.02
        #[[x_orig_rand,y_orig_rand],[x_dest_rand,y_dest_rand]] = mainapp.walksafr.get_random_coord(-122.507, -122.378, 37.71, 37.806, MAX_DIST)
        #ends.orig_long = str(x_orig_rand)
        #ends.orig_lati = str(y_orig_rand)
        #ends.dest_long = str(x_dest_rand)
        #ends.dest_lati = str(y_dest_rand)

        ###if address outside of SF
        if ((not ends.orig_city == 'san francisco') or (not ends.dest_city == 'san francisco')):
            template = django.template.loader.get_template('mainapp/form_input.html')
            context = django.template.RequestContext(request, {'form': form,})
        
            django.contrib.messages.add_message(request, django.contrib.messages.ERROR, 'Make sure that you\'re entering SF (strictly) addresses until WalkSafr expands to your city...')
            
            return django.http.HttpResponse(template.render(context))
        
        ###if everything is cool
        else:
            form.save()

            ############ generate routes using mainapp.api.api_script.get_poly
            print 'generate routes starts'
            N_WAYPOINTS = 5 #odd number!
            N_WAYPOINTS_OVER_2 = N_WAYPOINTS/2
            polys = []
            uni_polys = []
            poly_search_api_urls = []
            embed_dir_api_urls = []
        
            WAYPOINT_FACTOR = 0.13
            for waypoint in np.arange(-N_WAYPOINTS_OVER_2,N_WAYPOINTS_OVER_2+1):
                poly_temp, poly_search_api_url_temp, embed_dir_api_url_temp = mainapp.api.api_script.get_poly(ends.orig_lati + ',' + ends.orig_long,ends.dest_lati + ',' + ends.dest_long, WAYPOINT_FACTOR*waypoint)
                uni_poly_temp = mainapp.walksafr.uniform_poly( poly_temp )
                
                polys.append( poly_temp )
                poly_search_api_urls.append( poly_search_api_url_temp )
                embed_dir_api_urls.append( embed_dir_api_url_temp )    
                uni_polys.append( uni_poly_temp )
            
            print 'generate routes ends'
        
            ########## setting up parameters
            EPSILON = 0.0001 
            N_DAYS_BEFORE = 30
            POPULATION_BANDWIDTH = 0.015
            CRIME_BANDWIDTH = 0.0005
            GLOBAL_CRIME_BANDWIDTH = 0.0005 #0.001 #this should ideally depend on the context, but we want to save time
            x_bot, x_top, y_bot, y_top = mainapp.walksafr.get_bot_top( uni_polys )
            global_x_bot, global_x_top, global_y_bot, global_y_top = (-122.5228, -122.3511, 37.6980, 37.8097)
            
            
            ########## local crime
            print 'local crimes starts'
        
            crimes_around, grid_around = mainapp.walksafr.get_crimes_around( x_bot, x_top, y_bot, y_top, datetime.datetime(2015,8,1)-datetime.timedelta(days=N_DAYS_BEFORE), datetime.datetime(2015,8,1), EPSILON)
            crimes_around['ns_time'] = crimes_around['ns_time'].apply(lambda x:datetime.datetime.strptime(str(x),'%H:%M:%S'))
            crimes_around['time_of_day'] = crimes_around.apply(lambda row: EPSILON*(row['ns_time'].hour), axis=1)
        
            crime_X = np.array( crimes_around[['time_of_day','x','y']] )
        
            ### fixed crime_bandwidth, but here is (roughly) how I chose parameters: 
            #cv_grid = sklearn.grid_search.GridSearchCV(sklearn.neighbors.KernelDensity(),{'bandwidth': np.linspace(0.00001, .002, 5)}, cv=5)
            #cv_grid.fit(crime_X)
            crime_bandwidth = CRIME_BANDWIDTH #cv_grid.best_params_['bandwidth']
            #print 'local crimes bandwidth: ' + str(crime_bandwidth)

            crime_kernel_density_model = sklearn.neighbors.KernelDensity(kernel='gaussian',bandwidth=crime_bandwidth)
            crime_kernel_density_model.fit( crime_X )
        
            print 'local crimes ends'

            ########## global crime
            print 'global crimes starts'
            crimes_global, grid_global = mainapp.walksafr.get_crimes_around(global_x_bot, global_x_top, global_y_bot, global_y_top, datetime.datetime(2015,8,1)-datetime.timedelta(days=7), datetime.datetime(2015,8,1), EPSILON)
            crimes_global['ns_time'] = crimes_global['ns_time'].apply(lambda x:datetime.datetime.strptime(str(x),'%H:%M:%S'))
            crimes_global['time_of_day'] = crimes_global.apply(lambda row: EPSILON*(row['ns_time'].hour), axis=1)
        
            global_crime_X = np.array( crimes_global[['time_of_day','x','y']] )
        
            #cv_grid = sklearn.grid_search.GridSearchCV(sklearn.neighbors.KernelDensity(),{'bandwidth': np.linspace(0.0001, .001, 20)}, cv=5)
            #cv_grid.fit(global_crime_X)
            crime_bandwidth = GLOBAL_CRIME_BANDWIDTH #cv_grid.best_params_['bandwidth']
            #print 'global crimes bandwidth: ' + str(crime_bandwidth)

            global_crime_kernel_density_model = sklearn.neighbors.KernelDensity(kernel='gaussian',bandwidth=crime_bandwidth)
            global_crime_kernel_density_model.fit( global_crime_X )
            print 'global crimes ends'
        
            ######### local population, having in mind a more accurate measure of population density
            #print 'local pop starts'
            #population_around, population_grid_around = mainapp.walksafr.get_population_around( x_bot, x_top, y_bot, y_top, datetime.datetime(2015,8,1)-datetime.timedelta(days=N_DAYS_BEFORE), datetime.datetime(2015,8,1), EPSILON)
            #population_around['time_of_day'] = population_around.apply(lambda row: EPSILON*(row['ns_time']), axis=1)
        
            #population_X = np.array( population_around[['time_of_day','x','y']] )
         
            #cv_grid = sklearn.grid_search.GridSearchCV(sklearn.neighbors.KernelDensity(),{'bandwidth': np.linspace(0.001, .04, 5)}, cv=5)
            #cv_grid.fit(population_X)
            #population_bandwidth = cv_grid.best_params_['bandwidth']
            #population_bandwidth = POPULATION_BANDWIDTH

            #population_kernel_density_model = sklearn.neighbors.KernelDensity(kernel='gaussian',bandwidth=population_bandwidth)
            #population_kernel_density_model.fit( population_X )
            #print 'local pop ends'
        
            ######### global population
            print 'global pop starts'
            population_global, grid_global = mainapp.walksafr.get_population_around(global_x_bot, global_x_top, global_y_bot, global_y_top, datetime.datetime(2015,8,1)-datetime.timedelta(days=7), datetime.datetime(2015,8,1), EPSILON)
            population_global['time_of_day'] = population_global.apply(lambda row: EPSILON*(row['ns_time']), axis=1)
        
            print population_global
        
            global_population_X = np.array( population_global[['time_of_day','x','y']] )
         
            #cv_grid = sklearn.grid_search.GridSearchCV(sklearn.neighbors.KernelDensity(),{'bandwidth': np.linspace(0.001, .04, 5)}, cv=5)
            #cv_grid.fit(population_X)
            #population_bandwidth = cv_grid.best_params_['bandwidth']
            population_bandwidth = POPULATION_BANDWIDTH

            global_population_kernel_density_model = sklearn.neighbors.KernelDensity(kernel='gaussian',bandwidth=population_bandwidth)
            global_population_kernel_density_model.fit( global_population_X )
            print 'local pop ends'

            ############# integration along paths
            print 'integration starts'
            grid_polys = []
            global_grid_polys = []
            #density_along_polys = []
            sum_quotient_density_along_polys = []
            sum_crime_density_along_polys = []
            mean_global_population_density_along_polys = []
            mean_global_crime_density_along_polys = []
            for waypoint_n in range(N_WAYPOINTS):
                uni_poly = pd.DataFrame(uni_polys[waypoint_n], columns=['x','y'])
                uni_poly['ns_time'] = [ends.ends_datetime]*len(uni_poly)
                uni_poly['time_of_day'] = uni_poly.apply(lambda row: EPSILON*(row['ns_time'].hour), axis=1)
            
                ### local
                grid_poly = mainapp.walksafr.project_on_grid( np.array(uni_poly[['time_of_day','x','y']]), grid_around )
                grid_polys.append( grid_poly )
           
                crime_density_along_poly = crime_kernel_density_model.score_samples( grid_poly )
                crime_density_along_poly = np.exp(crime_density_along_poly)
            
                sum_crime_density_along_polys.append( np.sum(crime_density_along_poly) )       
            
                #population_density_along_poly = population_kernel_density_model.score_samples( grid_poly )
                #population_density_along_poly = np.exp(population_density_along_poly)
            
                ### global
                global_grid_poly = mainapp.walksafr.project_on_grid( np.array(uni_poly[['time_of_day','x','y']]), grid_global )
                global_grid_polys.append( global_grid_poly )
    
                global_crime_density_along_poly = global_crime_kernel_density_model.score_samples( global_grid_poly )
                global_crime_density_along_poly = np.exp(global_crime_density_along_poly)
 
                #print global_crime_density_along_poly

                global_population_density_along_poly = global_population_kernel_density_model.score_samples( global_grid_poly )
                global_population_density_along_poly = np.exp(global_population_density_along_poly)
             
                #print global_population_density_along_poly
            
                #global_quotient_density_along_poly = global_crime_density_along_poly/global_population_density_along_poly

                mean_global_crime_density_along_polys.append( np.mean(global_crime_density_along_poly) )       
            
                mean_global_population_density_along_poly = np.mean(global_population_density_along_poly)
                mean_global_population_density_along_polys.append( mean_global_population_density_along_poly )       
 
                ### quotient
                
                #quotient_density_along_poly = crime_density_along_poly/population_density_along_poly
                quotient_density_along_poly = crime_density_along_poly/mean_global_population_density_along_poly
                sum_quotient_density_along_polys.append( np.sum(quotient_density_along_poly) )       
            

            ### normalizing local densities
            sum_crime_density_along_polys = sum_crime_density_along_polys/np.min(sum_crime_density_along_polys)
        
            sum_quotient_density_along_polys = sum_quotient_density_along_polys/np.min(sum_quotient_density_along_polys)
        
            ### normalizing by global densities
            #mean_global_population_density_along  = np.mean(mean_global_population_density_along_polys)
            #mean_global_crime_density_along = np.mean(mean_global_crime_density_along_polys)
        
            #mean_global_quotient_density = 
            mean_global_density = 1./((global_x_top-global_x_bot)*0.85*(global_y_top-global_y_bot)*0.85*24*EPSILON) #size of grid

            #print mean_global_quotient_density_along_polys
            print np.array(mean_global_crime_density_along_polys)/mean_global_density
            print np.array(mean_global_population_density_along_polys)/mean_global_density
            print 'integration ends'
        
            ########## rendering the output template
            javascript_api_url = mainapp.api.api_script.get_javascript_api_url()

            center_long = (grid_around[0,0,0][1]+grid_around[0,-1,0][1])/2.
            center_lati = (grid_around[0,0,0][2]+grid_around[0,0,-1][2])/2.
        
            ###a dict with the relavant info for each waypoint
            waypoint_infos = [ {'waypoint_n':(w-N_WAYPOINTS/2), 'display_waypoint_n':w+1, 'embed_dir_api_url':embed_dir_api_urls[w], 'sum_quotient_density_along_poly':sum_quotient_density_along_polys[w],'sum_crime_density_along_poly':sum_crime_density_along_polys[w],'poly':polys[w],} for w in range(N_WAYPOINTS) ]
            waypoint_infos = sorted(waypoint_infos, key= lambda x: x['sum_quotient_density_along_poly'])
       
            display_colors = [ 'rgb(%d,%d,0)'%(i*255/(N_WAYPOINTS-1), 255-(i*255/(N_WAYPOINTS-1))) for i in range(N_WAYPOINTS) ]
            for i in range(len(waypoint_infos)):
                waypoint_infos[i]['display_color'] = display_colors[i]
                waypoint_infos[i]['display_waypoint_n'] = i+1

            template = django.template.loader.get_template('mainapp/form_output.html')
            context = django.template.RequestContext(request, {'form': form,})
            context.push({ 'waypoint_infos': waypoint_infos, 'javascript_api_url':javascript_api_url, 'crimes_around':np.array( crimes_around[['x','y']]),'center_long':center_long,'center_lati':center_lati,'orig_long':ends.orig_long,'orig_lati':ends.orig_lati,'dest_long':ends.dest_long,'dest_lati':ends.dest_lati,})

            return django.http.HttpResponse(template.render(context))



