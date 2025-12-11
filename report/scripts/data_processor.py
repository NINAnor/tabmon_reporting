import pandas as pd
import numpy as np
from matplotlib.colors import LogNorm


class DataProcessor:
    def __init__(self, predictions_df, index_df):
        self.predictions_df = predictions_df
        self.index_df = index_df
        self._species_counts = None
        self._daily_grouped = None
        self._hourly_grouped = None
    
    def get_species_counts(self):
        if self._species_counts is None:
            self._species_counts = self.predictions_df['species_with_status'].value_counts()
        return self._species_counts
    
    def get_daily_grouped(self):
        if self._daily_grouped is None:
            self._daily_grouped = self.predictions_df.groupby(['date', 'species_with_status']).size().unstack(fill_value=0)
            self._daily_grouped = self._daily_grouped.sort_index()
        return self._daily_grouped
    
    def get_hourly_grouped(self):
        if self._hourly_grouped is None:
            self._hourly_grouped = self.predictions_df.groupby(['time', 'species_with_status']).size().unstack(fill_value=0)
            self._hourly_grouped = self._hourly_grouped.sort_index()
        return self._hourly_grouped
    
    def filter_species_by_occurrence(self, threshold, use_daily=True):
        grouped = self.get_daily_grouped() if use_daily else self.get_hourly_grouped()
        species_filter = grouped.sum() > threshold
        return grouped.loc[:, species_filter]
    
    def get_date_counts_for_device(self, bugg_id, date_range):
        device_filter = self.index_df["device"].str.endswith(bugg_id)
        date_counts = self.index_df['date'][device_filter].value_counts().sort_index()
        return date_counts.reindex(date_range, fill_value=0)
    
    def get_predictions_for_device(self, bugg_id):
        return self.predictions_df[self.predictions_df['device_id'] == bugg_id]