"""read file config"""

import ast
import re
import socket
from pathlib import Path

from src.simconfig_variables import simconfig_vars, slurm_config


def parse_sim_config(filename):
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()

    in_sim_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == "[SimConfig]":
            in_sim_section = True
            continue
        if stripped == "[endSimConfig]":
            in_sim_section = False
            continue
        if in_sim_section:
            if stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip()
            try:
                # Handle the case where value might be a valid Python literal
                evaluated = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                # Fallback to string if evaluation fails (e.g., unquoted strings)
                evaluated = value
            simconfig_vars[key] = evaluated
    filename = Path(filename)
    simconfig_vars["source-filename"] = filename
    simconfig_vars["root-path"] = filename.parent
    simconfig_vars["extension"] = filename.suffix
    source_file_content = read_content(filename)
    slurm_config = read_slurm_config(filename)
    return simconfig_vars, slurm_config, source_file_content


def read_content(filename):
    with open(filename, "r", encoding="utf8") as file:
        content = file.readlines()

    content_temp = [x.strip() for x in content]
    start = content_temp.index("[endSlurmConfig]")
    content = content[start + 2 :]
    return content


def read_slurm_config(filename):
    local_slurm_config = {}
    with open(filename, "r", encoding="utf8") as f:
        content = f.read()

    # Locate the SlurmConfig section
    start = content.find("[SlurmConfig]")
    end = content.find("[endSlurmConfig]")
    if start == -1 or end == -1:
        return slurm_config
    slurm_section = content[start:end]

    # Use regex to find all host entries and their options
    pattern = r"""['"](.+?)['"]\s*:\s*\[(.*?)\]"""
    matches = re.findall(pattern, slurm_section, re.DOTALL)

    for host, options_str in matches:
        # Split options by commas and clean each option
        options = [opt.strip() for opt in options_str.split(",") if opt.strip()]
        local_slurm_config[host] = options
    # Update the global slurm_config with the local one
    for key, val in local_slurm_config.items():
        slurm_config[key] = val
    # get localhost
    local_host = socket.gethostname()
    slurm_config["host-name"] = local_host
    # slurm_config["host-name"] = "neptuno"

    return slurm_config
