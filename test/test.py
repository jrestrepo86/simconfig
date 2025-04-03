"""Read file info"""

import os
import sys
from pathlib import Path

try:
    from src.launchers import make_launcher
    from src.read_file import parse_sim_config
    from src.sim_files import set_simulations
    from src.slurm_files import set_slurm_files
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent))
    from src.launchers import make_launcher
    from src.read_file import parse_sim_config
    from src.sim_files import set_simulations
    from src.slurm_files import set_slurm_files


if __name__ == "__main__":
    filename = "../examples/example_python.py"
    simconfig_vars, slurm_vars, source_file_content = parse_sim_config(filename)
    # # print(sim_config)
    sims = set_simulations(simconfig_vars, source_file_content)
    sims = set_slurm_files(sims, slurm_vars)
    make_launcher(sims, simconfig_vars)
    pass

    # content = read_content(filename)
    # print(content)
