"""simconfig and slurm defults"""

simconfig_vars = {
    "name": "",
    "variables": {},
    "realizations": {},
    "matexecutable": "matlab",
    "pyexecutable": "python3",
    "venv": {"type": "conda", "conda-env": "base", "pip-env": "./.env"},
}
slurm_config = {
    "host-name": "",
    "neptuno": [
        "mail-user=",
        "partition=internos",
        "nodes=1",
        "ntasks=24",
        "tasks-per-node=24",
    ],
    "jupiter": [
        "mail-user=",
        "partition=debug",
        "nodes=1",
        "ntasks=1",
        "cpus-per-task=1",
        "mem=8G",
        "gres=gpu:1",
    ],
}
