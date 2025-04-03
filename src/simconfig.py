import argparse
import time

from src.launchers import make_launcher
from src.read_file import parse_sim_config
from src.sim_files import set_simulations
from src.slurm_files import set_slurm_files

# Parse options
parser = argparse.ArgumentParser(
    description="publicar", formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument(
    "file", nargs=argparse.REMAINDER, metavar="file.py/.m", help="file python / matlab"
)
args = parser.parse_args()
source_file_name = args.file[0]

date = time.strftime("%d/%m/%Y")


def main():
    simconfig_vars, slurm_vars, source_file_content = parse_sim_config(source_file_name)
    sims = set_simulations(simconfig_vars, source_file_content)
    sims = set_slurm_files(sims, slurm_vars)
    make_launcher(sims, simconfig_vars)

    print(
        "\n".join(
            [
                f"Archivos generados con SimConfig {date}",
                "Juan Felipe Restrepo <juan.restrepo@under.edu.ar> 2025",
            ]
        )
    )


if __name__ == "__main__":
    main()
