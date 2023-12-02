# EXTERNAL
from scipy.spatial import distance
import numpy as np

def create_itinerary(places, duration):
    # create a list just containing the coordinates to be used to create the matrix of
    #      all the distances
    coords = []
    for place in places:

        coord = (place['lat'], place['long'])
        coords.append(coord)

    # creates a matrix of all the distances between each point and every other point
    all_dist = distance.cdist(coords, coords, 'euclidean')
    # print(all_dist)

    places_copy = places.copy()    # creates a copy of the places list to be manipulated without altering the original

    # creates a key within the places_copy dict that holds a dict containing the distances
    #       to each of the other locations
    i = 0
    for place in places_copy:

        j = 0
        place['place_distances'] = {}
        
        for d in all_dist[i]:
            if d != 0.0:
                place['place_distances'][places_copy[j]['place_name']] = d
                
            j += 1
        i += 1

    # creates a list containing the sum of all the distances to each other location
    #       in order to compare proximities 
    sums = []
    for dist in all_dist:
        sums.append(sum(dist))

    # creates a key within places_copy that holds the sum of distances calculated above
    i = 0
    for s in sums:
        places_copy[i]['sum_dist'] = s
        i += 1

    ''' 1. Finds the location amongst the list of places that is furthest from the others.
        2. Removes that place from the places_copy list.
        3. Appends that location to the day_places list (see below)
        4. Continues this process X times where X is the number of days of the trip'''
    c = 0
    day_places = []      # gives you a list of places that matches the number of days, with each place being the furthest from others in order to create zones the user will visit each day
    while duration > c:

        max_value = 0
        max_place = ''

        # step 1
        for place in places_copy:

            if max_value < place['sum_dist']: 
                max_value = place['sum_dist']
                max_place = place['place_name']

        i = 0

        # step 2
        for place in places_copy:
            
            if place['place_name'] == max_place:
                places_copy.pop(i)
            
            i += 1

        # step 3
        day_places.append(max_place)

        # step 4
        c += 1

    ''' creates a list of days with each day being a dict that contains all the places for that day
        1. separate each day_place (the locations furthest from each other) into separate days in the list
        2. Go through each place dict to find the closest places to each of those max places, creating zones for each day
        3. Append each of those places to the list of days
        4. FINAL RESULT: Now have a list of days. Each day is a dict that contains the locations for that day.
            The information about those locations is also contained within the 'places' key of the day dict.
            The 'places' key is a list of dicts with the location information (with a key for each type of info) including: 
                    - place name
                    - lat
                    - long
                    - a dict containing the distance from that place to each of the other places
                    - the sum of the distances to each of the other places '''
    days = []

    # step 1
    for day_place in day_places:
        day = {}

        for place in places:
            if place['place_name'] == day_place:
                day['places'] = [place]
        
        days.append(day)

    # step 2
    for place in places_copy:

        min_value = 1000000
        min_place = ""

        for k, v in place['place_distances'].items():
            if k in day_places:

                if v < min_value:
                    min_value = v
                    min_place = k

        # step 3
        for day in days:
            if min_place == day['places'][0]['place_name']:

                day['places'].append(place)

    # print(day_places)

    return days

