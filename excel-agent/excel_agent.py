from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage, create_sdk_mcp_server, tool
import asyncio
import json
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import pandas as pd

@tool("create_spreadsheet", "Create a new Excel spreadsheet with data", {
    "filename": str,
    "sheet_name": str,
    "data": list,
    "headers": list
})
async def create_spreadsheet(args):
    filename = args["filename"]
    sheet_name = args.get("sheet_name", "Sheet1")
    data = args["data"]
    headers = args.get("headers", [])

    # Ensure .xlsx extension
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # Create workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Add headers if provided
    row_offset = 0
    if headers:
        for col_idx, header in enumerate(headers, start=1):
            ws.cell(row=1, column=col_idx, value=header)
        row_offset = 1

    # Add data rows
    for row_idx, row_data in enumerate(data, start=1 + row_offset):
        for col_idx, value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    # Auto-adjust column widths
    for col_idx in range(1, (len(headers) or len(data[0]) if data else 0) + 1):
        col_letter = get_column_letter(col_idx)
        max_length = 0
        for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):
            for cell in row:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_length + 2, 50)

    wb.save(filename)

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "status": "success",
                "filename": filename,
                "sheet_name": sheet_name,
                "rows": len(data),
                "columns": len(headers) if headers else (len(data[0]) if data else 0),
            }, indent=2)
        }]
    }

@tool("read_spreadsheet", "Read data from an Excel spreadsheet", {
    "filename": str,
    "sheet_name": str,
    "range": str
})
async def read_spreadsheet(args):
    filename = args["filename"]
    sheet_name = args.get("sheet_name")
    cell_range = args.get("range")

    if not Path(filename).exists():
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({"error": f"File not found: {filename}"})
            }]
        }

    try:
        # Read with pandas
        df = pd.read_excel(filename, sheet_name=sheet_name or 0)

        # Convert to records
        headers = list(df.columns)
        data = df.to_dict(orient="records")

        # Get sheet names
        wb = load_workbook(filename, read_only=True)
        sheet_names = wb.sheetnames
        wb.close()

        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "filename": filename,
                    "sheet_name": sheet_name or sheet_names[0],
                    "available_sheets": sheet_names,
                    "headers": headers,
                    "row_count": len(data),
                    "data": data[:100],  # Limit to 100 rows
                    "truncated": len(data) > 100,
                }, indent=2)
            }]
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({"error": str(e)})
            }]
        }

excel_tools = create_sdk_mcp_server(
    name="excel",
    version="1.0.0",
    tools=[create_spreadsheet, read_spreadsheet]
)

options = ClaudeAgentOptions(
    mcp_servers={"excel": excel_tools},
    allowed_tools=["mcp__excel__create_spreadsheet", "mcp__excel__read_spreadsheet"],
)

async def main():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Create an employee directory spreadsheet")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"[ASSISTANT]: {block.text}")

            elif isinstance(message, ResultMessage):
                print(f"[RESULT]: {message.result}")

asyncio.run(main())
