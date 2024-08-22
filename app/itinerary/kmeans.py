import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

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
            'long': [],
            'avg_duration': []
        }

        for place in self.places:
            data['local_id'].append(place.local_id)
            data['lat'].append(place.lat)
            data['long'].append(place.long)
            data['avg_duration'].append(place.avg_duration)

        return pd.DataFrame(data)

    def refine_clusters_based_on_duration(df, lat_long_dur_scaled, max_duration_per_day=480):
        while True:
            cluster_durations = df.groupby('Day')['duration'].sum()
            if all(cluster_durations <= max_duration_per_day):
                break
            else:
                global optimal_n_clusters
                optimal_n_clusters += 1
                kmeans = KMeans(n_clusters=optimal_n_clusters, random_state=42)
                df['Day'] = kmeans.fit_predict(lat_long_dur_scaled)
        return df

    def cluster_analysis(self):
        places_df = self.create_dataframe(self.places)

        lat_long_dur = places_df[['lat', 'long', 'avg_duration']]

        scaler = StandardScaler()
        lat_long_dur_scaled = scaler.fit_transform(lat_long_dur)

        # Silhouette Analysis to determine optimal number of clusters
        silhouette_avg = []
        range_n_clusters = range(2, 11)  # Start from 2 because silhouette score is not defined for 1 cluster

        for n_clusters in range_n_clusters:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(lat_long_dur_scaled)
            
            # Compute the silhouette score
            score = silhouette_score(lat_long_dur_scaled, cluster_labels)
            silhouette_avg.append(score)
        optimal_n_clusters = range_n_clusters[silhouette_avg.index(max(silhouette_avg))]
        
        kmeans = KMeans(n_clusters=optimal_n_clusters, random_state=42)

        kmeans.fit(lat_long_dur_scaled)

        places_df['Day'] = kmeans.labels_
        df_refined = self.refine_clusters_based_on_duration(places_df)
        return df_refined
    
    def __repr__(self):
        return f"trip_id: {self.trip_id}\nplaces: {self.places}\nduration: {self.duration} days"
