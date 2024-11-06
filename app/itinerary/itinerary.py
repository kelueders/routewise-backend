import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

max_visit_time_per_day = 540    # minutes
default_avg_visit_time = 60     # minutes

''' 
Itinerary Class
Sorts places into days to create an itinerary.
The algorithm uses kmeans to cluster places that
    are close (distance wise) to each other, then
    the algorithm goes through clusters and
    re-clusters if the total visit time per day 
    breaches the max duration per day.
The data is stored in a multi-dimensional array 
    with the rows being the days and columns being 
    the placeIds and is ordered by most to least 
    filled days.
'''
class Itinerary:

    def __init__(self, trip_id, places):
        self.trip_id = trip_id                  # int - index value from Trip table
        self.places = places                    # list - Place objects
        self.duration = self.get_duration()     # int - length of the trip in days
        self.sorted_days = []                   # Multi-dimen array - row is day, column is placeId
    
    def get_duration(self):
        return self.places[0].trip.duration
    
    def generate(self):
        # Set number of starting clusters
        n_clusters = self.duration
        if len(self.places) < self.duration:
            n_clusters = len(self.places)

        places_df = self.create_dataframe()
        lat_long = places_df[['lat', 'long']]       # Features for clustering
        scaler = StandardScaler()
        lat_long_scaled = scaler.fit_transform(lat_long)

        # Cluster into the amount of trip days
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(lat_long_scaled)
        places_df['day'] = kmeans.labels_

        # Re-cluster to limit day visit time
        df_refined = self.split_clusters_on_time_limit(places_df)

        # Create sorted_days multi-dimens array with places going into corresponding day
        self.sorted_days = [[] for _ in range(df_refined['day'].max() + 1)]
        for _, row in df_refined.iterrows():
            self.sorted_days[int(row['day'])].append(int(row['position_id']))

        # sort df_refined by day size (descending)
        self.sorted_days.sort(reverse=True, key=len)

        return self.sorted_days
    
    def create_dataframe(self):
        data = {
            'position_id': [],
            'lat': [],
            'long': [],
            'avg_visit_time': []
        }

        for place in self.places:
            data['position_id'].append(place.position_id)
            data['lat'].append(place.lat)
            data['long'].append(place.long)

            # temporarily set average visit time
            if place.avg_visit_time is None:
                data['avg_visit_time'].append(default_avg_visit_time)
            else:
                data['avg_visit_time'].append(place.avg_visit_time)

        return pd.DataFrame(data)

    def split_clusters_on_time_limit(self, df):
        if len(self.places) <= self.duration:
            return df
        
        cluster_days = df.groupby('day').sum()
        for i, day in cluster_days.iterrows():
            total_day_visit_time = day['avg_visit_time']
            if total_day_visit_time > max_visit_time_per_day:
                # Get all places in the overloaded cluster
                overloaded_cluster = df[df['day'] == i]
                
                # Determine how many additional clusters are needed
                n_splits = int((total_day_visit_time // max_visit_time_per_day) + 2)
            
                # Re-cluster the overloaded cluster
                X_overloaded = overloaded_cluster[['lat', 'long']]
                kmeans_overloaded = KMeans(n_clusters=n_splits, random_state=42)
                overloaded_cluster.loc[:, 'new_day'] = kmeans_overloaded.fit_predict(X_overloaded)

                # Adjust day numbers for the new clusters
                num_exisiting_days = df['day'].max()
                overloaded_cluster.loc[:, 'day'] = overloaded_cluster['new_day'] + num_exisiting_days + 1
                
                # Drop the intermediate 'new_day' column
                overloaded_cluster = overloaded_cluster.drop(columns=['new_day'])

                # Update the main dataframe with the new clusters
                df.loc[overloaded_cluster.index, 'day'] = overloaded_cluster['day']
        return df
    
    def __repr__(self):
        return f"trip_id: {self.trip_id}\nplaces: {self.places}\nduration: {self.duration} days"
