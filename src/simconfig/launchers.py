import time


def make_launcher(sims, simconfig_vars):
    sim_name = simconfig_vars["name"]
    root_path = simconfig_vars["root-path"]
    job_scripts_dir = root_path / "launchers" / "jobs"
    job_scripts_dir.mkdir(parents=True, exist_ok=True)

    launcher_groups = {}
    for sim in sims:
        launcher_group, content = generate_individual_job_script(
            sim, job_scripts_dir, simconfig_vars
        )
        if launcher_group not in launcher_groups:
            launcher_groups[launcher_group] = []
        launcher_groups[launcher_group].append(sim)

    launcher_files = write_group_launchers(launcher_groups, root_path)
    make_runfile(sim_name, root_path, launcher_files, simconfig_vars)


def generate_individual_job_script(sim, job_scripts_dir, simconfig_vars):
    launcher_group = sim["launcher-group"]
    slurm_filename = sim["slurm-filename"]
    process_name = slurm_filename.stem

    job_script_path = job_scripts_dir / f"{process_name}.sh"

    log_per_group = simconfig_vars.get("log-per-group", True)
    if log_per_group:
        log_path = f'$(dirname "$0")/../../logs/launchers/{launcher_group}.log'
    else:
        log_path = f'$(dirname "$0")/../../logs/launchers/{process_name}.log'

    job_path = f'$(dirname "$0")/../../{slurm_filename.relative_to(job_scripts_dir.parent.parent)}'

    content = f"""#!/bin/sh
# Proceso {process_name}

start_time=$(date +%s)
mkdir -p $(dirname \"{log_path}\")
echo "[$(date +'%Y-%m-%d %H:%M:%S')] Lanzando proceso: {process_name}" >> {log_path}

if [ -f "{job_path}" ]; then
    sbatch "{job_path}"
    status=$?
    if [ "$status" -eq 0 ]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] ✓ Enviado: {process_name}" >> {log_path}
    else
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] ❌ Error al enviar: {process_name} (code=$status)" >> {log_path}
    fi
else
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️ Archivo no encontrado: {job_path}" >> {log_path}
fi

end_time=$(date +%s)
duration=$((end_time - start_time))
echo "[$(date +'%Y-%m-%d %H:%M:%S')] ⏱️ Duración: $duration s para {process_name}" >> {log_path}
sleep 0.3
"""

    with open(job_script_path, "w", encoding="utf-8") as f:
        f.write(content)

    return launcher_group, content


def write_group_launchers(groups, root_path):
    launcher_dir = root_path / "launchers"
    date = time.strftime("%d/%m/%Y")
    launcher_files = []

    for group, sims in groups.items():
        lines = ["#!/bin/sh", f"# Lanzador de grupo: {group}"]
        for sim in sims:
            process_name = sim["slurm-filename"].stem
            job_script_path = f'$(dirname "$0")/jobs/{process_name}.sh'
            lines.append(f"bash {job_script_path}")

        lines.append(f"# Generado automaticamente por SimConfig - {date}")
        full_path = launcher_dir / f"{group}.sh"
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        launcher_files.append(full_path)

    return launcher_files


def make_runfile(sim_name, root_path, launchers_filenames, simconfig_vars):
    filename = root_path / f"run_{sim_name}.sh"
    date = time.strftime("%d/%m/%Y")
    content = ["#!/bin/sh"]

    # Conda environment activation
    env = simconfig_vars.get("venv", {})
    env_type = env.get("type", "conda")
    env_name = env.get("conda-env", "base")

    if env_type == "conda":
        content += [
            "# ---- Conda Environment Activation ----",
            'if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then',
            '    . "$HOME/miniconda3/etc/profile.d/conda.sh"',
            'elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then',
            '    . "$HOME/anaconda3/etc/profile.d/conda.sh"',
            "elif command -v conda &>/dev/null; then",
            "    CONDA_BASE=$(conda info --base 2>/dev/null)",
            '    . "$CONDA_BASE/etc/profile.d/conda.sh"',
            "else",
            '    echo "Error: conda.sh not found" >&2',
            "    exit 1",
            "fi",
            f"conda activate {env_name}",
            "",
        ]

    for launcher in launchers_filenames:
        launcher_name = launcher.stem
        relative_path = launcher.relative_to(root_path)
        content.append("\n#==========================================")
        content.append(f"# {launcher_name}")
        content.append(f'bash "$(dirname "$0")/{relative_path}"')

    content.append("\nsqueue")
    content.append(f"# Generado automaticamente por SimConfig - {date}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
