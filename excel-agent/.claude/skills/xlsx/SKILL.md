---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis. Use when working with Excel files for creating spreadsheets, adding formulas, formatting, or data analysis."
---

# xlsx Skill

## Core Principle: Use Formulas, Not Hardcoded Values

Always use Excel formulas instead of calculating values in Python and hardcoding results.

### Wrong Approach
```python
total = sum(values)
sheet['B10'] = total  # Hardcodes result - won't update if data changes
```

### Correct Approach
```python
sheet['B10'] = '=SUM(B2:B9)'  # Dynamic formula - updates automatically
```

## Color Coding Standards (Financial Models)

Follow industry-standard color conventions for professional spreadsheets:

| Color | Usage | Hex Code |
|-------|-------|----------|
| **Blue text** | Hardcoded inputs (user-changeable values) | `0000FF` |
| **Black text** | Formulas and calculations | `000000` |
| **Green text** | Cross-sheet references/links | `008000` |
| **Red text** | External file links or warnings | `FF0000` |
| **Yellow background** | Headers or key assumptions | `FFFF00` |
| **Light gray background** | Subtotals or summary rows | `D3D3D3` |

## Number Formatting

Use appropriate number formats for data types:

| Data Type | Format String | Example Output |
|-----------|---------------|----------------|
| Currency | `$#,##0.00` | $1,234.56 |
| Currency (negative in parens) | `$#,##0.00;($#,##0.00)` | ($1,234.56) |
| Percentage | `0.0%` | 12.5% |
| Number with commas | `#,##0` | 1,234 |
| Decimal | `0.00` | 12.34 |
| Date | `YYYY-MM-DD` | 2024-01-15 |
| Accounting | `_($* #,##0.00_)` | $ 1,234.56 |

## Common Excel Formulas

### Basic Aggregation
- `=SUM(A1:A10)` - Sum of values
- `=AVERAGE(A1:A10)` - Average of values
- `=COUNT(A1:A10)` - Count of numeric cells
- `=COUNTA(A1:A10)` - Count of non-empty cells
- `=MIN(A1:A10)` / `=MAX(A1:A10)` - Minimum/Maximum

### Conditional Logic
- `=IF(A1>100, "High", "Low")` - Simple condition
- `=IFERROR(A1/B1, 0)` - Handle division errors
- `=IFNA(VLOOKUP(...), "Not Found")` - Handle lookup failures

### Lookup Functions
- `=VLOOKUP(lookup_value, table, col_index, FALSE)` - Vertical lookup
- `=HLOOKUP(lookup_value, table, row_index, FALSE)` - Horizontal lookup
- `=INDEX(range, MATCH(value, lookup_range, 0))` - More flexible lookup
- `=XLOOKUP(lookup, lookup_array, return_array)` - Modern lookup (Excel 365)

### Conditional Aggregation
- `=SUMIF(range, criteria, sum_range)` - Sum with condition
- `=COUNTIF(range, criteria)` - Count with condition
- `=AVERAGEIF(range, criteria, average_range)` - Average with condition
- `=SUMIFS(sum_range, criteria_range1, criteria1, ...)` - Multiple conditions

### Text Functions
- `=CONCATENATE(A1, " ", B1)` or `=A1 & " " & B1` - Join text
- `=LEFT(A1, 5)` / `=RIGHT(A1, 5)` - Extract characters
- `=TRIM(A1)` - Remove extra spaces
- `=UPPER(A1)` / `=LOWER(A1)` / `=PROPER(A1)` - Change case

### Date Functions
- `=TODAY()` - Current date
- `=YEAR(A1)` / `=MONTH(A1)` / `=DAY(A1)` - Extract date parts
- `=DATEDIF(start, end, "d")` - Days between dates
- `=EOMONTH(date, 0)` - End of month

## Spreadsheet Workflow

Follow this workflow for creating professional spreadsheets:

1. **Create Structure**
   - Set up sheet with clear headers
   - Use descriptive column names
   - Leave space for totals/summaries

2. **Add Data**
   - Input raw data in organized rows
   - Use consistent data types per column
   - Mark input cells with blue text

3. **Add Formulas**
   - Use formulas for all calculations
   - Reference cells, never hardcode values
   - Add totals, averages, and summaries

4. **Apply Formatting**
   - Format headers (bold, yellow background, centered)
   - Apply number formats to data columns
   - Use color coding for inputs vs calculations

5. **Verify & Validate**
   - Check for formula errors (#REF!, #DIV/0!, etc.)
   - Verify totals are correct
   - Test with sample data changes

## Common Spreadsheet Templates

### Budget Tracker
- Columns: Date, Category, Type (Income/Expense), Amount, Description
- Formulas: Total Income, Total Expenses, Net Balance
- Format: Currency for amounts, date format for dates

### Sales Report
- Columns: Month, Product, Region, Units, Unit Price, Revenue
- Formulas: Revenue = Units * Price, Totals by product/region
- Format: Currency for revenue/price, number for units

### Employee Directory
- Columns: ID, Name, Department, Title, Salary, Start Date, Email
- Formulas: Average salary, count by department
- Format: Currency for salary, date for start date

## Error Prevention

- Always use `IFERROR()` wrapper for division operations
- Use data validation for input cells
- Lock formula cells to prevent accidental edits
- Use named ranges for frequently referenced data
