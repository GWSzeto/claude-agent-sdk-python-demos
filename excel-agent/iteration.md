# Excel Agent - Python Implementation Iterations

## TypeScript Demo Analysis

### Key Agentic Components

The TypeScript excel-demo is an Electron desktop app with a Python agent backend:

1. **CLAUDE.MD**: Agent instructions defining scope (Excel-only tasks)
2. **xlsx Skill**: Comprehensive skill for spreadsheet operations
3. **recalc.py**: LibreOffice-based formula recalculation script
4. **Libraries**: openpyxl (formulas/formatting), pandas (data analysis)

### Core Capabilities

- Create, read, modify Excel files (.xlsx, .xlsm, .csv, .tsv)
- Formula management with zero-error requirement
- Professional formatting (color coding, number formats)
- Data analysis and visualization
- Formula recalculation and error detection

### Workflow

```
User Request → xlsx Skill → Create/Edit with openpyxl
                              ↓
                        Add formulas/formatting
                              ↓
                        recalc.py (LibreOffice)
                              ↓
                        Verify errors → Fix if needed
                              ↓
                        Final output
```

---

## Python Implementation Approach

### Simplified Scope

We'll focus on the core agentic components without the Electron UI:
- MCP tools for Excel operations
- xlsx Skill for domain knowledge
- CLI interface for interaction
- Mock data for testing
- Formula recalculation (optional - requires LibreOffice)

### MCP Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `create_spreadsheet` | Create new Excel file with data | Core tool |
| `read_spreadsheet` | Read and analyze Excel data | Core tool |
| `edit_spreadsheet` | Modify existing Excel file | Core tool |
| `add_formula` | Add formulas to cells | Formula management |
| `format_cells` | Apply formatting (colors, fonts) | Styling |
| `get_spreadsheet_info` | Get metadata about file | Analysis |
| `recalculate_formulas` | Recalculate using LibreOffice | Optional |

---

## Iteration 1: Project Setup with Mock Data

**Goal**: Set up project structure with sample Excel data and helper functions.

**Requirements**:
- Create `mock_data.py` with sample datasets:
  - Sales data (monthly revenue, products)
  - Budget tracker (income, expenses, categories)
  - Employee data (names, departments, salaries)
- Helper functions for generating sample data
- Basic project structure

**Mock Data Scenarios**:
```python
# Sample datasets to include:
SALES_DATA = [
    {"month": "Jan", "product": "Widget A", "units": 150, "revenue": 4500},
    {"month": "Jan", "product": "Widget B", "units": 200, "revenue": 6000},
    # ...
]

BUDGET_DATA = [
    {"category": "Salary", "type": "income", "amount": 5000, "date": "2024-01-01"},
    {"category": "Rent", "type": "expense", "amount": 1500, "date": "2024-01-01"},
    # ...
]

EMPLOYEE_DATA = [
    {"name": "John Smith", "department": "Engineering", "salary": 85000, "start_date": "2022-03-15"},
    # ...
]
```

**Helper Functions**:
```python
def get_sales_data(months: int = 12) -> list[dict]:
    """Get sample sales data for N months."""
    pass

def get_budget_data(months: int = 6) -> list[dict]:
    """Get sample budget data."""
    pass

def get_employee_data(count: int = 10) -> list[dict]:
    """Get sample employee data."""
    pass
```

**Expected Structure**:
```
excel-agent/
├── mock_data.py      # Sample datasets and helpers
├── iteration.md      # This file
└── .claude/
    └── skills/
        └── xlsx/     # Will hold SKILL.md
```

**Key Concepts Tested**:
- Data modeling for spreadsheets
- Sample data generation
- Project organization

---

## Iteration 2: Basic MCP Tools (create, read)

**Goal**: Create core MCP tools for spreadsheet creation and reading.

**Requirements**:
- Create `create_spreadsheet` tool using openpyxl
- Create `read_spreadsheet` tool for data extraction
- Set up MCP server with `create_sdk_mcp_server()`
- Basic agent that can create and read Excel files

**Tool Definitions**:
```python
@tool("create_spreadsheet", "Create a new Excel spreadsheet with data", {
    "filename": str,
    "sheet_name": str,
    "data": list,      # List of dicts or list of lists
    "headers": list    # Optional column headers
})
async def create_spreadsheet(args: dict) -> dict:
    """Create a new Excel file with the provided data."""
    pass

@tool("read_spreadsheet", "Read data from an Excel spreadsheet", {
    "filename": str,
    "sheet_name": str,  # Optional, defaults to active sheet
    "range": str        # Optional, e.g., "A1:D10"
})
async def read_spreadsheet(args: dict) -> dict:
    """Read and return data from an Excel file."""
    pass
```

**Test Prompts**:
```
"Create a sales report spreadsheet with monthly data"
"Read the contents of Budget_Tracker.xlsx"
"Create a new employee directory spreadsheet"
```

**Key Concepts Tested**:
- MCP tool creation with `@tool` decorator
- openpyxl for Excel file creation
- pandas for data reading
- File I/O handling

---

## Iteration 3: Edit and Formula Tools

**Goal**: Add tools for editing spreadsheets and managing formulas.

**Requirements**:
- Create `edit_spreadsheet` tool for cell modifications
- Create `add_formula` tool for formula insertion
- Create `get_spreadsheet_info` tool for metadata
- Handle formula strings properly (Excel syntax)

**Tool Definitions**:
```python
@tool("edit_spreadsheet", "Edit cells in an existing spreadsheet", {
    "filename": str,
    "sheet_name": str,
    "edits": list      # List of {"cell": "A1", "value": "new value"}
})
async def edit_spreadsheet(args: dict) -> dict:
    """Edit specific cells in an Excel file."""
    pass

@tool("add_formula", "Add Excel formulas to cells", {
    "filename": str,
    "sheet_name": str,
    "formulas": list   # List of {"cell": "B10", "formula": "=SUM(B2:B9)"}
})
async def add_formula(args: dict) -> dict:
    """Add formulas to specified cells."""
    pass

@tool("get_spreadsheet_info", "Get metadata about a spreadsheet", {
    "filename": str
})
async def get_spreadsheet_info(args: dict) -> dict:
    """Return sheet names, dimensions, formula count, etc."""
    pass
```

**Formula Guidelines** (from xlsx Skill):
- Always use Excel formulas, not hardcoded Python calculations
- Common formulas: `=SUM()`, `=AVERAGE()`, `=IF()`, `=VLOOKUP()`
- Cross-sheet references: `=Sheet1!A1`

**Test Prompts**:
```
"Add a SUM formula to total the revenue column"
"Edit cell A1 to say 'Sales Report 2024'"
"What sheets are in the Budget_Tracker.xlsx file?"
```

**Key Concepts Tested**:
- File modification with openpyxl
- Formula string handling
- Preserving existing data when editing

---

## Iteration 4: Formatting Tools

**Goal**: Add tools for professional spreadsheet formatting.

**Requirements**:
- Create `format_cells` tool for styling
- Support color coding (financial model standards)
- Support number formatting
- Support alignment and borders

**Tool Definition**:
```python
@tool("format_cells", "Apply formatting to cells", {
    "filename": str,
    "sheet_name": str,
    "formats": list    # List of formatting instructions
})
async def format_cells(args: dict) -> dict:
    """
    Apply formatting to cells.

    Format options:
    - font: {"bold": True, "color": "FF0000", "size": 12}
    - fill: {"color": "FFFF00"}  # Background color
    - alignment: {"horizontal": "center", "vertical": "center"}
    - number_format: "$#,##0.00" or "0.0%" or "0.0x"
    - border: {"style": "thin", "color": "000000"}
    """
    pass
```

**Color Coding Standards** (Financial Models):
```python
COLORS = {
    "input_blue": "0000FF",      # Hardcoded inputs
    "formula_black": "000000",   # Formulas/calculations
    "link_green": "008000",      # Cross-sheet links
    "external_red": "FF0000",    # External links
    "attention_yellow": "FFFF00" # Key assumptions (background)
}
```

**Number Format Examples**:
```python
NUMBER_FORMATS = {
    "currency": "$#,##0;($#,##0);-",
    "percentage": "0.0%",
    "multiple": "0.0x",
    "year": "@",  # Text format for years
}
```

**Test Prompts**:
```
"Format the header row with bold text and yellow background"
"Apply currency formatting to the revenue column"
"Color the input cells blue and formula cells black"
```

**Key Concepts Tested**:
- openpyxl styling (Font, PatternFill, Alignment, Border)
- Financial model color conventions
- Number format strings

---

## Iteration 5: xlsx Skill Integration

**Goal**: Create the xlsx Skill for comprehensive domain knowledge.

**Requirements**:
- Create `SKILL.md` with YAML frontmatter
- Include formula best practices
- Include formatting standards
- Include common workflow patterns
- Configure `setting_sources` to load the Skill

**Skill Content** (`.claude/skills/xlsx/SKILL.md`):
```yaml
---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis. Use when working with Excel files for creating spreadsheets, adding formulas, formatting, or data analysis."
---

# xlsx Skill

## Core Principles

### Use Formulas, Not Hardcoded Values
Always use Excel formulas instead of calculating in Python.

❌ WRONG:
```python
total = sum(values)
sheet['B10'] = total  # Hardcodes result
```

✅ CORRECT:
```python
sheet['B10'] = '=SUM(B2:B9)'  # Dynamic formula
```

## Color Coding Standards (Financial Models)
- **Blue text**: Hardcoded inputs (user-changeable)
- **Black text**: Formulas and calculations
- **Green text**: Cross-sheet links
- **Red text**: External file links
- **Yellow background**: Key assumptions

## Number Formatting
- Currency: $#,##0;($#,##0);-
- Percentages: 0.0%
- Multiples: 0.0x
- Years: Text format (@)

## Common Formulas
- SUM, AVERAGE, COUNT, COUNTA
- IF, IFERROR, IFNA
- VLOOKUP, XLOOKUP, INDEX/MATCH
- SUMIF, COUNTIF, AVERAGEIF

## Workflow
1. Create/load spreadsheet
2. Add data and formulas
3. Apply formatting
4. Verify formulas (no errors)
5. Save file
```

**Agent Configuration**:
```python
options = ClaudeAgentOptions(
    mcp_servers={"excel": excel_tools},
    allowed_tools=[...],
    setting_sources=["project"],
    cwd=str(Path(__file__).parent)
)
```

**Test Prompts**:
```
"Create a budget tracker following financial model standards"
"Help me build a sales dashboard with proper formatting"
```

**Key Concepts Tested**:
- Skill creation with SKILL.md
- Domain-specific knowledge encoding
- `setting_sources` configuration

---

## Iteration 6: Hooks, CLI, and Evaluator Pattern

**Goal**: Add hooks for monitoring, CLI interface, and quality evaluation.

**Requirements**:
- PreToolUse hook to log Excel operations
- CLI using shared `AgentCLI` module
- Quality evaluator for spreadsheet validation
- Support for common workflows (budget, sales, etc.)

**Hook Implementation**:
```python
async def log_excel_operation(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all Excel operations."""
    tool_name = input_data.get('tool_name', 'unknown')

    if tool_name.startswith('mcp__excel__'):
        operation = tool_name.replace('mcp__excel__', '')
        print(f"[EXCEL-OP] {operation}")

    return {}
```

**Quality Evaluator Tool**:
```python
@tool("evaluate_spreadsheet", "Evaluate spreadsheet quality", {"filename": str})
async def evaluate_spreadsheet(args: dict) -> dict:
    """
    Evaluate spreadsheet against quality criteria:
    1. Formula errors (0 tolerance for #REF!, #DIV/0!, etc.)
    2. Formatting consistency
    3. Data completeness
    4. Formula usage (vs hardcoded values)
    """
    pass
```

**CLI Configuration**:
```python
cli = AgentCLI(
    name="Excel Agent",
    description="AI-powered spreadsheet creation and analysis",
    arguments=[
        CLIArgument(name="--query", short="-q", help="Direct query"),
        CLIArgument(name="--create-budget", help="Create budget tracker", action="store_true"),
        CLIArgument(name="--create-sales", help="Create sales report", action="store_true"),
        CLIArgument(name="--analyze", short="-a", help="Analyze existing file"),
        CLIArgument(name="--output", short="-o", help="Output filename"),
        CLIArgument(name="--verbose", short="-v", help="Show detailed output", action="store_true"),
    ]
)
```

**Usage Examples**:
```bash
# Direct query
python excel_agent.py -q "Create a monthly expense tracker"

# Create budget tracker
python excel_agent.py --create-budget -o my_budget.xlsx

# Analyze existing file
python excel_agent.py --analyze existing_file.xlsx

# Verbose mode
python excel_agent.py --create-sales -v
```

**Key Concepts Tested**:
- Hooks for operation logging
- CLI with shared module
- Quality evaluation pattern
- Multiple workflow shortcuts

---

## Comparison Checklist

| Feature | TypeScript Demo | Python Implementation |
|---------|-----------------|----------------------|
| UI | Electron desktop app | CLI |
| Excel Library | N/A (Python agent) | openpyxl + pandas |
| Agent Instructions | CLAUDE.MD | CLI + Skills |
| xlsx Skill | Full skill | Simplified skill |
| Formula Recalc | recalc.py + LibreOffice | Optional (mock/skip) |
| Formatting | Full support | Core formatting |
| Data Analysis | pandas | pandas |

## Tools Summary

| Tool | Purpose | Iteration |
|------|---------|-----------|
| `create_spreadsheet` | Create new Excel file | 2 |
| `read_spreadsheet` | Read Excel data | 2 |
| `edit_spreadsheet` | Modify cells | 3 |
| `add_formula` | Add formulas | 3 |
| `get_spreadsheet_info` | File metadata | 3 |
| `format_cells` | Apply styling | 4 |
| `evaluate_spreadsheet` | Quality check | 6 |

## Patterns Used

| Pattern | Iteration | Description |
|---------|-----------|-------------|
| Augmented LLM | 1-4 | Tools + Mock data |
| Skills | 5 | Domain knowledge via SKILL.md |
| Evaluator | 6 | Quality validation for spreadsheets |

## Dependencies

```
openpyxl>=3.1.0
pandas>=2.0.0
```
