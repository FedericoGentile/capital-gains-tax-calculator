
# Financial Sales Processing Script

## Overview

This code processes sales transactions and calculates profits and taxes based on different inventory accounting methods, such as **ACB (Average Cost Basis)**, **FIFO (First In First Out)**, **LIFO (Last In First Out)**, and **HIFO (Highest In First Out)**. The process involves tracking the balance of purchased inventory, determining the cost basis of items sold, and updating the sales dataframe with profit and tax information.

## Requirements

### Input DataFrames:
1. **`df_purchase`**: A DataFrame representing the purchase transactions, including columns like:
    - `Date`: The date of purchase.
    - `Units`: The number of units purchased.
    - `Price`: The price per unit of the purchase.

2. **`df_sales_orig`**: A DataFrame representing sales transactions, including columns like:
    - `Date`: The date of sale.
    - `Units`: The number of units sold.
    - `Price`: The price per unit for the sale.

3. **Method**: A string variable `METHOD` which determines which inventory valuation method is used. Supported methods are:
    - `"ACB"`: Average Cost Basis
    - `"FIFO"`: First In, First Out
    - `"LIFO"`: Last In, First Out
    - `"HIFO"`: Highest In, First Out

4. **Tax Calculators**:
   - `tax_calculator_ACB()`: A function that calculates the capital gain and taxes using the **ACB** method.
   - `tax_calculator_XYFO()`: A function that calculates the capital gain and taxes using **FIFO**, **LIFO**, or **HIFO** methods.

5. **VERBOSE**: A Boolean variable to control the display of debug and progress information.

## Workflow

### 1. Balance Setup:
- The code starts by making copies of the input purchase and sales dataframes. The purchases DataFrame is copied to `df_balance`, which will be used to track the balance of the inventory after each sale.

### 2. Sales Loop:
- For each row in the sales DataFrame (`df_sales`), the code performs the following steps:
  - **Filter Balance by Date**: Only consider purchases made before or on the sale date to calculate the cost basis for sold units.
  - **Unit Availability Check**: Ensure that the units available for sale are sufficient. If the number of units to be sold exceeds available units in the balance, an exception is raised.

### 3. Calculation Methods:
- Depending on the value of the `METHOD` variable, the code applies different inventory accounting methods:

#### a. **Average Cost Basis (ACB)**:
  - The filtered balance is sorted by units.
  - The average purchase price is calculated by weighting the units and prices.
  - Capital gains and taxes are calculated using the `tax_calculator_ACB()` function.
  - The balance is updated to reflect the units sold.

#### b. **FIFO, LIFO, HIFO**:
  - The filtered balance is sorted based on the selected method:
    - **FIFO**: Sorted by `Date` in ascending order.
    - **LIFO**: Sorted by `Date` in descending order.
    - **HIFO**: Sorted by `Price` in descending order.
  - Capital gains, taxes, and updated balance are calculated using the `tax_calculator_XYFO()` function.

### 4. Error Handling:
- The code raises exceptions for:
  - **Excess Sales**: If there aren't enough units in the balance to fulfill a sale.
  - **Mismatched Units**: If the total number of units sold doesn't match the units specified in the sales DataFrame.

### 5. Updating Sales DataFrame:
- After each sale, the code adds profit and tax information to a list (`sales_infos`). At the end of the loop, this data is joined to the original sales DataFrame (`df_sales`).

## Example Data Structure

### Purchases (`df_purchase`)
| Date       | Units | Price |
|------------|-------|-------|
| 2023-01-01 | 100   | 10.00 |
| 2023-01-15 | 50    | 12.00 |
| 2023-02-01 | 200   | 11.00 |

### Sales (`df_sales_orig`)
| Date       | Units | Price |
|------------|-------|-------|
| 2023-02-15 | 120   | 15.00 |
| 2023-03-01 | 100   | 16.00 |

### Sales After Enrichment (`df_sales`)
| Date       | Units | Price | Capital Gain | Taxes | Net Profit | Average Purchase Price |
|------------|-------|-------|--------------|-------|------------|------------------------|
| 2023-02-15 | 120   | 15.00 | 450.00       | 100.00| 350.00     | 11.25                  |
| 2023-03-01 | 100   | 16.00 | 600.00       | 120.00| 480.00     | 10.50                  |

## Key Functions

### `tax_calculator_ACB(selling_units, selling_price, average_purchase_price)`
Calculates the capital gain and taxes based on the ACB method.

- **Parameters**:
  - `selling_units`: The number of units sold.
  - `selling_price`: The sale price per unit.
  - `average_purchase_price`: The average price per unit based on prior purchases.

- **Returns**:
  - `capital_gain`: The calculated capital gain.
  - `taxes`: The calculated taxes on the capital gain.

### `tax_calculator_XYFO(selling_units, df_balance, df_balance_temp)`
Calculates the capital gain and taxes based on **FIFO**, **LIFO**, or **HIFO** methods.

- **Parameters**:
  - `selling_units`: The number of units sold.
  - `df_balance`: The current balance of purchases.
  - `df_balance_temp`: The balance filtered by the sale date and sorted by the chosen method.

- **Returns**:
  - `capital_gain`: The calculated capital gain.
  - `taxes`: The calculated taxes on the capital gain.
  - `df_balance`: The updated balance after the sale.
  - `tot_units_sold`: Total units sold in the transaction.

### `upload_balance(df_balance, df_balance_temp, units_sold)`
Updates the balance after a sale, reducing the units available.

- **Parameters**:
  - `df_balance`: The current balance.
  - `df_balance_temp`: The filtered and sorted balance based on the sale.
  - `units_sold`: The number of units sold in the transaction.

- **Returns**:
  - Updated `df_balance`.
  - Total units sold in the transaction.

## Configuration

- **`METHOD`**: Set this variable to `"ACB"`, `"FIFO"`, `"LIFO"`, or `"HIFO"` based on the desired inventory accounting method.
- **`VERBOSE`**: Set this variable to `True` for detailed output during execution, or `False` for silent execution.

## Exceptions

- **Units Exceeded**: If the sale attempts to sell more units than are available in the balance.
- **Mismatched Units**: If the number of units sold doesn't match the number specified in the sale.

## Usage

Ensure the input DataFrames are properly structured as shown, and define the `METHOD` and `VERBOSE` variables before running the script. The output will be an enriched sales DataFrame containing profit and tax information.
