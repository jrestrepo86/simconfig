import time
from pathlib import Path

import pandas as pd


def make_launcher(sims, simconfig_vars):

    sim_name = simconfig_vars["name"]
    root_path = simconfig_vars["root-path"]

    launcher_array = []
    for sim in sims:
        launcher_file_name, content = single_sim_content(sim)
        launcher_array.append((launcher_file_name, content))
    launchers_info = pd.DataFrame(launcher_array, columns=["launcher-group", "content"])
    # Group by launcher-name and concatenate the content
    merged_launchers = launchers_info.groupby("launcher-group", as_index=False).agg(
        {"content": "\n".join}
    )
    launchers_filenames = write_launchers_to_files(
        merged_launchers, output_dir=root_path / "launchers"
    )
    make_runfile(sim_name, root_path, launchers_filenames)


def single_sim_content(sim):

    slurm_filename = sim["slurm-filename"]
    launcher_group = sim["launcher-group"]
    process_name = slurm_filename.stem

    content = (
        "#============================================================\n"
        f"# Proceso {process_name} \n"
        f"echo 'lanzando proceso: {process_name} '\n"
        f"sbatch {slurm_filename} &\n"
        "sleep 0.3"
    )
    return launcher_group, content


def write_launchers_to_files(merged_launchers, output_dir):
    """
    Write merged launcher content to files.

    Args:
        merged_launchers (pd.DataFrame): DataFrame from make_launcher() containing
                                          "launcher-name" and "content" columns
        output_dir (str/path): Directory where launcher files will be saved
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)  # Create directory if needed
    date = time.strftime("%d/%m/%Y")

    launchers_filenames = []
    for _, row in merged_launchers.iterrows():
        launcher_name = row["launcher-group"]
        content = row["content"]

        # add line to content begin
        content = (
            "#!/bin/sh\n"
            + content
            + f"\n\n# Generado automaticamente por SimConfig - {date}"
        )
        # Create filename with .sh extension
        filename = output_path / f"{launcher_name}.sh"
        launchers_filenames.append(filename)

        # Write content to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    return launchers_filenames


def make_runfile(sim_name, root_path, launchers_filenames):
    filename = root_path / f"run_{sim_name}.sh"
    date = time.strftime("%d/%m/%Y")

    content = ["#!/bin/sh"]
    for launcher in launchers_filenames:
        launcher_name = launcher.stem
        text = f"# {launcher_name}\n" f"./{launcher}"
        content.append(text)

    content.append("\nsqueue\n")
    content.append(f"# Generado automaticamente por SimConfig - {date}")
    content = "\n#==========================================\n".join(content)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
