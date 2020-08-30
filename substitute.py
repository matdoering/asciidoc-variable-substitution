"""Substitution of Strings in AsciiDoc."""

from string import Template

def build_adoc_table_from_dict(col_entries: dict) -> str:
    """Creates an adoc table from a dictionary.

    Args:
        col_entries (dict[str]): Dictionary with a list of values for the column names.

    Returns:
        str: An adoc table as a string.
    """
    # sort columns
    columns = list(col_entries.keys())
    columns.sort()

    # generate the header
    header: str = f'|{" |".join(columns)}'

    # create the table content
    n_rows = len(list(col_entries.values())[0])
    rows = []
    for row_i in range(n_rows):
        row = ""
        for column in columns:
            value = col_entries[column][row_i]
            row += f'|{value}\n'
        rows.append(row)
    table_content = '\n'.join(rows)

    # store the table
    adoc_table = f'|===\n{header}\n\n{table_content}\n|==='
    return adoc_table

def create_substitution_for(var, col_entries):
    """Generates the substitution text for the input variable.

    Args:
        var (str): name of the variable to be replaced
        col_entries (dict): mapping from column names to list of column entries

    Returns:
        str: text that shall replace the variable
    """
    if var == "reward_agents_table":
        return build_adoc_table_from_dict(col_entries)
    else:
        print(f"Warning: No substitution implemented for variable '{var}'.")
        return ""

def substitute(template_fname, col_entries):
    """Substitutes the input variables in the specified file.

    Stores the result in an output file with the name 'result.adoc.'.

    Args:
        template_fname (str): Filename of the AsciiDoc template file for which vars should be replaced.
        col_entries (dict): mapping from column names to list of column entries
    """
    substitutions = {}
    vars = ["reward_total_table", "reward_agents_table", "custom_metrics_table"]
    for var in vars:
        substitutions[var] = create_substitution_for(var, col_entries)

    template = Template(open(template_fname).read())
    report = template.substitute(substitutions)
    with open("result.adoc", "w") as out_file:
        out_file.write(report)


col_entries_agents = {'agent': ['Pacman_0', 'Pacman_1', 'Pacman_2'],
                      'policy_reward_max': ['12.0', '24.0', '23.0'],
                      'policy_reward_mean': ['11.15', '23.81', '21.75'],
                      'policy_reward_min': ['9.0', '21.0', '12.0']
                     }
substitute('template.adoc', col_entries_agents)
