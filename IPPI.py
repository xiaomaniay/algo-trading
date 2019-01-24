import pandas as pd
import matplotlib.pyplot as plt

# Industrial Product Price Index (IPPI) data
# https://open.canada.ca/data/en/dataset/39a39c7c-24f1-4789-8f20-a04bcbf635b0

# Load the CSV file
df = pd.read_csv('https://lemay.ai/forex/18100030.csv')

# Decide what columns we want
categories = list(df[list(df)[3]].drop_duplicates())
df_cols = ['REF_DATE', 'North American Product Classification System (NAPCS)', 'VALUE']

# Prepare an empty dataframe to fill with properly indexed economic data
new_df = pd.DataFrame(columns=df_cols)
# Toss out the columns we don't want
df = df[df_cols]
# Set the date as the index using the same format as the USD_CAD data
df.index = df['REF_DATE']
new_df.index = new_df['REF_DATE']
# Dump out the date column now that we applied it to the dataframe index
df.drop(['REF_DATE'], axis=1, inplace=True)
new_df.drop(['REF_DATE'], axis=1, inplace=True)
# Spot check the dataframe so far
print(df.head())

# Loop through the economic indicators and put each one in a dedicated column
for cat in categories:
    # Data can have problems, and not all indicators will make it through
    try:
        temp = df[df[list(df)[0]] == cat]['VALUE']
        new_df[cat] = df[df[list(df)[0]] == cat]['VALUE']
    except Exception as e:
        print("failed on", cat, e)

# Spot check the output dataframe
print(new_df.head())

# Graph the data
new_df.plot()
plt.show()

# Save the dataframe with the economic indicators to a file
new_df.to_csv("forex_signals.csv")