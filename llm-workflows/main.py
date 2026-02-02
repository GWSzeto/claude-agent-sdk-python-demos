from util import llm_call, extract_xml
from concurrent.futures import ThreadPoolExecutor

def chain(input: str, prompts: list[str]) -> str:
    result = input
    for i, prompt in enumerate(prompts, 1):
        print(f"\nstep {i}:")
        result = llm_call(f"{prompt}\nInput: {result}")
        print(result)

    return result

def parallel(prompt: str, inputs: list[str], n_workers: int = 3) -> list[str]:
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(llm_call, f"{prompt}\nInput: {x}") for x in inputs]
        return [f.result() for f in futures]

def route(input: str, routes: dict[str, str]) -> str:
    print(f"\nAvailable routes: {list(routes.keys())}")
    selector_prompt = f"""
    Analyze the input and select the most appropriate support team from these options: {list(routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgeny level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>

    Input: {input}""".strip()

    route_response = llm_call(selector_prompt)
    reasoning = extract_xml(route_response, "reasoning")
    route_key = extract_xml(route_response, "selection").strip().lower()

    print("Routing Analysis:")
    print(reasoning)
    print(f"\nSelected route: {route_key}")

    selected_prompt = routes[route_key]
    return llm_call(f"{selected_prompt}\nInput: {input}")


# Eaxmple 1: Chain workflow for structured data extraction and formatting
# Each step progressively transforms raw text into a formatted table

data_processing_steps = [
    """Extract only the numerical values and their associated metrics form the text.
       Format each as 'vale: metric' on a new line
       Example format:
       92: customer satisfaction
       45%: revenue growth""",
    """Convert all numerical values to percentages where possible.
        If not a percentage or points, convert to decimal (e.g., 92 points -> 92%).
        Keep one number per line.
        Example format:
        92%: customer satisfaction
        45%: revenue growth""",
    """Sort all lines in descending order by numerical value.
    Keep the format 'value: metric' on each line.
    Example:
    92%: csutoemr satisfaction
    87%: employee satisfaction""",
    """Format the sorted data as a markdown table with columns:
        | Metric | Value | 
        |:--|--:|
        | Custoemr Satisfaction | 92% |
    """
]

report = """
    Q3 Performance Summary:
    Out customer satisfaction score rose to 92 points this quarter.
    Revenue grew by 45% compared to last year.
    Market share is now at 23% in our primary market.
    Customer churn decreased to 5% from 8%.
    New user acquisition cost is 43$ per user.
    Product adoption rate increased to 78%.
    Employee satisfaction is at 87 points.
    Operating margin improved to 34%.
"""

print("\nInput text:")
print(report)
formatted_result = chain(report, data_processing_steps)

# Example 2: Parallelization workflow for stakeholder impact analysis
# Process impact analysis for multiple stakeholder groups concurrently

stakeholders = [
    """Customers:
    - Price sensitive
    - Want better tech
    - Environmental concerns""",
    """Employees:
    - Job security worries
    - Need new skills
    - Want clear direction""",
    """Investors:
    - Expect growth
    - Want cost control
    - Risk concerns""",
    """Suppliers:
    - Capactiry constraints
    - Price pressures
    - Tech transitions"""
]

impact_results = parallel(
    """Analyze how market changes will impact this stakeholder group.
    Provide specific impacts and recommend actions.
    Format with clear sections and priorities.""",
    stakeholders,
)

for result in impact_results:
    print(result)
    print("+" * 80)


# Example 3: Route workflow for customer support ticket handling
# Route support tickets to appropriate teams based on content analysis

support_routes = {
        "billing": """You are a billing support specialist. Follow these guidelines:
        1. Always start with "Billing Support Response:"
        2. first acknowledge the specific billing issue
        3. Explain any charges or discrpancies clearly
        4. List concrete next steps with timeline
        5. End with payment options if relevant

        Keep responses professional but friendly.

        Input: """,
        "technical": """You are a technical support engineer. Follow these guidelines:
        1. Always start with "Technical Support Response:"
        2. List exact steps to resolve the issue
        3. Include system requirements if relevant
        4. Provide workarounds for common problems
        5. End with escalation path if needed

        Use clear, numbered steps and technical details.

        Input: """,
        "account": """You are an account security specialist. Follow these guidelines:
        1. Always start with "Account Support Response:"
        2. Prioritize account security and verification
        3. Provide clear steps for account recovery/changes
        4. Include security tips and warnings
        5. Set clear expectations for resoltuion time

        Maintain a serious, security-focused tone.

        Input: """,
        "product": """Youa re a product specialist. Follow these guidelines:
        1. Always start with "Product Support Response:"
        2. focus on feature education and best practices
        3. Include specific examples of usage
        4. Link to relevant documentation sections
        5. Suggest related features that might help

        Be educational and encouraging in tone.

        Input: """,
}


# Test with different support tickets
tickets = [
    """Subject: Can't access my account
    Message: Hi, I've been trying to log in for the past hour but keep getting an 'invalid password' error.
    I'm sure I'm using the right password. Can you help me regain access? This is urgent as I need to
    submit a report by end of day.
    - John""",
    """Subject: Unexpected charge on my card
    Message: Hello, I just noticed a charge of $49.99 on my credit card from your company, but I thought
    I was on the $29.99 plan. Can you explain this charge and adjust it if it's a mistake?
    Thanks,
    Sarah""",
    """Subject: How to export data?
    Message: I need to export all my project data to Excel. I've looked through the docs but can't
    figure out how to do a bulk export. Is this possible? If so, could you walk me through the steps?
    Best regards,
    Mike""",
]

print("Processing support tickets...\n")
for i, ticket in enumerate(tickets, 1):
    print(f"\nTicket {i}:")
    print("-" * 40)
    print(ticket)
    print("\nResponse:")
    print("-" * 40)
    response = route(ticket, support_routes)
    print(response)
    print("+" * 80)


