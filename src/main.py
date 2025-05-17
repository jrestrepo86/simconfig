import argparse
import time
from pathlib import Path

from src.launchers import make_launcher
from src.read_file import parse_sim_config
from src.sim_files import set_simulations
from src.slurm_files import set_slurm_files


def main():
    parser = argparse.ArgumentParser(
        description="SimConfig — Simulation configuration and SLURM launcher generator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Input Python or MATLAB file containing [SimConfig] and [SlurmConfig] blocks",
    )
    args = parser.parse_args()

    file_path = args.file
    date = time.strftime("%d/%m/%Y")

    # Core pipeline
    simconfig_vars, slurm_vars, source_file_content = parse_sim_config(file_path)
    sims = set_simulations(simconfig_vars, source_file_content)
    sims = set_slurm_files(sims, slurm_vars)
    make_launcher(sims, simconfig_vars)

    print(
        "\n".join(
            [
                f"✓ Archivos generados con SimConfig ({date})",
                "Autor: Juan F. Restrepo <juan.restrepo@uner.edu.ar>",
            ]
        )
    )


if __name__ == "__main__":
    main()
