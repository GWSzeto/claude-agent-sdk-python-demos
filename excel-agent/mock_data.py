"""Mock data for Excel Agent - Sample datasets for spreadsheet operations."""

from datetime import datetime, timedelta
import random

# =============================================================================
# Sales Data
# =============================================================================

PRODUCTS = ["Widget A", "Widget B", "Widget C", "Gadget Pro", "Gadget Lite"]
REGIONS = ["North", "South", "East", "West"]

SALES_DATA = [
    {"month": "Jan", "product": "Widget A", "region": "North", "units": 150, "unit_price": 30, "revenue": 4500},
    {"month": "Jan", "product": "Widget B", "region": "North", "units": 200, "unit_price": 30, "revenue": 6000},
    {"month": "Jan", "product": "Widget C", "region": "East", "units": 120, "unit_price": 45, "revenue": 5400},
    {"month": "Feb", "product": "Widget A", "region": "North", "units": 175, "unit_price": 30, "revenue": 5250},
    {"month": "Feb", "product": "Widget B", "region": "South", "units": 220, "unit_price": 30, "revenue": 6600},
    {"month": "Feb", "product": "Gadget Pro", "region": "West", "units": 80, "unit_price": 120, "revenue": 9600},
    {"month": "Mar", "product": "Widget A", "region": "East", "units": 190, "unit_price": 30, "revenue": 5700},
    {"month": "Mar", "product": "Widget C", "region": "North", "units": 140, "unit_price": 45, "revenue": 6300},
    {"month": "Mar", "product": "Gadget Lite", "region": "South", "units": 250, "unit_price": 75, "revenue": 18750},
    {"month": "Apr", "product": "Widget B", "region": "East", "units": 180, "unit_price": 30, "revenue": 5400},
    {"month": "Apr", "product": "Gadget Pro", "region": "North", "units": 95, "unit_price": 120, "revenue": 11400},
    {"month": "Apr", "product": "Gadget Lite", "region": "West", "units": 210, "unit_price": 75, "revenue": 15750},
    {"month": "May", "product": "Widget A", "region": "South", "units": 165, "unit_price": 30, "revenue": 4950},
    {"month": "May", "product": "Widget C", "region": "West", "units": 130, "unit_price": 45, "revenue": 5850},
    {"month": "May", "product": "Gadget Pro", "region": "East", "units": 110, "unit_price": 120, "revenue": 13200},
    {"month": "Jun", "product": "Widget B", "region": "North", "units": 240, "unit_price": 30, "revenue": 7200},
    {"month": "Jun", "product": "Gadget Lite", "region": "South", "units": 280, "unit_price": 75, "revenue": 21000},
    {"month": "Jun", "product": "Widget A", "region": "West", "units": 155, "unit_price": 30, "revenue": 4650},
]

# =============================================================================
# Budget Data
# =============================================================================

EXPENSE_CATEGORIES = ["Rent", "Utilities", "Groceries", "Transportation", "Entertainment", "Healthcare", "Insurance"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Investments", "Other"]

BUDGET_DATA = [
    # January
    {"date": "2024-01-01", "category": "Salary", "type": "income", "amount": 5000, "description": "Monthly salary"},
    {"date": "2024-01-05", "category": "Rent", "type": "expense", "amount": 1500, "description": "Monthly rent"},
    {"date": "2024-01-10", "category": "Utilities", "type": "expense", "amount": 150, "description": "Electric & water"},
    {"date": "2024-01-15", "category": "Groceries", "type": "expense", "amount": 400, "description": "Weekly groceries"},
    {"date": "2024-01-20", "category": "Transportation", "type": "expense", "amount": 200, "description": "Gas & transit"},
    {"date": "2024-01-25", "category": "Entertainment", "type": "expense", "amount": 100, "description": "Streaming & dining"},
    # February
    {"date": "2024-02-01", "category": "Salary", "type": "income", "amount": 5000, "description": "Monthly salary"},
    {"date": "2024-02-05", "category": "Rent", "type": "expense", "amount": 1500, "description": "Monthly rent"},
    {"date": "2024-02-08", "category": "Freelance", "type": "income", "amount": 800, "description": "Side project"},
    {"date": "2024-02-10", "category": "Utilities", "type": "expense", "amount": 160, "description": "Electric & water"},
    {"date": "2024-02-15", "category": "Groceries", "type": "expense", "amount": 380, "description": "Weekly groceries"},
    {"date": "2024-02-18", "category": "Healthcare", "type": "expense", "amount": 75, "description": "Doctor visit"},
    {"date": "2024-02-22", "category": "Insurance", "type": "expense", "amount": 200, "description": "Auto insurance"},
    # March
    {"date": "2024-03-01", "category": "Salary", "type": "income", "amount": 5000, "description": "Monthly salary"},
    {"date": "2024-03-05", "category": "Rent", "type": "expense", "amount": 1500, "description": "Monthly rent"},
    {"date": "2024-03-10", "category": "Utilities", "type": "expense", "amount": 140, "description": "Electric & water"},
    {"date": "2024-03-12", "category": "Investments", "type": "income", "amount": 250, "description": "Dividend income"},
    {"date": "2024-03-15", "category": "Groceries", "type": "expense", "amount": 420, "description": "Weekly groceries"},
    {"date": "2024-03-20", "category": "Transportation", "type": "expense", "amount": 180, "description": "Gas & transit"},
    {"date": "2024-03-28", "category": "Entertainment", "type": "expense", "amount": 150, "description": "Concert tickets"},
]

# =============================================================================
# Employee Data
# =============================================================================

DEPARTMENTS = ["Engineering", "Sales", "Marketing", "Finance", "HR", "Operations"]
TITLES = {
    "Engineering": ["Software Engineer", "Senior Engineer", "Tech Lead", "Engineering Manager"],
    "Sales": ["Sales Rep", "Account Executive", "Sales Manager", "VP Sales"],
    "Marketing": ["Marketing Coordinator", "Marketing Manager", "Content Strategist", "CMO"],
    "Finance": ["Financial Analyst", "Senior Analyst", "Finance Manager", "CFO"],
    "HR": ["HR Coordinator", "HR Manager", "Recruiter", "CHRO"],
    "Operations": ["Operations Analyst", "Operations Manager", "Project Manager", "COO"],
}

EMPLOYEE_DATA = [
    {"id": "EMP001", "name": "John Smith", "department": "Engineering", "title": "Senior Engineer", "salary": 95000, "start_date": "2022-03-15", "email": "john.smith@company.com"},
    {"id": "EMP002", "name": "Sarah Johnson", "department": "Engineering", "title": "Tech Lead", "salary": 125000, "start_date": "2020-08-01", "email": "sarah.johnson@company.com"},
    {"id": "EMP003", "name": "Michael Chen", "department": "Sales", "title": "Account Executive", "salary": 75000, "start_date": "2023-01-10", "email": "michael.chen@company.com"},
    {"id": "EMP004", "name": "Emily Davis", "department": "Marketing", "title": "Marketing Manager", "salary": 85000, "start_date": "2021-06-20", "email": "emily.davis@company.com"},
    {"id": "EMP005", "name": "Robert Wilson", "department": "Finance", "title": "Financial Analyst", "salary": 70000, "start_date": "2023-04-05", "email": "robert.wilson@company.com"},
    {"id": "EMP006", "name": "Lisa Anderson", "department": "HR", "title": "HR Manager", "salary": 80000, "start_date": "2019-11-15", "email": "lisa.anderson@company.com"},
    {"id": "EMP007", "name": "David Martinez", "department": "Operations", "title": "Project Manager", "salary": 90000, "start_date": "2022-09-01", "email": "david.martinez@company.com"},
    {"id": "EMP008", "name": "Jennifer Taylor", "department": "Engineering", "title": "Software Engineer", "salary": 85000, "start_date": "2023-02-20", "email": "jennifer.taylor@company.com"},
    {"id": "EMP009", "name": "James Brown", "department": "Sales", "title": "Sales Manager", "salary": 95000, "start_date": "2020-05-10", "email": "james.brown@company.com"},
    {"id": "EMP010", "name": "Amanda White", "department": "Marketing", "title": "Content Strategist", "salary": 72000, "start_date": "2022-07-25", "email": "amanda.white@company.com"},
]


# =============================================================================
# Helper Functions
# =============================================================================

def get_sales_data(months: int = 6, products: list[str] | None = None) -> list[dict]:
    """
    Get sales data, optionally filtered by months and products.

    Args:
        months: Number of months of data to return (from the beginning)
        products: List of product names to filter by (None for all)

    Returns:
        List of sales records
    """
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    valid_months = set(month_order[:months])

    result = [
        record for record in SALES_DATA
        if record["month"] in valid_months
        and (products is None or record["product"] in products)
    ]

    return result


def get_budget_data(months: int = 3, type_filter: str | None = None) -> list[dict]:
    """
    Get budget data, optionally filtered by months and type.

    Args:
        months: Number of months of data to return
        type_filter: "income", "expense", or None for all

    Returns:
        List of budget records
    """
    # Calculate date cutoff
    start_date = datetime(2024, 1, 1)
    end_date = start_date + timedelta(days=months * 30)

    result = []
    for record in BUDGET_DATA:
        record_date = datetime.strptime(record["date"], "%Y-%m-%d")
        if record_date < end_date:
            if type_filter is None or record["type"] == type_filter:
                result.append(record)

    return result


def get_employee_data(
    count: int | None = None,
    department: str | None = None,
    min_salary: int | None = None
) -> list[dict]:
    """
    Get employee data with optional filters.

    Args:
        count: Maximum number of employees to return (None for all)
        department: Filter by department name
        min_salary: Filter by minimum salary

    Returns:
        List of employee records
    """
    result = []

    for employee in EMPLOYEE_DATA:
        if department and employee["department"] != department:
            continue
        if min_salary and employee["salary"] < min_salary:
            continue
        result.append(employee)

        if count and len(result) >= count:
            break

    return result


def generate_sales_data(months: int = 12, seed: int | None = None) -> list[dict]:
    """
    Generate random sales data for testing.

    Args:
        months: Number of months to generate
        seed: Random seed for reproducibility

    Returns:
        List of generated sales records
    """
    if seed is not None:
        random.seed(seed)

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    result = []

    for month_idx in range(months):
        month = month_names[month_idx % 12]
        for product in PRODUCTS:
            for region in REGIONS:
                # Not every product/region combination has sales each month
                if random.random() < 0.6:
                    continue

                units = random.randint(50, 300)
                unit_price = {
                    "Widget A": 30,
                    "Widget B": 30,
                    "Widget C": 45,
                    "Gadget Pro": 120,
                    "Gadget Lite": 75,
                }[product]

                result.append({
                    "month": month,
                    "product": product,
                    "region": region,
                    "units": units,
                    "unit_price": unit_price,
                    "revenue": units * unit_price,
                })

    return result


def generate_budget_data(months: int = 6, seed: int | None = None) -> list[dict]:
    """
    Generate random budget data for testing.

    Args:
        months: Number of months to generate
        seed: Random seed for reproducibility

    Returns:
        List of generated budget records
    """
    if seed is not None:
        random.seed(seed)

    result = []
    base_date = datetime(2024, 1, 1)

    for month_offset in range(months):
        month_start = base_date + timedelta(days=month_offset * 30)

        # Monthly salary (always)
        result.append({
            "date": month_start.strftime("%Y-%m-%d"),
            "category": "Salary",
            "type": "income",
            "amount": 5000,
            "description": "Monthly salary",
        })

        # Rent (always)
        result.append({
            "date": (month_start + timedelta(days=4)).strftime("%Y-%m-%d"),
            "category": "Rent",
            "type": "expense",
            "amount": 1500,
            "description": "Monthly rent",
        })

        # Random expenses
        for category in ["Utilities", "Groceries", "Transportation", "Entertainment"]:
            day_offset = random.randint(5, 25)
            amounts = {
                "Utilities": (100, 200),
                "Groceries": (300, 500),
                "Transportation": (100, 250),
                "Entertainment": (50, 200),
            }
            min_amt, max_amt = amounts[category]

            result.append({
                "date": (month_start + timedelta(days=day_offset)).strftime("%Y-%m-%d"),
                "category": category,
                "type": "expense",
                "amount": random.randint(min_amt, max_amt),
                "description": f"Monthly {category.lower()}",
            })

        # Occasional freelance income
        if random.random() < 0.3:
            result.append({
                "date": (month_start + timedelta(days=random.randint(1, 28))).strftime("%Y-%m-%d"),
                "category": "Freelance",
                "type": "income",
                "amount": random.randint(500, 1500),
                "description": "Freelance project",
            })

    # Sort by date
    result.sort(key=lambda x: x["date"])
    return result


def get_summary_stats(data: list[dict], value_field: str, group_field: str | None = None) -> dict:
    """
    Calculate summary statistics for a dataset.

    Args:
        data: List of records
        value_field: Field name containing numeric values
        group_field: Optional field to group by

    Returns:
        Dictionary with statistics (total, average, min, max, count)
    """
    if not data:
        return {"total": 0, "average": 0, "min": 0, "max": 0, "count": 0}

    if group_field:
        groups = {}
        for record in data:
            key = record.get(group_field, "Unknown")
            if key not in groups:
                groups[key] = []
            groups[key].append(record.get(value_field, 0))

        result = {}
        for key, values in groups.items():
            result[key] = {
                "total": sum(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "count": len(values),
            }
        return result
    else:
        values = [record.get(value_field, 0) for record in data]
        return {
            "total": sum(values),
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "count": len(values),
        }


# =============================================================================
# Data Conversion Helpers
# =============================================================================

def to_rows(data: list[dict], columns: list[str] | None = None) -> tuple[list[str], list[list]]:
    """
    Convert list of dicts to header row and data rows.

    Args:
        data: List of dictionaries
        columns: Optional list of column names to include (in order)

    Returns:
        Tuple of (headers, rows)
    """
    if not data:
        return [], []

    if columns is None:
        columns = list(data[0].keys())

    headers = columns
    rows = [[record.get(col, "") for col in columns] for record in data]

    return headers, rows
