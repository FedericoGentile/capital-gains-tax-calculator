import pandas as pd
from datetime import datetime
# Data provided by the user
data = {
    "Date": ["01/09/2023", "02/10/2023", "03/11/2023", "02/12/2023", "02/01/2024", "01/02/2024",
             "01/03/2024", "02/04/2024", "02/05/2024", "03/06/2024", "01/07/2024", "01/08/2024",
             "01/09/2024", "15/09/2024", "15/10/2024"],
    "Price": [78.85, 77.04, 75.60, 79.79, 82.15, 84.99, 88.59, 90.63, 88.87, 91.82, 94.32, 95.27, 95.55, 94.70, 99.76],
    "Units": [3.152, 3.225, 13.207, 12.514, 12.154, 11.749, 11.271, 11.017, 11.236, 10.875, 10.586, 10.481, 10.450, 10.544, 10.009]
}

# Creating DataFrame
df_purchase = pd.DataFrame(data)
df_purchase['Date'] = pd.to_datetime(df_purchase['Date'], format='%d/%m/%Y')

df_balance = df_purchase.copy()
print("Ooriginal Balance:")
print(df_balance,"\n")

df_sales = pd.DataFrame({'Date':[datetime(2024,10,16), datetime(2024,10,17)],
                         'Units': [100, 40],
                         "Price": [120, 100]})
df_sales['Value'] = df_sales['Units']*df_sales['Price']

sales_infos = []
for i, row_s in df_sales.iterrows():

  # Select purchases until sale date
  df_balance_temp = df_balance[df_balance['Date']<=df_sales['Date'].iloc[-1]].sort_values("Units")

  # Check if units can be sold:
  if row_s['Units'] <= df_balance_temp['Units'].sum():

    # Calculate average purchasing price
    average_purchase_price = (df_balance_temp['Units']*df_balance_temp['Price']).sum()/df_balance_temp['Units'].sum()
    print(f"Average Purchase Price: {average_purchase_price}")

    sold_value = row_s['Value']
    average_purchase_value = row_s['Units'] * average_purchase_price
    profit = round((sold_value - average_purchase_value),2)
    taxes = 0
    if profit > 0:
      taxes = round(profit * 0.275,2)
    net_profit = profit - taxes
    print(f"Sold {row_s['Units']} units for a value of {sold_value}. The {row_s['Units']} units where purchased at averaged price of {round(average_purchase_price,2)}, which means their average value is {round(average_purchase_value, 2)}")
    print(f"Gross Profit: {round(profit,2)} ({round(sold_value,2)} - {round(average_purchase_value,2)})")
    print(f"Taxes: {taxes}\n")
    sales_infos.append({'Gross Profit':profit, 'Taxes':taxes, 'Net Profit':net_profit, 'Average Purchase Price':round(average_purchase_price,2)})

    # Update balance
    tot_units_sold = 0
    remaining_units_to_sell = row_s['Units'] # target
    units_to_sell_avg = row_s['Units'] / df_balance_temp.shape[0]
    flag = False
    k = 1
    for j, row_b in df_balance_temp.iterrows():

      units_diff = row_b['Units'] - units_to_sell_avg
      if units_diff <0:
        n = df_balance_temp.shape[0] - k
        units_to_sell_avg += abs(units_diff) / n
        units_to_sell = row_b['Units']
        tot_units_sold += units_to_sell
      else:
        units_to_sell = units_to_sell_avg
        tot_units_sold += units_to_sell
      
      df_balance.loc[j, 'Units'] -= units_to_sell
      remaining_units_to_sell = row_s['Units'] - tot_units_sold

      # Update counter
      k += 1

    df_balance = df_balance[df_balance['Units']>0].reset_index(drop=True)

    # Check if sold units match target:
    if round(row_s['Units']) == round(tot_units_sold):
      print("Updated Balance:")
      print(df_balance)
    else:
      raise Exception(f"Sold units ({round(tot_units_sold)}) != target ({round(row_s['Units'])})")
    print('-----------------------------------------------------------------------')
  else:
    raise Exception(f"Too many units to be sold! {row_s['Units']} > {df_balance_temp['Units'].sum()}")

# Add sales additional infos
df_sales['Gross Profit'] = [x['Gross Profit'] for x in sales_infos]
df_sales['Net Profit'] = [x['Net Profit'] for x in sales_infos]
df_sales['Taxes'] = [x['Taxes'] for x in sales_infos]
df_sales['Average Purchase Price'] = [x['Average Purchase Price'] for x in sales_infos]

df_sales
