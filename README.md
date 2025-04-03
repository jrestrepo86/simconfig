# Simulation Config — Python Code

**Juan F. Restrepo**

[juan.restrepo@uner.edu.ar](mailto:juan.restrepo@uner.edu.ar)

_Laboratorio de Señales y Dinámicas no Lineales, Instituto de Bioingeniería y
Bioinformática, CONICET - Universidad Nacional de Entre Ríos, Argentina._

---

## Installation

### From GitHub Repository

To install the package directly from GitHub:

```bash
pip install git+https://github.com/jrestrepo86/simconfig.git
```

To clone and install locally:

```bash
git clone https://github.com/jrestrepo86/simconfig.git
cd simconfig
pip install .
```

For development (editable mode):

```bash
git clone https://github.com/jrestrepo86/simconfig.git
cd simconfig
pip install -e .
```

---

## Usage

Run `simconfig` on Python or Matlab scripts:

```bash
simconfig file.py  # For Python files
simconfig file.m   # For Matlab files
```

### Example:

```bash
cd simconfig/examples
simconfig example.py
```

---

## Configuration File Structure

Define configuration blocks in your Python or Matlab script using comments.

### Python Example (`example_python.py`)

```python
"""
[SimConfig]
name='E01'  # Simulation name
variables={'condition':[1,2],'pathology':[1,3]}  # Parameters
realizations={'exp01':2}  # Trial configurations
pyexecutable='python3.10'  # Python interpreter
venv={'type': 'conda', 'conda-env': 'base'}  # Virtual environment
[endSimConfig]

[SlurmConfig]
slurm = {
  'neptuno': [  # Host-specific settings
    mail-user=[jrestrepo@uner.edu.ar](mailto:jrestrepo@uner.edu.ar),
    partition=internos,
    nodes=1,
    ntasks=24,
    tasks-per-node=24,
  ],
  'jupiter': [
    mail-user=[jrestrepo@uner.edu.ar](mailto:jrestrepo@uner.edu.ar),
    partition=debug,
    gres=gpu:1,
  ]
}
[endSlurmConfig]
"""
```

### Matlab Example (`example_matlab.m`)

```matlab
%{
[SimConfig]
name='E01'
variables={'condition':[1,2],'pathology':[1,3]}
realizations={'exp01':2}
matexecutable='matlab'  # Matlab interpreter
[endSimConfig]

[SlurmConfig]
slurm = {
  'neptuno': [
    mail-user=[jrestrepo@uner.edu.ar](mailto:jrestrepo@uner.edu.ar),
    tasks-per-node=24,
  ]
}
[endSlurmConfig]
%}
```

---

## Key Features

### SimConfig Parameters

- **name**: Unique identifier for the simulation
- **variables**: Defines parameter space
- **realizations**: Configures trial repetitions
- **pyexecutable/matexecutable**: Defines runtime environment
- **venv**: Virtual environment setup (e.g., Conda or Pip)

### SlurmConfig Options

- Supports multiple cluster profiles
- Defines host-specific job configurations
- Common SLURM parameters:
  - **partition**: Job queue
  - **nodes**: Number of nodes
  - **gres**: GPU resources
  - **mail-user**: Notification email
  - **etc ...**: Add all needed slurm parameters

---

## File Structure

```
.
├── setup.py           # Package setup
├── simconfig.py       # CLI implementation
├── example_python.py  # Python configuration template
├── example_matlab.m   # Matlab configuration template
└── README.md          # Documentation
```

---

## Output

The tool generates:

- **SLURM job files** for batch execution
- **Parameter combinations** based on configuration
- **Execution launchers** for automated runs

---

## License

**MIT License**

**Contact:** Juan Felipe Restrepo
[jrestrepo@ingenieria.uner.edu.ar](mailto:jrestrepo@ingenieria.uner.edu.ar)
