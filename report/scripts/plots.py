import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import seaborn as sns
from matplotlib.colors import LogNorm


def configure_axes(ax, remove_spines=True):
    if remove_spines:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


def format_date_ticks(ax, date_tick):
    xticks = ax.xaxis.get_major_ticks()
    for j, tick in enumerate(xticks):
        if j % date_tick != 0:
            tick.label1.set_visible(False)


def plot_num_recorded_files_per_buggs(data_processor, bugg_id_list, site_list, date_range, plot_width=10, date_tick=7):
    N_plot = len(bugg_id_list)
    fig, ax = plt.subplots(N_plot, 1, figsize=(plot_width, 1.8 * N_plot), sharex=True)
    fig.supylabel("Number of recorded files \n")
    date_counts_total = pd.Series(0, dtype=int)

    for i, bugg_id in enumerate(bugg_id_list):
        ax[i].set_title(f"{site_list[i]} - Bugg {bugg_id}")
        date_counts = data_processor.get_date_counts_for_device(bugg_id, date_range)
        
        date_counts.plot(kind='bar', ax=ax[i], width=0.7)
        ax[i].axhline(y=288, color='g', linewidth=0.5)
        ax[i].set_ylim([0, 320])
        configure_axes(ax[i])
        format_date_ticks(ax[i], date_tick)
        date_counts_total = date_counts_total.add(date_counts, fill_value=0)

    plt.tight_layout()
    return date_counts_total


def plot_number_detections_per_species(data_processor, plot_width=10):
    counts = data_processor.get_species_counts()
    n_species = len(counts)
    mid = n_species // 2
    
    fig, axes = plt.subplots(1, 2, figsize=(plot_width - 4, int(n_species / 18)), sharex=True)
    
    for i, data in enumerate([counts.iloc[:mid], counts.iloc[mid:]]):
        axes[i].barh(data.index, data.values)
        axes[i].set_xscale('log')
        axes[i].invert_yaxis()
        axes[i].set_ylabel("")
        axes[i].xaxis.grid(True)
        axes[i].set_xlabel("Number of detections (logarithmic scale)")
        
        if i == 0:
            axes[i].set_title("Detections per species")
    
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    axes[1].xaxis.set_major_formatter(formatter)
    plt.tight_layout()


def plot_daily_trends(data_processor, occurrence_threshold, plot_width=10, cluster_name=""):
    grouped_df = data_processor.filter_species_by_occurrence(occurrence_threshold, use_daily=False)
    species_order = grouped_df.sum().sort_values(ascending=False).index.tolist()
    grouped_df = grouped_df[species_order]
    
    n_species = grouped_df.shape[1]
    fig, ax = plt.subplots(figsize=(plot_width, 1.5 + n_species/7))
    
    sns.heatmap(grouped_df.T, norm=LogNorm(), cmap=sns.cm.rocket_r, 
                cbar_kws={"shrink": 0.5}, linewidth=.5)
    ax.set_title(f"Daily trend: Number of detections per species per hour - {cluster_name}", y=1.002)
    ax.set_ylabel("")
    ax.set_xlabel("Time (UTC)")
    plt.tight_layout()


def create_temporal_heatmap(ax, grouped_df, date_tick, vmax=None):
    norm = LogNorm(vmin=1, vmax=vmax) if vmax else LogNorm()
    sns.heatmap(grouped_df.T, norm=norm, cmap=sns.cm.rocket_r, 
                cbar_kws={"shrink": 0.6, 'orientation': 'horizontal', "pad": 5/grouped_df.shape[1]}, 
                linewidth=0, ax=ax)
    
    for i in range(grouped_df.shape[1] + 1):
        ax.axhline(i, color='white', lw=1)
    
    ax.set_ylabel("")
    ax.set_xlabel("")
    format_date_ticks(ax, date_tick)


def plot_daily_trends_full(data_processor, occurrence_threshold, date_range, date_counts_total, 
                          plot_width=10, cluster_name="", date_tick=7):
    grouped_df = data_processor.filter_species_by_occurrence(occurrence_threshold, use_daily=True)
    species_order = grouped_df.sum().sort_values(ascending=False).index.tolist()
    grouped_df = grouped_df[species_order].reindex(date_range, fill_value=0)
    
    n_species = grouped_df.shape[1]
    N_devices = len(data_processor.index_df['device'].unique())
    height1, height2 = 0.4, 3 + n_species/7
    
    fig, ax = plt.subplots(2, 1, figsize=(plot_width, height1 + height2), 
                          gridspec_kw={'height_ratios': [height1, height2]})
    fig.suptitle(f"Temporal trend: Number of detections per species per day - {cluster_name}", y=1.002)
    
    date_counts_total = date_counts_total.reindex(date_range, fill_value=0)
    date_counts_total.plot(kind='bar', ax=ax[0], width=0.7, color="lightgrey")
    n_files_max = 288 * N_devices
    ax[0].axhline(y=n_files_max, color='darkgrey', linewidth=0.5)
    ax[0].set_ylim([0, n_files_max * 1.1])
    configure_axes(ax[0])
    ax[0].get_xaxis().set_visible(False)
    ax[0].set_ylabel("Num. of recordings", rotation=0, labelpad=40)
    
    create_temporal_heatmap(ax[1], grouped_df, date_tick)
    fig.text(0.2, 0.13, "Number of detections", verticalalignment='bottom', horizontalalignment='left')
    plt.tight_layout()


def plot_daily_trends_full_per_device(data_processor, bugg_id_list, occurrence_threshold, date_range, 
                                     date_tick, plot_width=5, cluster_name="", site_list=[]):
    base_vmax = data_processor.get_daily_grouped().to_numpy().max()
    
    for i, bugg_id in enumerate(bugg_id_list):
        device_predictions = data_processor.get_predictions_for_device(bugg_id)
        if device_predictions.empty:
            continue
            
        device_grouped = device_predictions.groupby(['date', 'species_with_status']).size().unstack(fill_value=0)
        device_grouped = device_grouped.sort_index()
        species_order = device_grouped.sum().sort_values(ascending=False).index.tolist()
        device_grouped = device_grouped[species_order].reindex(date_range, fill_value=0)
        
        n_species = device_grouped.shape[1]
        height1, height2 = 0.4, 3 + n_species/7
        
        fig, ax = plt.subplots(2, 1, figsize=(plot_width, height1 + height2), 
                              gridspec_kw={'height_ratios': [height1, height2]})
        fig.suptitle(f"Temporal trend: {cluster_name} - {site_list[i]} - Bugg {bugg_id}", y=1.001)
        
        date_counts = data_processor.get_date_counts_for_device(bugg_id, date_range)
        date_counts.plot(kind='bar', ax=ax[0], width=0.7, color="lightgrey")
        ax[0].axhline(y=288, color='darkgrey', linewidth=0.5)
        ax[0].set_ylim([0, 288 * 1.1])
        configure_axes(ax[0])
        ax[0].get_xaxis().set_visible(False)
        ax[0].set_ylabel("Num. of recordings", rotation=0, labelpad=40)
        
        create_temporal_heatmap(ax[1], device_grouped, date_tick, base_vmax)
        fig.text(0.2, 0.13, "Number of detections", verticalalignment='bottom', horizontalalignment='left')
        plt.tight_layout()