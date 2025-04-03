import copy
import time


def set_slurm_files(sims, slurm_config):
    for sim in sims:
        sim["slurm-filename"] = set_slurm_filename(sim)
        sim["slurm-content"] = set_slurm_content(sim, slurm_config)
        write_slurm_sbatch_files(sim)
    return sims


def set_slurm_filename(sim):
    fullpath = sim["full-path"]
    output_dir = fullpath.parent
    filename = fullpath.stem
    slurm_filename = output_dir / "SBATCH" / f"{filename}.sh"
    return slurm_filename


def set_slurm_content(sim, slurm_config):
    date = time.strftime("%d/%m/%Y")
    fullpath = sim["full-path"]
    output_dir = fullpath.parent
    executable = sim["executable"]
    env_type = sim["env-type"]
    env_name = sim["env-name"]

    host_name = slurm_config["host-name"]

    slurm_options = copy.deepcopy(slurm_config.get(host_name))

    if slurm_options is None:
        slurm_options = copy.deepcopy(slurm_config.get("neptuno"))

    # set slurm error file path
    if "error" not in slurm_options:
        slurm_options.append(f"error={output_dir}job.%J.err")
    # set slurm output file path
    if "output" not in slurm_options:
        slurm_options.append(f"output={output_dir}job.%J.out")

    # options to content
    slurm_content = ["#!bin/sh"] + [f"## hostname: {host_name}"]
    for opt in slurm_options:
        slurm_content.append(f"#SBATCH --{opt}")

    # set conda env
    if env_type == "conda" and "python" in executable:
        slurm_content += set_conda_env(env_name)

    slurm_content += set_run_content(fullpath, executable)
    slurm_content += [f"\n\n# Generado automaticamente por SimConfig - {date}"]
    slurm_content = "\n".join(slurm_content)
    return slurm_content


def set_conda_env(env_name):
    conda_content = []
    locate_conda = """
# ---- Automatically locate conda.sh ----
# Method 1: Check common installation paths
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    . "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    . "$HOME/anaconda3/etc/profile.d/conda.sh"
# Method 2: Use conda info (if conda is in PATH)
elif command -v conda &>/dev/null; then
    CONDA_BASE=$(conda info --base 2>/dev/null)
    if [ -n "$CONDA_BASE" ]; then
        . "$CONDA_BASE/etc/profile.d/conda.sh"
    else
        echo "Error: Failed to find conda.sh" >&2
        exit 1
    fi
else
    echo "Error: conda.sh not found in standard locations" >&2
    exit 1
fi
"""
    conda_content.append(locate_conda)
    # activate environment
    conda_content.append("# Activate environment")
    conda_content.append(f"conda activate {env_name}")

    return conda_content


def set_run_content(fullpath, executable):

    sim_dir = fullpath.parent
    filename = fullpath.name
    sim_name = fullpath.stem
    run_content = [f"cd {sim_dir}"]
    run_content.append(f"chmod u+w {fullpath}")
    run_content.append("export PYTHONUNBUFFERED=1")
    # stdout
    out_filename = sim_dir / f"out_{sim_name}.txt"
    err_filename = sim_dir / f"err_{sim_name}.txt"
    # execute line
    exec_line = f"{executable} {filename} >{out_filename} 2>{err_filename} &"
    run_content.append(exec_line)
    return run_content


def write_slurm_sbatch_files(sim):
    fullpath = sim["slurm-filename"]
    sbatch_dir = fullpath.parent
    sbatch_dir.mkdir(parents=True, exist_ok=True)
    with open(fullpath, "w", encoding="utf8") as file:
        file.writelines(sim["slurm-content"])
