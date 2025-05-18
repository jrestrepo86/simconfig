import itertools
import re
import time
from copy import deepcopy


def set_simulations(simconfig_vars, content):
    root_dir = simconfig_vars["root-path"]
    base_name = simconfig_vars["name"]
    extension = simconfig_vars["extension"]

    # enviroment
    if "venv" in simconfig_vars:
        env_type = simconfig_vars["venv"].get("type", "venv")
        if env_type == "conda":
            env_name = simconfig_vars["venv"].get("env-name", "base")
        elif env_type == "venv":
            env_name = simconfig_vars["venv"].get("env-name", None)
        else:
            env_name = None
    else:
        env_type = "venv"
        env_name = None

    # variables values
    variables_names = list(simconfig_vars["variables"].keys())
    variables_values = list(simconfig_vars["variables"].values())

    param_combinations = list(itertools.product(*variables_values))
    realization_name = list(simconfig_vars["realizations"].keys())
    realization_values = list(simconfig_vars["realizations"].values())[0]
    realization_values = list(range(1, realization_values + 1))
    sims = []
    for params in param_combinations:
        vars_ = dict(zip(variables_names, params))

        for realization in realization_values:
            full_path, launcher_group = set_sim_filename(
                vars_, realization, base_name, root_dir, extension
            )

            sim = {
                "full-path": full_path,
                "launcher-group": launcher_group,
                "filename": full_path.name,
                "variables": vars_,
                "realization": dict(zip(realization_name, [realization])),
                "executable": (
                    simconfig_vars["pyexecutable"]
                    if extension == ".py"
                    else simconfig_vars["matexecutable"]
                ),
                "extension": extension,
                "comment-string": "#" if extension == ".py" else "%",
                "content": "",
                "env-type": env_type,
                "env-name": env_name,
            }
            mod_content = set_sim_content(content, sim)
            sim["content"] = mod_content

            sims.append(sim)

    write_sim_files(sims)
    return sims


def set_sim_filename(variables, realization, base_name, root_dir, extension):
    variables_names = list(variables.keys())
    variables_values = list(variables.values())
    # Process variables (all except last)
    var_codes = [
        f"{key[0].upper()}{val}" for key, val in zip(variables_names, variables_values)
    ]
    # Process realization (last value with zero-padding)
    realization = f"{realization:02d}"

    # Build filename components
    file_tag = "_".join(var_codes + [realization])
    dir_tag = "_".join(var_codes)
    # Create full paths
    full_path = root_dir / f"{dir_tag}" / f"{base_name}_{file_tag}{extension}"
    return full_path, dir_tag


def set_sim_content(content, sim_info):
    """
    d
    """
    # Create a working copy to avoid modifying original content
    date = time.strftime("%d/%m/%Y")
    content_copy = deepcopy(content)

    # Extract required components from sim_info
    variables = sim_info["variables"]
    realization = sim_info["realization"]
    filename = sim_info["filename"]
    comment_string = sim_info["comment-string"]

    # Process replacements in specified order
    for replacement_dict in [variables, realization]:
        for key, value in replacement_dict.items():
            # Compile pattern once per key
            pattern = re.compile(
                rf"^\s*{re.escape(key)}\s*=\s*.*?(?=\s*(#|$))", re.IGNORECASE
            )

            # Search through copy content
            for i, line in enumerate(content_copy):
                if pattern.search(line):
                    # Preserve any existing inline comments
                    comment_match = re.search(r"\s*(#.*)$", line)
                    comment = comment_match.group(1) if comment_match else ""
                    content_copy[i] = (
                        f"{key}={value}{' ' + comment if comment else ''}\n"
                    )
                    break  # Stop after first match

    # Add header comment (using list concatenation for clarity)
    content_copy = (
        [f"{comment_string} {filename}\n"]
        + content_copy
        + [f"\n\n# Generado automaticamente por SimConfig - {date}"]
    )

    return content_copy


def write_sim_files(sims):
    for sim in sims:
        full_path = sim["full-path"]
        output_dir = full_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf8") as file:
            file.writelines(sim["content"])
