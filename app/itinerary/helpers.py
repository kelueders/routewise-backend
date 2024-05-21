# EXTERNAL
from scipy.spatial import distance
import numpy as np

# INTERNAL
from app.models import Place, db

'''
Takes a list of Place objects and a trip duration and returns a dictionary of days that contains 
all the information needed for that day: such as all the trips associated with it

places - dict type
places_copy - dict type
'''
def create_itinerary(serialized_places, duration):

    days = {}
    day_order = []    # [day-1, day-2, day-3, ...]
    for i in range(duration):
        days[f'day-{i + 1}'] = {
            'id': f'day-{i + 1}',
            'placeIds': []
        } 
        day_order.append(f'day-{i + 1}') 

    # if only one place given - create days dict and day_order list, then return simply itinerary
    if len(serialized_places) < 2:

        days['day-1']['placeIds'] = [1]

        return {
            "days": days,
            "day_order": day_order
        }

    # create a list just containing the coordinates to be used to create the matrix of all the distances
    coords = []
    for place in serialized_places.values():

        coord = (place['lat'], place['long'])
        coords.append(coord)

    # creates a matrix of all the distances between each point and every other point
    all_dist = distance.cdist(coords, coords, 'euclidean')

    serialized_places_copy = serialized_places.copy()    # creates a copy of the places dict to be manipulated without altering the original
    dist_range = 0

    places_list = list(serialized_places_copy.values())

    # creates a key within the places_copy dict that holds a dict containing the distances to each of the other locations
    i = 0
    for place in places_list:

        j = 0
        place['place_distances'] = {}
        
        for d in all_dist[i]:
            # if d != 0.0: # if there are duplicates of the same place in the places list this breaks the code
            place['place_distances'][places_list[j]['local_id']] = d
            dist_range = max(d, dist_range)
                
            j += 1
        
        # creates a key within places_copy that holds the sum of distances calculated above
        place['sum_dist'] = sum(all_dist[i])
        i += 1

    # The chosen range is 15% when comparing locations to eachother
    threshold_range = 0.15 * dist_range

    for day_num in day_order:        

        max_distance = 0
        max_place_id = ''

        # step 1
        for place in places_list:

            if max_distance < place['sum_dist']: 
                max_distance = place['sum_dist']
                max_place_id = place['local_id']  


        if max_place_id: # there won't be an id if there are no more places left in places_list

            # step 1b - add captain's place id to the current day 
            captain_id = max_place_id
            days[day_num]['placeIds'] = [captain_id]     # in brackets because we're putting the captain_id into an array before putting it in the placesIds key
            # serialized_places[captain_id]['in_itinerary'] = True

            captain_dict = list(filter(lambda x : True if x['local_id'] == captain_id else False, places_list ))

            # step 1c - remove captain place object from places_list
            place_index = places_list.index(captain_dict[0])
            places_list.pop(place_index)

            # step 2 - find co-captains of the selected captain (places that are within 15% range distance of the selected captain place)
            sorted_places_copy = sorted(places_list, key=lambda x: x['place_distances'][captain_id]) # sorted by distance 


            for place in sorted_places_copy:

                if len(days[day_num]['placeIds']) < 4: # caps day places at 4

                    if place['place_distances'][captain_id] < threshold_range:
                        days[day_num]['placeIds'].append(place['local_id'])
                        # serialized_places[place['local_id']]['in_itinerary'] = True

                        places_list = list(filter(lambda x : True if x['local_id'] != place['local_id'] else False, places_list ))


    # create saved_places list to hold places not in the itinerary
    saved_places = [] 

    # loop thru the remaining places in places_list
    # for place in places_copy.values():
    for place in places_list:

        # create closest_captain_id and closest_day_num "day-2"
        closest_captain_id = ""
        closest_day_num = ""

        # loop thru the day_order
        for day_num in day_order:

            # only executes if that day has less than four places assigned to it
            if len(days[day_num]['placeIds']) < 4:

                # current day captain id
                captain_id = days[day_num]['placeIds'][0]

                if closest_captain_id:
                    # comparing this place's distance from current day captain to current closest captain
                    # trying to ultimately find the day whose captain is the closest to it
                    if place['place_distances'][captain_id] < place['place_distances'][closest_captain_id]:
                        closest_captain_id = captain_id
                        closest_day_num = day_num
                else:
                    # if closest_captain_id hasn't been assigned yet we assign it
                    closest_captain_id = captain_id
                    closest_day_num = day_num

        # after resolving the closest day_num, add this place to the closest day_num
        if closest_day_num: # if closest day_num is falsey, all of the days are full

            days[closest_day_num]['placeIds'].append(place['local_id'])
            # serialized_places[place['local_id']]['in_itinerary'] = True

        else:

            # add the place id to list 'saved_places'
            saved_places.append(place['local_id'])


    # saved_places = list(filter(lambda x : True if x['local_id'] not in remove_list else False, places_list))
    # saved_places = list(filter(lambda x : True if 'in_itinerary' not in x.keys() else False, places_list))

    # saved_places_ids = list(map(lambda x : x['local_id'], saved_places))

    # places_list = list(map(lambda x : x['in_itinerary'] == False, saved_places))


    return {
        "days": days,
        "day_order": day_order,
        "saved_places": saved_places,    # this will be a list of id's
        "serialized_places": serialized_places
    }

def add_places(trip_id, places_last, places_arr):


    for i in range(places_last):

        if type(places_arr) == dict:
            place = places_arr[i + 1]
            
            local_id = place['local_id']
            place_name = place['placeName']
            geoapify_placeId = place['placeId']
            place_address = place['address']
            place_img = place['imgURL']
            category = place['category']
            favorite = place['favorite']
            info = place['info']
            lat = place['lat']
            long = place['long']   

        elif type(places_arr) == list:
            place = places_arr[i]

            local_id = place['id']
            place_name = place['placeName']
            geoapify_placeId = place['place_id']
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

