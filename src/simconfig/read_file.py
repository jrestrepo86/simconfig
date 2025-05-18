"""read file config"""

import ast
import re
import socket
import subprocess
from pathlib import Path

from simconfig.simconfig_variables import simconfig_vars, slurm_config


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
    simconfig_vars["root-path"] = filename.parent / "simulation"
    simconfig_vars["extension"] = filename.suffix

    # Normalize venv config early
    venv = simconfig_vars.get("venv", {})
    venv_type = venv.get("type", "venv")
    venv_name = venv.get("env-name")

    if venv_type == "conda":
        if not venv_name or not isinstance(venv_name, str) or not venv_name.strip():
            venv_name = "base"
    elif venv_type == "venv":
        if not venv_name or not isinstance(venv_name, str) or not venv_name.strip():
            venv_name = None
    else:
        venv_type = "venv"
        venv_name = None

    if venv_type == "venv" and venv_name is not None:
        venv_path = Path(venv_name).expanduser().resolve()
        if not (venv_path / "bin" / "activate").exists():
            print(
                f"⚠️ Warning: Virtual environment not found at {venv_path}/bin/activate — the script will continue."
            )
    elif venv_type == "conda" and venv_name:
        try:
            output = subprocess.check_output(
                ["conda", "info", "--envs"], stderr=subprocess.DEVNULL, text=True
            )
            if not any(
                line.split()[0] == venv_name
                for line in output.splitlines()
                if line and not line.startswith("#")
            ):
                print(
                    f"⚠️ Warning: Conda environment '{venv_name}' not found in `conda info --envs` — continuing anyway."
                )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(
                "⚠️ Warning: Could not verify Conda environment (is Conda installed and in PATH?)."
            )

    simconfig_vars["venv"] = {"type": venv_type, "env-name": venv_name}

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
