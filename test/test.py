"""Read file info"""

from simconfig.launchers import make_launcher
from simconfig.read_file import parse_sim_config
from simconfig.sim_files import set_simulations
from simconfig.slurm_files import set_slurm_files

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
