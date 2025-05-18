import argparse
import time
from pathlib import Path

from simconfig.launchers import make_launcher
from simconfig.read_file import parse_sim_config
from simconfig.sim_files import set_simulations
from simconfig.slurm_files import set_slurm_files


def main():
    parser = argparse.ArgumentParser(
        description="SimConfig — SLURM Simulation Configuration and Launcher Generator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("file", type=Path, help="Config source file (.py or .m)")
    parser.add_argument(
        "--rewrite-only",
        action="store_true",
        help="Only regenerate simulation source files; skip SBATCH and launcher creation",
    )
    args = parser.parse_args()

    file_path = args.file
    date = time.strftime("%d/%m/%Y")

    simconfig_vars, slurm_vars, source_file_content = parse_sim_config(file_path)
    sims = set_simulations(simconfig_vars, source_file_content)

    if args.rewrite_only:
        print(
            f"🔁 Solo se reescribieron los archivos de simulación ({len(sims)} archivos actualizados)."
        )
    else:
        sims = set_slurm_files(sims, slurm_vars)
        make_launcher(sims, simconfig_vars)
        print(f"✅ Archivos generados con SimConfig ({date})")

    print("Autor: Juan F. Restrepo <juan.restrepo@uner.edu.ar>")


if __name__ == "__main__":
    main()
