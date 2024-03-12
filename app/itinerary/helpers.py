# EXTERNAL
from scipy.spatial import distance
import numpy as np

# INTERNAL
from app.models import Place, db

'''
Takes a list of Place objects and a trip duration and returns a dictionary of days that contains 
all the information needed for that day: such as all the trips associated with it
'''
def create_itinerary(places, duration):

    days = {}
    day_order = []    # [day-1, day-2, day-3, ...]
    places_dict = {}   # creates a serialized list (dict) that holds the place id as a key for each place object

    for place in places:
        places_dict[place['id']] = place

    if len(places) < 2:

        for i in range(duration):
            days[f'day-{i + 1}'] = {
                'id': f'day-{i + 1}',
                'placeIds': []
            } 
            day_order.append(f'day-{i + 1}') 

        days['day-1'] = {
            'id': 'day-1',
            'placeIds': [1]
        }

        return {
            "days": days,
            "day_order": day_order
        }
    
    print(places)


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
    dist_range = 0

    # creates a key within the places_copy dict that holds a dict containing the distances
    #       to each of the other locations
    i = 0
    for place in places_copy:

        j = 0
        place['place_distances'] = {}
        
        for d in all_dist[i]:
            if d != 0.0:
                place['place_distances'][places_copy[j]['id']] = d
                dist_range = max(d, dist_range)
                
            j += 1
        i += 1

    print(all_dist)
    print(dist_range)
    
    threshold_range = 0.15 * dist_range

    # creates a list containing the sum of all the distances to each other location
    #       in order to compare proximities 
    sums = []
    for dist in all_dist:
        sums.append(sum(dist))

    # creates a key within places_copy that holds the sum of distances calculated above
    i = 0
    for i in range(len(sums)):
        places_copy[i]['sum_dist'] = sums[i]
        i += 1

    ''' 1. Finds the location amongst the list of places that is furthest from the others.
        2. Removes that place from the places_copy list.
        3. Appends that location to the day_places list (see below)
        4. Continues this process X times where X is the number of days of the trip'''
    c = 0
    day_places = []      # gives you a list of place ids that matches the number of days, with each place being the furthest from others in order to create zones the user will visit each day
    co_captains = {}

    while duration > c:

        max_value = 0
        max_place = ''

        # step 1
        for place in places_copy:

            if max_value < place['sum_dist']: 
                max_value = place['sum_dist']
                max_place = place['id']   

        i = 0

        # step 2
        for place in places_copy:
            
            if place['id'] == max_place:
                for p, d in place['place_distances'].items():

                    print("Captain =", place['id'])

                    if d < threshold_range:

                        print(place['place_distances'])

                        print("p in loop = ", p)

                        try:
                            co_cap_index = places_copy.index(co_captain)
                            places_copy.pop(co_cap_index)

                            if place['id'] not in co_captains.keys():
                                co_captains[place['id']] = [p]
                            elif len(co_captains[place['id']]) < 4:
                                co_captains[place['id']].append(p)
                            elif len(co_captains[place['id']]) >= 4:
                                continue
                        
                        except:
                            continue
                    
                        co_captain = places[p - 1]
                        print("p = ", p)  

                        # print("co_captain =", co_captain)
                        print("co_cap_index =", co_cap_index)


                captain = places[place['id'] - 1]
                cap_index = places_copy.index(captain)
                places_copy.pop(cap_index)

                # print("captain = ", captain)
                # print("cap_index = ", cap_index)

                # print("places after =", places_copy)
            
            i += 1

        print("Co-captains = ", co_captains)

        # step 3
        if max_place:
            day_places.append(max_place)

        captains = day_places.copy()

        # step 4
        c += 1

    ''' creates a dict of days with each day being a key-value pair that contains info about that day including place IDs associated with it
        1. separate each day_place (the locations furthest from each other) into separate days in the list
        2. Go through each place dict to find the closest places to each of those max places, creating zones for each day
        3. Append each of those places to the list of days
        4. FINAL RESULT: Now have a dict called days, which contains a reference to the id of the day 'day-1, etc.' and a list of 
            place ID's that correspond to that day.  
            
            Example structure: 
                days: {
                    "day-1": {
                        id: "day-1",
                        placeIds: [1, 2]
                    },
                    "day-2": {
                        id: "day-2",
                        placeIds: [3]
                    }} '''


    # step 1
    for i in range(duration):
        days[f'day-{i + 1}'] = {
            'id': f'day-{i + 1}',
            'placeIds': []
        } 
        day_order.append(f'day-{i + 1}') 

    for day_num in day_order:
        if len(day_places) > 0:
            local_id = day_places.pop()
            days[day_num]['placeIds'].append(local_id)

            if local_id in co_captains.keys():
                for co_cap in co_captains[local_id]:
                    days[day_num]['placeIds'].append(co_cap)
                    # if len(days[day_num]['placeIds']) < 4:
                    #     days[day_num]['placeIds'].append(co_cap)
                    # else:
                    #     places_copy.append(places_dict[co_cap])
                

            # print("day_place")


    # print(captains)
    
    places_leftover = []

    for place in places_copy:

        min_value = 1000000
        min_place = 0

        # place['place_distances'] is a dict with each of the other locations as keys, and distances to them as values
        for k, v in place['place_distances'].items():
            if k in captains:            # day_places = a list of places that matches the number of days, with each place being the furthest from others in order to create zones the user will visit each day

                if v < min_value:
                    min_value = v
                    min_place = k

        for day_num in day_order:
            d = days[day_num]    # referencing the key of days["day-1"] for example, which is a dict containing key-value pairs that describe the day
            placeIds = d['placeIds']     # a list of integers, which are the local_id 's
            id = placeIds[0]       # first 'local_id' in the list = integer

            if min_place == id:      
                d['placeIds'].append(place['id'])

            # if min_place == id:
            #     if len(d['placeIds']) < 4:      
            #         d['placeIds'].append(place['id'])
            #     else:
            #         places_leftover.append(place['id'])

    # if places_leftover:


    return {
        "days": days,
        "day_order": day_order
    }

def add_places(trip_id, places_last, places_serial):
    # trip_id = request.json['tripID']
    # places_last = request.json['placesLast']
    # places = request.json['places_serial']

    for i in range(places_last):
        place = places_serial[i + 1] 

        local_id = place['id']
        place_name = place['placeName']
        geoapify_placeId = place['placeId']
        place_address = place['address']
        place_img = place['imgURL']
        category = place['category']
        favorite = place['favorite']
        info = place['info']
        lat = place['lat']
        long = place['long']
        

        place = Place(local_id, place_name, geoapify_placeId, place_address, place_img, 
                      info, favorite, category, lat, long, trip_id)

        db.session.add(place)
        db.session.commit()

