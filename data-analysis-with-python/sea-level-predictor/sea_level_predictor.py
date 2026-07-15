import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'epa-sea-level.csv')
    df = pd.read_csv(csv_path)

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    res = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years_extended = pd.Series(range(1880, 2051))
    ax.plot(years_extended, res.slope * years_extended + res.intercept, 'r')

    # Create second line of best fit
    recent_df = df[df['Year'] >= 2000]
    res_recent = linregress(recent_df['Year'], recent_df['CSIRO Adjusted Sea Level'])
    years_recent_extended = pd.Series(range(2000, 2051))
    ax.plot(years_recent_extended, res_recent.slope * years_recent_extended + res_recent.intercept, 'g')

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()