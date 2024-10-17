
# Financial Sales Processing Script

## Overview

This Python script processes sales transactions by calculating the gross and net profits based on previously purchased units at different prices. It ensures that the sales do not exceed the available units, and updates the balance of units after each sale. The script also calculates taxes on profits and provides detailed sales information, including the average purchase price, gross profit, net profit, and taxes.

## Features

- **Purchases Data:** The script processes purchase data, including dates, prices, and units bought.
- **Sales Data:** It handles multiple sales transactions, where each sale consists of units sold at a specific price and date.
- **Profit Calculation:** Calculates gross and net profit for each sale.
  - **Gross Profit:** Difference between sale value and the purchase value of the sold units.
  - **Net Profit:** Gross profit minus taxes (27.5% tax on positive profits).
- **Balance Update:** Updates the remaining units after each sale to track the stock balance.
- **Error Handling:** Ensures that sales do not exceed available units and that sold units match the target quantity.

## Data Structure

### Purchases Data (`df_purchase`)
The initial purchase data is structured as follows:

- `Date`: The date of each purchase (formatted as DD/MM/YYYY).
- `Price`: The price per unit at the time of purchase.
- `Units`: The number of units bought.

Example:
```python
data = {
    "Date": ["01/09/2023", "02/10/2023", ... ],
    "Price": [78.85, 77.04, ... ],
    "Units": [3.152, 3.225, ... ]
}
```

### Sales Data (`df_sales`)
The sales data is structured with the following columns:

- `Date`: The date of each sale (as a `datetime` object).
- `Units`: The number of units sold.
- `Price`: The price per unit at the time of sale.
- `Value`: Calculated as `Units * Price` for each sale.

Example:
```python
df_sales = pd.DataFrame({
    'Date': [datetime(2024,10,16), datetime(2024,10,17)],
    'Units': [100, 40],
    'Price': [120, 100]
})
```

## Logic

1. **Date Formatting:** Converts the `Date` column in purchases data to `datetime` format.
2. **Profit Calculation:** For each sale, the script:
   - Filters the purchase history to only include purchases made on or before the sale date.
   - Calculates the weighted average purchase price of the units being sold.
   - Computes gross profit (`sale value - purchase value`), taxes (27.5% of positive profit), and net profit.
3. **Balance Update:** Reduces the units available in the balance as sales are processed.
4. **Sales Information:** After each sale, detailed profit information (gross profit, net profit, taxes, and average purchase price) is stored and added to the final sales DataFrame.

## Output

The script outputs the updated `df_sales` DataFrame, which includes:

- `Date`: Date of the sale.
- `Units`: Number of units sold.
- `Price`: Price per unit for the sale.
- `Value`: Total value of the sale.
- `Gross Profit`: Profit before taxes.
- `Net Profit`: Profit after taxes.
- `Taxes`: Calculated taxes on the profit.
- `Average Purchase Price`: Average price of the units sold.

Example:
```python
df_sales
```

| Date       | Units | Price | Value | Gross Profit | Net Profit | Taxes | Average Purchase Price |
|------------|-------|-------|-------|--------------|------------|-------|------------------------|
| 2024-10-16 | 100   | 120   | 12000 | 3379.64      | 2449.23    | 930.41| 86.20                  |
| 2024-10-17 | 40    | 100   | 4000  | 171.96       | 124.67     | 47.29 | 95.70                  |

## Exception Handling

- **Insufficient Units:** If a sale exceeds the available stock, the script raises an exception: `Too many units to be sold!`.
- **Mismatch in Sold Units:** If the number of units sold doesn’t match the target, an exception is raised to ensure data integrity: `Sold units != target`.

## Requirements

This script requires the following Python libraries:
- `pandas`
- `datetime`

Install them using:
```bash
pip install pandas
```

## How to Run

1. Copy the script into a Python file.
2. Ensure your purchase and sales data is structured in the same format as shown above.
3. Run the script to see the updated balance and sales information.
