import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ..models import Place, Trip

class Itinerary:

    def __init__(self, trip_id):
        self.trip_id = trip_id                  # int - index value from Trip table
        self.places = self.get_places()         # list - of Place objects
        self.duration = self.get_duration()     # int - length of the trip in days

    def get_places(self):
        return Place.query.filter_by(trip_id = self.trip_id).all()
    
    def get_duration(self):
        trip = Trip.query.filter_by(trip_id = self.trip_id).first()
        return trip.duration

    def create_dataframe(self):
        data = {
            'local_id': [],
            'lat': [],
            'long': []
        }

        for place in self.places:
            data['local_id'].append(place.local_id)
            data['lat'].append(place.lat)
            data['long'].append(place.long)

        return pd.DataFrame(data)

    def cluster_analysis(self):
        places_df = self.create_dataframe(self.places)

        lat_long = places_df[['lat', 'long']]

        scaler = StandardScaler()
        lat_long_scaled = scaler.fit_transform(lat_long)
        
        kmeans = KMeans(n_clusters=self.duration, random_state=42)

        kmeans.fit(lat_long_scaled)

        places_df['Day'] = kmeans.labels_

        return places_df
    
    def __repr__(self):
        return f"trip_id: {self.trip_id}\nplaces: {self.places}\nduration: {self.duration} days"
