import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


connection = sqlite3.connect('../data/data_saved.sqlite')

cancer_rates_df = pd.read_sql("SELECT * FROM cancer_rates", connection)
aqi_df = pd.read_sql("SELECT * FROM aqi", connection)

connection.close()

# Visualize cancer_rates data
plt.figure(figsize=(10, 6))
for state in cancer_rates_df['State'].unique():
    state_data = cancer_rates_df[cancer_rates_df['State'] == state]
    plt.plot(state_data['Year'], state_data['Crude Rate'], label=state)
plt.title('Cancer Rates over time by State')
plt.xlabel('Year')
plt.ylabel('Crude Rate (per 100.000)')
plt.legend(title='State', loc='upper left', bbox_to_anchor=(0, 0.5))
plt.savefig('./images/cancer_rates.png')



aqi_df= aqi_df.rename(columns={"('good_days_percentage', 'mean')": 'good_days_percentage', "('moderate_days_percentage', 'mean')": 'moderate_days_percentage', "('unhealthy_sensitive_days_percentage', 'mean')": 'unhealthy_sensitive_days_percentage', "('unhealthy_days_percentage', 'mean')": 'unhealthy_days_percentage', "('very_unhealthy_days_percentage', 'mean')": 'very_unhealthy_days_percentage', "('hazardous_days_percentage', 'mean')": 'hazardous_days_percentage', "('Max AQI', 'median')": 'Max AQI', "('Year', 'min')": 'Year', "('State', '')": 'State'})

categories = ['good_days_percentage', 'moderate_days_percentage', 'unhealthy_sensitive_days_percentage', 'unhealthy_days_percentage', 'very_unhealthy_days_percentage', 'hazardous_days_percentage']
colors = ['green', 'yellow', 'orange', 'red', 'purple', 'maroon']

# visulize aqi data and cancer rates for each state
for state in aqi_df['State'].unique():
    filtered_aqi_df = aqi_df[aqi_df["State"] == state].sort_values(by='Year')
    filtered_cancer_df = cancer_rates_df[cancer_rates_df["State"] == state].sort_values(by='Year')

    df = pd.merge(filtered_aqi_df, filtered_cancer_df, on=['State', 'Year'])

    x_axis = np.arange(len(df['Year']))

    fig, ax1 = plt.subplots()

    # Plot stacked bar chart
    bottom_values = np.zeros(len(df['Year']))
    for i, col in enumerate(categories):
        ax1.bar(x_axis, df[col], bottom=bottom_values, color=colors[i], label=col, alpha=0.7)
        bottom_values += df[col]  # Update bottoms for stacking

    ax1.set_xticks(x_axis)
    ax1.set_xticklabels(df['Year'], rotation=90)
    # ax1.set_xlabel('Percentage')
    ax1.set_ylabel('Percentage of each AQI category')
    plt.title(f'Percentage of AQI categories and cancer rate over time in {state}')
    # ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Plot line chart
    ax2 = ax1.twinx()
    ax2.set_ylim(410, 700)
    ax2.plot(x_axis, df['Crude Rate'], color='blue', marker='o', label='Cancer Rate')
    ax2.set_ylabel('Cancer Rate')
    # ax2.legend(loc='upper left', bbox_to_anchor=(0, 0))

    plt.savefig(f'./images/aqi_stacked_bar_cancer_{state}.png')



# mean of the years per state
summary_aqi = aqi_df.groupby('State').agg({
    'good_days_percentage': 'mean',
    'moderate_days_percentage': 'mean',
    'unhealthy_sensitive_days_percentage': 'mean',
    'unhealthy_days_percentage': 'mean',
    'very_unhealthy_days_percentage': 'mean',
    'hazardous_days_percentage': 'mean'
}).reset_index()

summary_aqi.columns = [col.split(' ')[0] for col in summary_aqi.columns.values]

summary_cancer = cancer_rates_df.groupby('State').agg({
    'Crude Rate': 'mean',
}).reset_index()

summary_cancer = summary_cancer.sort_values('Crude Rate')

summary = pd.merge(summary_cancer, summary_aqi, on='State')

# Plot the summary
x_axis = np.arange(len(summary['State']))

fig, ax1 = plt.subplots()

# Plot stacked bar chart
bottom_values = np.zeros(len(summary['State']))
for i, col in enumerate(categories):
    ax1.bar(x_axis, summary[col], bottom=bottom_values, color=colors[i], label=col, alpha=0.7)
    bottom_values += summary[col]  # Update bottoms for stacking

ax1.set_xticks(x_axis)
ax1.set_xticklabels(summary['State'])
# ax1.set_xlabel('Percentage')
ax1.set_ylabel('Percentage of each AQI category (mean of all years)')
plt.title(f'AQI Categories percentage and cancer rate (mean of all year)')
ax1.legend(loc='lower right', bbox_to_anchor=(1, 0.09))

# Plot line chart
ax2 = ax1.twinx()
ax2.set_ylim(410, 700)
ax2.plot(x_axis, summary['Crude Rate'], color='blue', marker='o', label='Cancer Rate')
ax2.set_ylabel('Cancer Rate per 100.000 (mean of all years)')
ax2.legend(loc='lower right', bbox_to_anchor=(1, 0))

plt.savefig('./images/year_summary.png')





aqi_df= aqi_df.rename(columns={'good_days_percentage': 'good', 'moderate_days_percentage': 'moderate', 'unhealthy_sensitive_days_percentage': 'unhealthy_sensitive', 'unhealthy_days_percentage': 'unhealthy', 'very_unhealthy_days_percentage': 'very_unhealthy', 'hazardous_days_percentage': 'hazardous'})
aqi_df = aqi_df.drop("Max AQI", axis=1)
aqi_df = aqi_df.drop("('Max AQI', 'max')", axis=1)


# compute correlation of summary
summary_corr = summary.drop(summary.columns[0], axis=1)
# correlation_matrix = summary_corr.corr(method='pearson')
# print(correlation_matrix)
correlation_matrix = summary_corr.corr(method='spearman')

plt.figure(figsize=(10, 6))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar()

labels = correlation_matrix.columns
plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
plt.yticks(range(len(labels)), labels)

plt.savefig(f'./images/correlation_matrix.png')


# compute correlation of values over time
all_data = pd.merge(aqi_df, cancer_rates_df, on=['State', 'Year']).sort_values(by='Year').sort_values(by='State')
# drop column year and state
all_data_corr = all_data.drop(all_data.columns[0], axis=1)
all_data_corr = all_data_corr.drop("Year", axis=1)
# correlation_matrix = all_data_corr.corr(method='pearson')
# print(correlation_matrix)
correlation_matrix = all_data_corr.corr(method='spearman')

plt.figure(figsize=(10, 6))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar()

labels = correlation_matrix.columns
plt.xticks(range(len(labels)), labels, rotation=20, ha='right')
plt.yticks(range(len(labels)), labels)

plt.savefig(f'./images/correlation_matrix2.png')
