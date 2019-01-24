import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# daily exchange rate
# https://open.canada.ca/data/en/dataset/1bc25b1e-0e02-4a5e-afd7-7b96d6728aac

# Load the CSV file
rates = pd.read_csv('https://lemay.ai/forex/10100008.csv')

# Decide what columns we want
rates_cols = ['REF_DATE', 'VALUE']

# Only keep the closing spot price for our currency pair
rates = rates[rates['Type of currency'] == 'United States dollar, closing spot rate']

# Dump the columns we don't need, and fill null values with 0s
rates = rates[rates_cols].fillna(0)

# Force a common index with the economic data we will be getting next
rates.index = pd.to_datetime(rates['REF_DATE'])

# Now that we set the index, drop the extra date column
rates.drop(['REF_DATE'], axis=1, inplace=True)

# Let's give our asset a nice human-friendly name: USD_CAD
rates.rename(columns={'VALUE': 'USD_CAD'}, inplace=True)

# If rate is on a weekend or day market is closed, then use the most recent day's rate
# Weekends are 2 days long so copy Saturday stuff to Sundays
# Carry forward the rates for 3 day and 4 day market closures
while rates[rates == 0].count(axis=0)['USD_CAD']/len(rates.index) > 0:
  print("Shifting rates. Days with rate at 0 = %", rates[rates == 0].count(axis=0)['USD_CAD']/len(rates.index))
  rates['yesterday'] = rates['USD_CAD'].shift(1)
  rates['USD_CAD'] = np.where(rates['USD_CAD'] == 0, rates['yesterday'], rates['USD_CAD'])

#Verify we don't have days with rates at 0
print("Days with rate at 0 = %", rates[rates == 0].count(axis=0)['USD_CAD']/len(rates.index))

# Spot check the results against a trading days calendar: http://www.swingtradesystems.com/trading-days-calendars.html
# Graph the data
rates.drop(['yesterday'], axis=1, inplace=True)
rates.plot()
plt.show()
rates.tail()
