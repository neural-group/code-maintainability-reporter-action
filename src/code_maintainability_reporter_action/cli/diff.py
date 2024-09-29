import json
from collections import defaultdict

def parse_json(json_str: str):
    """Parse JSON strings with mixed single and double quotes, and return a proper JSON object."""
    # Replace single quotes with double quotes to ensure correct JSON format
    json_str = json_str.replace("'", '"')
    return json.loads(json_str)

def calculate_diff(json_old: dict, json_new: dict):
    """Calculate the differences between the old and new JSON."""
    keys = set(json_old.keys()).union(set(json_new.keys()))  # Get all unique keys
    result = []

    total_diff = defaultdict(float)  # Track total differences for summary row
    for key in keys:
        old_val = json_old.get(key, {'cc': 0.0, 'hal': 0.0, 'sloc': 0.0, 'mi_raw': 0.0, 'mi_pct': None})
        new_val = json_new.get(key, {'cc': 0.0, 'hal': 0.0, 'sloc': 0.0, 'mi_raw': 0.0, 'mi_pct': None})

        # Calculate differences for fields
        diff_cc = round(new_val['cc'] - old_val['cc'], 1)
        diff_hal = round(new_val['hal'] - old_val['hal'], 1)
        diff_sloc = round(new_val['sloc'] - old_val['sloc'], 1)
        diff_mi_raw = round(new_val['mi_raw'] - old_val['mi_raw'], 1)
        
        # Check for changes (skip if cc, hal, and sloc are unchanged)
        if diff_cc == 0 and diff_hal == 0 and diff_sloc == 0:
            continue

        # Determine the status (Add, Del, Upd)
        if key in json_old and key not in json_new:
            status = "Del"
        elif key not in json_old and key in json_new:
            status = "Add"
        else:
            status = "Upd"

        # mi_pct should be directly taken from new value if key exists in json_new, else leave blank
        new_mi_pct = f"{new_val['mi_pct']:.1f}" if new_val['mi_pct'] is not None else ""

        # Append the row
        result.append((key, status, diff_cc, diff_hal, diff_sloc, diff_mi_raw, new_mi_pct))

        # Add to total summary if it's an update
        total_diff['cc'] += diff_cc
        total_diff['hal'] += diff_hal
        total_diff['sloc'] += diff_sloc
        total_diff['mi_raw'] += diff_mi_raw

    # Create summary row
    result.append((
        "**total**", "", 
        round(total_diff['cc'], 1), 
        round(total_diff['hal'], 1), 
        round(total_diff['sloc'], 1), 
        round(total_diff['mi_raw'], 1), 
        ""  # mi_pct should be blank
    ))

    return result

def format_as_markdown(diff_list):
    """Format the differences as a Markdown table."""
    header = "| Key |   | diff cc | diff hal | diff sloc | diff mi_raw | new mi_pct |"
    separator = "|---|---|---|---|---|---|---|"
    rows = [header, separator]

    for key, status, diff_cc, diff_hal, diff_sloc, diff_mi_raw, new_mi_pct in diff_list:
        rows.append(f"| {key} | {status} | {diff_cc} | {diff_hal} | {diff_sloc} | {diff_mi_raw} | {new_mi_pct} |")

    return "\n".join(rows)

def main(value1: str, value2: str):
    # Parse json
    json_old = parse_json(value1)
    json_new = parse_json(value2)

    # Calculate differences
    diff_list = calculate_diff(json_old, json_new)

    # Generate the Markdown table
    markdown_output = format_as_markdown(diff_list)

    # Wrap the output in a collapsible <details> tag
    final_output = f"""
<details>
<summary>Code Complexity Analytics</summary>

{markdown_output}

</details>
"""

    print(final_output)
