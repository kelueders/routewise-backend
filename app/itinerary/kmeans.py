import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from ..models import Place, Trip

max_duration_per_day = 480  # minutes

class Itinerary:


    def __init__(self, trip_id):
        self.trip_id = trip_id                  # int - index value from Trip table
        self.places = self.get_places()         # list - of Place objects
        self.duration = self.get_duration()     # int - length of the trip in days
        self.sorted_places = {}

    def get_places(self):
        return Place.query.filter_by(trip_id = self.trip_id).all()
    
    def get_duration(self):
        trip = Trip.query.filter_by(trip_id = self.trip_id).first()
        return trip.duration

    def create_dataframe(self):
        data = {
            'local_id': [],
            'lat': [],
            'long': [],
            'avg_duration': []
        }

        for place in self.places:
            data['local_id'].append(place.local_id)
            data['lat'].append(place.lat)
            data['long'].append(place.long)
            data['avg_duration'].append(place.avg_duration)

        return pd.DataFrame(data)

    def split_clusters_on_duration(df):
        cluster_days = df.groupby('day').sum()
        for i, day in cluster_days.iterrows():
            total_day_duration = day['duration']
            if total_day_duration > max_duration_per_day:
                # Get all places in the overloaded cluster
                overloaded_cluster = df[df['day'] == i]
                
                # Determine how many additional clusters are needed
                n_splits = int((total_day_duration // max_duration_per_day) + 1)
            
                # Re-cluster the overloaded cluster
                X_overloaded = overloaded_cluster[['lat', 'long']]
                kmeans_overloaded = KMeans(n_clusters=n_splits, random_state=42)
                overloaded_cluster.loc[:, 'new_day'] = kmeans_overloaded.fit_predict(X_overloaded)

                # Adjust day numbers for the new clusters
                max_existing_day = df['day'].max()
                overloaded_cluster.loc[:, 'day'] = overloaded_cluster['new_day'] + max_existing_day + 1
                
                # Drop the intermediate 'new_day' column
                overloaded_cluster = overloaded_cluster.drop(columns=['new_day'])

                # Update the main dataframe with the new clusters
                df.loc[overloaded_cluster.index, 'day'] = overloaded_cluster['day']
        return df

    def cluster_analysis(self):
        places_df = self.create_dataframe(self.places)

        lat_long = places_df[['lat', 'long']]
        scaler = StandardScaler()
        lat_long_scaled = scaler.fit_transform(lat_long)
        kmeans = KMeans(n_clusters=self.distance, random_state=42)
        kmeans.fit(lat_long_scaled)
        places_df['Day'] = kmeans.labels_
        df_refined = self.split_clusters_on_duration(places_df)

        self.sorted_places = df_refined.to_dict()
        return self.sorted_places
    
    def __repr__(self):
        return f"trip_id: {self.trip_id}\nplaces: {self.places}\nduration: {self.duration} days"
