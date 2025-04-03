

%{
[SimConfig]
name='E01'
variables={'condition':[1,2],'pathology':[1,3]}
realizations={'exp01':2}
matexecutable='matlab'
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
%}

condition = 1;
pathology = 1;
exp01 = 1;

disp(['condition=' condition]);
disp(['pathology=' pathology]);
disp(['exp01=' exp01]);

if exp01 == 1
    disp('exp01 == 1')
else
    disp('exp01 != 1')
end
