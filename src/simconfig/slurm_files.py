import copy
import time

from pathlib import Path


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
    executable = sim["executable"]

    host_name = slurm_config["host-name"]

    slurm_options = copy.deepcopy(slurm_config.get(host_name))

    if slurm_options is None:
        slurm_options = copy.deepcopy(slurm_config.get("neptuno"))

    # # set slurm error file path
    # if not any(opt.startswith("error=") for opt in slurm_options):
    #     slurm_options.append("error=job.%J.err")
    # # set slurm output file path
    # if not any(opt.startswith("output=") for opt in slurm_options):
    #     slurm_options.append("output=job.%J.out")

    # options to content
    slurm_content = ["#!/bin/sh"] + [f"## hostname: {host_name}"]
    for opt in slurm_options:
        slurm_content.append(f"#SBATCH --{opt}")

    slurm_content += set_run_content(fullpath, executable)
    slurm_content += [f"\n\n# Generado automaticamente por SimConfig - {date}"]
    slurm_content = "\n".join(slurm_content)
    return slurm_content


def set_run_content(fullpath, executable):
    filename = fullpath.name
    sim_name = fullpath.stem
    sim_dir = Path(fullpath.parent).resolve()

    return [
        f'cd "{sim_dir}" || exit 1',
        f"chmod u+w {filename}",
        "export PYTHONUNBUFFERED=1",
        f"{executable} {filename} > out_{sim_name}.txt 2> err_{sim_name}.txt",
    ]


def write_slurm_sbatch_files(sim):
    fullpath = sim["slurm-filename"]
    sbatch_dir = fullpath.parent
    sbatch_dir.mkdir(parents=True, exist_ok=True)
    with open(fullpath, "w", encoding="utf8") as file:
        file.writelines(sim["slurm-content"])
