import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def bar_plot(data, x, y, figsize=(10, 7)):
    plt.subplots(figsize=figsize)
    fig = sns.barplot(data=data, x='txn.chargeStationCity', y='Total_amount_charged')
    fig.set_title(f'{y} vs {x}')
    plt.show()

def line_plot(data, x, y, rotation=0, figsize=(10, 7), hue=None):
    plt.subplots(figsize=figsize)
    fig = sns.lineplot(data=data, x='date', y='Total_amount_charged', hue=hue)
    fig.set_xticklabels(labels=data['date'], rotation=rotation)
    fig.set_title(f'{y} vs {x}')
    plt.show()

def plot_amount_vs_energy(data, x, col1, col2, figsize=(10, 7)):
    df_date_vs_amount_watthr_temp = pd.DataFrame(data).set_index(x)

    x = np.arange(len(df_date_vs_amount_watthr_temp.index))
    bar_width = 0.35

    plt.subplots(figsize=figsize)
    plt.bar(x, df_date_vs_amount_watthr_temp[col1], bar_width, label='Amount Charged')
    plt.bar(x + bar_width, df_date_vs_amount_watthr_temp[col2], bar_width, label='Enery used (Wh)')
    plt.xticks(x + bar_width/2, df_date_vs_amount_watthr_temp.index, rotation=75)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.yscale('symlog')
    plt.show()