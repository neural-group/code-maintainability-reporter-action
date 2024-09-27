#!/bin/bash

# This script is generated by Chat GPT with the prompt:
#------
# Please create a script called diff_json.sh that is executed with ./diff_json.sh json_old json_new and outputs the difference between json_old and json_new in Markdown format. The detailed specifications are as follows:

# Input Format:
# json_old and json_new are both plain JSON strings where keys are strings, and values are objects in the format { cc: float, hal: float, sloc: float, mi_raw: float, mi_pct: float }. 
# Since the input JSON strings may use a mix of single quotes (') and double quotes ("), you need to preprocess them to ensure all quotes are converted to double quotes (").

# Difference Calculation:
# For keys that are present in both json_old and json_new, calculate the difference (json_new value - json_old value) for the fields cc, hal, sloc, and mi_raw.
# If a key is present in only one of the JSONs, assume the value of the missing key is 0 during the calculation.

# Special Handling for mi_pct:
# The mi_pct field should not be calculated as a difference. Instead, directly display the mi_pct value from json_new.
# If a key is present only in json_old, leave the mi_pct column blank.

# Output Format:
# If the diffs of cc, hal and sloc is all 0 (unchanged) then the record is skipped.
# The output should be a Markdown table with the following columns:
# | Key |  | diff cc | diff hal | diff sloc | diff mi_raw | new_mi_pct |.

# The Key column displays the key from the JSONs. 
# The second column displays if the file was Added (Add), Deleted (Del), or Updated (Upd) based on the presence of the key in json_old and json_new.
# Columns diff cc, diff hal, diff sloc, and diff mi_raw display the calculated differences for each respective field.
# The new_mi_pct column displays the mi_pct value from json_new. If a key only exists in json_old, this column should be left blank.

# Summary Row:
# Add a summary row at the end of the Markdown table to show the total differences for cc, hal, sloc, and mi_raw. mi_pct should be blank.
# Use **total** as the value in the Key column for this row.

# Output Formatting:
# The entire output should be enclosed in a collapsible Markdown <details> tag with the following format:
# markdown
# <details>
# <summary>Code Complexity Analytics</summary>

# { Output the Markdown table here. All the float values should be rounded to 1st decimal place }
# </details>


# This formatting ensures that the output is neatly presented in a compact format that can be expanded for detailed viewing.
#------

#!/bin/bash

# Input arguments
json_old=$1
json_new=$2

# Convert single quotes to double quotes and store in temporary files
echo "$json_old" | sed "s/'/\"/g" > old.json
echo "$json_new" | sed "s/'/\"/g" > new.json

# Read the JSONs into variables
old_content=$(cat old.json)
new_content=$(cat new.json)

# Create associative arrays for both old and new JSON data
declare -A old_data
declare -A new_data

# Parse old JSON content
for key in $(jq -r 'keys[]' old.json); do
  values=$(jq -r ".[\"$key\"] | [.cc, .hal, .sloc, .mi_raw, .mi_pct] | @csv" old.json)
  old_data[$key]=$values
done

# Parse new JSON content
for key in $(jq -r 'keys[]' new.json); do
  values=$(jq -r ".[\"$key\"] | [.cc, .hal, .sloc, .mi_raw, .mi_pct] | @csv" new.json)
  new_data[$key]=$values
done

# Initialize variables for table content and totals
table=""
total_cc=0.0
total_hal=0.0
total_sloc=0.0
total_mi_raw=0.0

# Iterate through all keys in both old and new data
for key in $(echo "${!old_data[@]} ${!new_data[@]}" | tr ' ' '\n' | sort -u); do
  old_values=${old_data[$key]:-0.0,0.0,0.0,0.0,}
  new_values=${new_data[$key]:-0.0,0.0,0.0,0.0,}
  
  IFS=',' read -r old_cc old_hal old_sloc old_mi_raw old_mi_pct <<< "$old_values"
  IFS=',' read -r new_cc new_hal new_sloc new_mi_raw new_mi_pct <<< "$new_values"
  
  # Calculate differences
  diff_cc=$(echo "$new_cc - $old_cc" | bc -l)
  diff_hal=$(echo "$new_hal - $old_hal" | bc -l)
  diff_sloc=$(echo "$new_sloc - $old_sloc" | bc -l)
  diff_mi_raw=$(echo "$new_mi_raw - $old_mi_raw" | bc -l)
  
  # Format values to 1 decimal place
  diff_cc=$(printf "%.1f" "$diff_cc")
  diff_hal=$(printf "%.1f" "$diff_hal")
  diff_sloc=$(printf "%.1f" "$diff_sloc")
  diff_mi_raw=$(printf "%.1f" "$diff_mi_raw")
  new_mi_pct=$(printf "%.1f" "$new_mi_pct")

  # Determine if we should display this row (skip unchanged rows)
  if [[ "$diff_cc" == "0.0" && "$diff_hal" == "0.0" && "$diff_sloc" == "0.0" ]]; then
    continue
  fi

  # Determine the status of the key (Add, Del, Upd)
  if [[ -z "${old_data[$key]}" ]]; then
    status="Add"
  elif [[ -z "${new_data[$key]}" ]]; then
    status="Del"
  else
    status="Upd"
  fi

  # Add to total calculations
  total_cc=$(echo "$total_cc + $diff_cc" | bc -l)
  total_hal=$(echo "$total_hal + $diff_hal" | bc -l)
  total_sloc=$(echo "$total_sloc + $diff_sloc" | bc -l)
  total_mi_raw=$(echo "$total_mi_raw + $diff_mi_raw" | bc -l)

  # Add to the Markdown table
  table+="| $key | $status | $diff_cc | $diff_hal | $diff_sloc | $diff_mi_raw | $new_mi_pct |\n"
done

# Format total values to 1 decimal place
total_cc=$(printf "%.1f" "$total_cc")
total_hal=$(printf "%.1f" "$total_hal")
total_sloc=$(printf "%.1f" "$total_sloc")
total_mi_raw=$(printf "%.1f" "$total_mi_raw")

# Add the summary row
table+="| **total** | | **$total_cc** | **$total_hal** | **$total_sloc** | **$total_mi_raw** | |\n"

# Output in collapsible Markdown format
echo -e "<details>\n<summary>Code Complexity Analytics</summary>\n\n"
echo -e "| Key |  | diff cc | diff hal | diff sloc | diff mi_raw | new_mi_pct |"
echo -e "| --- | --- | --- | --- | --- | --- | --- |"
echo -e "$table"
echo -e "</details>"

# Clean up temporary files
rm old.json new.json