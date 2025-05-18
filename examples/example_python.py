#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[SimConfig]
name='E01'
variables={'condition':[1,2],'pathology':[1,3]}
realizations={'exp01':2}
pyexecutable='python3.10'
venv = {"type": "conda", "env-name": "base"}
[endSimConfig]
[SlurmConfig]
slurm = { 'neptuno':[
mail-user=juan.restrepo@uner.edu.ar,
partition=internos,
nodes=1,
ntasks=24,
tasks-per-node=24,
],
'jupiter':[
mail-user=juan.restrepo@uner.edu.ar,
partition=debug,
nodes=1,
ntasks=1,
cpus-per-task=1,
mem=8G,
gres=gpu:1,
]
}
[endSlurmConfig]
"""

condition = 1
pathology = 1
exp01 = 1

print(f"condition={condition} pathology={pathology} exp01={exp01}")

if exp01 == 1:
    print(f"{exp01} == 1")
else:
    print(f"{exp01} != 1")
