from bs4 import BeautifulSoup
from math import gcd
from functools import reduce
import re
from collections import defaultdict 

html_content = """
<table border='1'>
	<tr>
		<td> Main Topic </td>
	</tr>
	<tr>
		<td>
			<table border='1'>
				<tr>
					<td>Section 1</td>
					<td>Section 2</td>
				</tr>
				<tr>
					<td>
						<table border='1'>
							<tr>
								<td>SubSec 1.1</td>
								<td>SubSec 1.2</td>
								<td>SubSec 1.3</td>
							</tr>
							<tr>
								<td>Item 1.1</td>
								<td>Item 1.2</td>
								<td>Item 1.3</td>
							</tr>
							<tr>
								<td>
									<table border='1'>
										<tr>
											<td>Detail 1.3.1</td>
											<td>Detail 1.3.2</td>
										</tr>
									</table>
								</td>
								<td>Item 1.3.2</td>
								<td>Item 1.3.3</td>
							</tr>
						</table>
					</td>
					<td>Content 2.1</td>
				</tr>
				<tr>
					<td>Section 3</td>
					<td>
						<table border='1'>
							<tr>
								<td>Detail 3.1</td>
								<td>Detail 3.2</td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
		</td>
	</tr>
</table>

"""

# html_content = """
# <table border>
#   <tr>
#     <td colspan="4">Main Table Header</td>
#   </tr>
#   <tr>
#     <td colspan="2">
#       <table border>
#         <tr>
#           <td colspan="2">Nested Table 1 Header</td>
#         </tr>
#         <tr>
#           <td>Cell 1.1</td>
#           <td>Cell 1.2</td>
#         </tr>
#         <tr>
#           <td>Cell 1.3</td>
#           <td>Cell 1.4</td>
#         </tr>
#       </table>
#     </td>
#     <td colspan="2">
#       <table border>
#         <tr>
#           <td colspan="2">Nested Table 2 Header</td>
#         </tr>
#         <tr>
#           <td colspan="2">Nested Table 3 Header</td>
#         </tr>
#         <tr>
#           <td>Cell 1.3</td>
#           <td>Cell 1.4</td>
#         </tr>
#       </table>
#     </td>
#   </tr>
#   <tr>
#     <td>Main Cell 1</td>
#     <td>Main Cell 2</td>
#     <td>Main Cell 3</td>
#     <td>Main Cell 4</td>
#   </tr>
# </table>
# """

# html_content = """
# 			<table class="style1">
# 				<tbody>
# 					<tr>
# 						<td class="style2">
# 							<strong>Natasha's Pattern</strong>

# 							<table class="style3">
# 								<thead>
# 									<tr>
# 										<th>Term</th>
# 										<th>Number</th>
# 									</tr>
# 								</thead>
# 								<tbody>
# 									<tr>
# 										<td class="style4">1</td>
# 										<td class="style4">1</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">2</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE11" shuffle="false">
# 												<inlineChoice identifier="a1">4</inlineChoice>
# 												<inlineChoice identifier="a2">5</inlineChoice>
# 												<inlineChoice identifier="a3">9</inlineChoice>
# 												<inlineChoice identifier="a4">10</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">3</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE12" shuffle="false">
# 												<inlineChoice identifier="a1">9</inlineChoice>
# 												<inlineChoice identifier="a2">16</inlineChoice>
# 												<inlineChoice identifier="a3">19</inlineChoice>
# 												<inlineChoice identifier="a4">81</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">4</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE13" shuffle="false">
# 												<inlineChoice identifier="a1">14</inlineChoice>
# 												<inlineChoice identifier="a2">28</inlineChoice>
# 												<inlineChoice identifier="a3">64</inlineChoice>
# 												<inlineChoice identifier="a4">729</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 								</tbody>
# 							</table>
# 						</td>
# 						<td class="style5">&#160;</td>
# 						<td class="style2">
# 							<strong>Jason's Pattern</strong>
# 							<table class="style3">
# 								<thead>
# 									<tr>
# 										<th>Term</th>
# 										<th>Number</th>
# 									</tr>
# 								</thead>
# 								<tbody>
# 									<tr>
# 										<td class="style4">1</td>
# 										<td class="style4">1</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">2</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE14" shuffle="false">
# 												<inlineChoice identifier="a1">4</inlineChoice>
# 												<inlineChoice identifier="a2">5</inlineChoice>
# 												<inlineChoice identifier="a3">9</inlineChoice>
# 												<inlineChoice identifier="a4">10</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">3</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE15" shuffle="false">
# 												<inlineChoice identifier="a1">9</inlineChoice>
# 												<inlineChoice identifier="a2">16</inlineChoice>
# 												<inlineChoice identifier="a3">19</inlineChoice>
# 												<inlineChoice identifier="a4">81</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 									<tr>
# 										<td class="style4">4</td>
# 										<td class="style4">
# 											<inlineChoiceInteraction responseIdentifier="RESPONSE16" shuffle="false">
# 												<inlineChoice identifier="a1">14</inlineChoice>
# 												<inlineChoice identifier="a2">28</inlineChoice>
# 												<inlineChoice identifier="a3">64</inlineChoice>
# 												<inlineChoice identifier="a4">729</inlineChoice>
# 											</inlineChoiceInteraction>
# 										</td>
# 									</tr>
# 								</tbody>
# 							</table>
# 						</td>
# 					</tr>
# 				</tbody>
# 			</table>
# """


def table_to_dict(table):
    result = {"table": {}}
    sections = table.find_all(['tbody', 'thead', 'tfoot'], recursive=False) or [table]
    rows = [tr for section in sections for tr in section.find_all('tr', recursive=False)]
    for row_index, row in enumerate(rows):
        row_key = f"row{row_index + 1}"
        result["table"][row_key] = {}
        for col_index, col in enumerate(row.find_all(['td', 'th'], recursive=False)):
            col_key = f"col{col_index + 1}"
            nested_table = col.find('table', recursive=False)
            if nested_table:
                # Process nested tables recursively
                result["table"][row_key][col_key] = table_to_dict(nested_table)
            else:
                # Get text from cell, ensuring to strip any excess whitespace
                result["table"][row_key][col_key] = {
                    "cell":  str(col.find()) if col.find() else col.get_text(strip=True),
                    "colspan": col.get('colspan',1),
                    "rowspan": col.get('rowspan',1)
                  }
    return result

def calc_new_row_count(data):
    # Find all tr and table tags
    tr_tags = soup.find_all('tr')
    table_tags = soup.find_all('table')

    # Calculate the difference
    difference = len(tr_tags) - len(table_tags)

    # Return the count
    return difference - 1

def create_new_table_struct(new_table_row_count):
    new_table = {'table':{}}
    for i in range(1,new_table_row_count + 1):
        new_table['table'][f'row{i}'] = {}
    return new_table

def map_new_table(new_table,input_dict):
    def flatten_table(input_dict, new_table):
        process_rows(input_dict['table'], new_table, 1, "table")  # Start with the root table

    def process_rows(node, new_table, start_row, path):
        row_counter = start_row

        for row_name, columns in node.items():
            row_path = f"{path}/{row_name}"  # Append the current row to the path
            col_counter = 1
            max_row_span = 1

            for col_name, content in columns.items():
                if "cell" in content:
                    # Handle simple cell
                    cell_path = f"{row_path}/{col_name}"
                    add_cell_to_table(new_table, row_counter, col_counter, content['cell'], content['rowspan'], content['colspan'], cell_path)
                    col_counter += 1
                elif "table" in content:
                    # Handle nested table
                    nested_table_path = f"{row_path}/{col_name}/table"
                    nested_table_info = process_nested_table(content['table'], new_table, row_counter, col_counter, nested_table_path)
                    col_counter += nested_table_info['colspan']
                    max_row_span = max(max_row_span, nested_table_info['rowspan'])

            row_counter += max_row_span

    def process_nested_table(nested_node, new_table, start_row, start_col, path):
        total_rows = 0
        max_col = 0

        for row_name, columns in nested_node.items():
            row_path = f"{path}/{row_name}"
            col_counter = start_col
            row_span = 1

            for col_name, content in columns.items():
                if "cell" in content:
                    cell_path = f"{row_path}/{col_name}"
                    add_cell_to_table(new_table, start_row + total_rows, col_counter, content['cell'], content['rowspan'], content['colspan'], cell_path)
                    col_counter += 1
                elif "table" in content:
                    nested_table_path = f"{row_path}/{col_name}/table"
                    nested_info = process_nested_table(content['table'], new_table, start_row + total_rows, col_counter, nested_table_path)
                    col_counter += nested_info['colspan']
                    row_span = max(row_span, nested_info['rowspan'])

            total_rows += row_span
            max_col = max(max_col, col_counter - start_col)

        return {'rowspan': total_rows, 'colspan': max_col}

    def add_cell_to_table(new_table, row, col, value, rowspan, colspan, path):
        row_key = f"row{row}"
        col_key = f"col{col}"

        if row_key not in new_table['table']:
            new_table['table'][row_key] = {}

        new_table['table'][row_key][col_key] = {
            "cell": value,
            "colspan": colspan,
            "rowspan": rowspan,
            "path": path  # Record the path to the cell
        }
    
    flatten_table(input_dict, new_table)

    return new_table

def dict_to_html_table(data,path_col_dict=None,path_row_dict=None):
    # Start the HTML table
    html = '<table border="1">'
    
    # Iterate through each row in the dictionary
    for row_key in sorted(data.keys()):
        html += '<tr>'
        # Sort columns by key to ensure proper order in cases like col10, col2, etc.
        sorted_columns = sorted(data[row_key].items(), key=lambda x: int(x[0][3:]))
        # Iterate through each column in the row
        for col_key, col_data in sorted_columns:
            # Extract cell data
            cell = col_data['cell']
            colspan = (path_col_dict and path_col_dict[col_data['path']]) or 1
            rowspan = (path_row_dict and path_row_dict[col_data['path']]) or 1
            # Append the cell to the row in HTML format
            html += f'<td colspan="{colspan}" rowspan="{rowspan}">{cell}</td>'
        html += '</tr>'
    # Close the HTML table tag
    html += '</table>'
    
    return html

def extract_paths_from_dict(d, current_path=""):
    paths = []
    for key, value in d.items():
        new_path = f"{current_path}/{key}"
        if isinstance(value, dict):
            if 'path' in value:
                paths.append( value['path'])
            paths.extend(extract_paths_from_dict(value, new_path))
    return paths

def clean_table(new_table):
    tem = {'table':{}}
    # Iterating over a copy of keys
    for k, v in list(new_table['table'].items()):
        if v:
            tem['table'][k] = v
            # Iterating over a copy of keys
            for x in list(v.keys()):
                if tem['table'][k][x]['cell'] == '':
                    del tem['table'][k][x]
    return tem

################### COLS ZONE ################################

class TreeNode:
    def __init__(self, value=1, parent=None, path=''):
        self.value = value
        self.children = []
        self.parent = parent
        self.path = path 

def add_child(parent, child_value=1, child_path=''):
    # Create a new child node with the current parent as its parent
    child = TreeNode(value=child_value, parent=parent, path=child_path)
    parent.children.append(child)
    return child

def assign_initial_values(root):
    # Compute the depth of the tree
    depth = max_depth(root)
    # Gather nodes at the bottom-most level
    bottom_nodes = get_nodes_at_level(root, depth)
    # Determine the most populous level
    most_nodes = max([len(n.parent.children) for n in  bottom_nodes])

    # Calculate values based on the proportion of most_nodes to the count of nodes in each group
    for node in bottom_nodes:
        node.value = most_nodes / len(node.parent.children)

def max_depth(node, current_depth=1):
    if not node.children:
        return current_depth
    return max(max_depth(child, current_depth + 1) for child in node.children)

def get_nodes_at_level(node, target_level, current_level=1):
    if current_level == target_level:
        return [node]
    
    nodes = []
    if node.children:
        for child in node.children:
            nodes.extend(get_nodes_at_level(child, target_level, current_level + 1))
    return nodes

def aggregate_values(root):
    depth_values = {}
    aggregate_node_values(root, 0, depth_values)
    adjust_leaf_nodes(depth_values,root)

def aggregate_node_values(node, current_depth, depth_values):
    if not node.children:
        node.value = node.value  # Retain original value for leaf nodes
    else:
        # Sum values for non-leaf nodes
        node.value = sum(aggregate_node_values(child, current_depth + 1, depth_values) for child in node.children)
    
    # Store nodes by depth
    if current_depth in depth_values:
        depth_values[current_depth].append(node)
    else:
        depth_values[current_depth] = [node]
    
    return node.value

def adjust_leaf_nodes(depth_values,root):
    max_depths = max(depth_values.keys())
    for depth, nodes in depth_values.items():
        if depth == max_depths:
            continue  # Skip adjustment for the bottom-most leaves
        
        average_value = sum(node.value for node in nodes if node.children) / len([node for node in nodes if node.children]) if any(node.children for node in nodes) else sum(node.value for node in nodes) / len(nodes)
        
        for node in nodes:
            if not node.children :
                node.value = average_value / len(node.parent.children)

def print_tree(node, level=0):
    print(' ' * 4 * level + '->', node.value)
    for child in node.children:
        print_tree(child, level + 1)

def build_tree_from_paths(paths):
    root = TreeNode(path="root")  # Start with a root path
    nodes = {"root": root}  # Root path is "root"

    for path in paths:
        parts = path.split('/')
        current_path = "root"
        current_node = root

        for part in parts:
            if part:  # Skip any empty parts from splitting
                current_path += '/' + part
                if current_path not in nodes:
                    nodes[current_path] = add_child(current_node, child_path=current_path)
                current_node = nodes[current_path]

    return root

def generate_path_value_dict(node, path_value_dict=None):
    if path_value_dict is None:
        path_value_dict = {}
    
    # Store the current node's path and value
    path_value_dict[node.path] = node.value
    
    # Recursively do this for all children
    for child in node.children:
        generate_path_value_dict(child, path_value_dict)

    return path_value_dict

###################################################


soup = BeautifulSoup(html_content, 'html.parser')
main_table = soup.find('table')

table_dict = table_to_dict(main_table)
print(table_dict)

new_table_row_count = calc_new_row_count(table_dict)
print("new_table_row_count:", new_table_row_count)

new_table = create_new_table_struct(new_table_row_count)
print(new_table)

new_table = map_new_table(new_table,table_dict)
print(new_table)

paths = extract_paths_from_dict(new_table)
print(paths)

root = build_tree_from_paths(paths)
print_tree(root)

assign_initial_values(root)
print_tree(root)

[aggregate_values(root) for i in range(10)]
print_tree(root)

path_value_dict = generate_path_value_dict(root)
print(path_value_dict)

path_value_dict = {k[5:]:v for k,v in path_value_dict.items() if k[5:] in paths}
print(path_value_dict)

new_table = clean_table(new_table)
print(new_table)

html_table = dict_to_html_table(new_table['table'],path_value_dict)
print(html_table)

stop = 0
