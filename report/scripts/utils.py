import pandas as pd
import duckdb
import os
from datetime import datetime
from pathlib import Path


def parse_date(date_str):
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ", 
        "%Y-%m-%dT%H:%MZ"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not supported: {date_str}")


def get_file_date(bugg_file_name):
    date_str = bugg_file_name.replace('.mp3', '').replace('_', ':')
    return parse_date(date_str).date()


def get_file_time(bugg_file_name):
    date_str = bugg_file_name.replace('.mp3', '').replace('_', ':')
    return parse_date(date_str).hour


def get_bugg_id(folder_name):
    return folder_name.split('-', 1)[1][1:].lstrip('0')


def load_parquet_batch(file_paths, species_filter=None, confidence_threshold=0.5):
    if not file_paths:
        return pd.DataFrame()
    
    file_paths_str = "', '".join(file_paths)
    query = f"SELECT * FROM read_parquet(['{file_paths_str}'])"
    predictions_df = duckdb.query(query).to_df()
    
    predictions_df = predictions_df[predictions_df["confidence"] > confidence_threshold]
    
    if species_filter:
        predictions_df = predictions_df[~predictions_df["scientific name"].isin(species_filter)]
    
    predictions_df['date'] = predictions_df['filename'].apply(get_file_date)
    predictions_df['time'] = predictions_df['filename'].apply(get_file_time)
    
    return predictions_df


def load_parquet(file_path, species_filter=None, confidence_threshold=0.5):
    return load_parquet_batch([file_path], species_filter, confidence_threshold)


def get_file_paths_for_devices(database_path, device_ids):
    all_files = []
    for device_id in device_ids:
        device_path = database_path / f"device_id={device_id}"
        if device_path.exists():
            files = sorted(device_path.glob("*.parquet"))
            all_files.extend([str(f) for f in files])
    return all_files

def get_file_paths_for_devices(database_path, device_ids):
    all_files = database_path.glob("**/*.parquet")
    all_files = list(all_files)
    current_files = [str(f) for f in all_files if any(f.parts[-2] == f"device_id={device_id}" for device_id in device_ids)]
    return current_files