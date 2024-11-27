# Commit Cartographer

## Overview

The `commit-cartographer` project provides a tool to analyze the commit activity of a Git repository. It generates a flowchart diagram that visualizes the number of commits made in each folder of the repository, helping developers understand the structure and activity of their codebase.

## Features

- Count commits for each folder in a Git repository.
- Generate a Mermaid flowchart diagram to visualize commit activity.
- Supports only files that currently exist in the repository.
- Customizable color gradient for visual representation.

## Installation

To use this project, ensure you have Python 3.12 or higher installed. You can install the required dependencies using `pip`:

"""
pip install -r requirements.txt
"""

Alternatively, you can install the dependencies directly:

"""
pip install gitpython>=3.1.43
"""

## Usage

To run the tool, execute the following command in your terminal:

"""
python git-activity.py [path_to_your_repo]
"""

If no path is provided, it defaults to the current directory.

## Output

The script generates a Markdown file named `git-activity.md`, which contains the Mermaid flowchart diagram representing the commit activity in the specified Git repository.

## Example

After running the script, you will find a `git-activity.md` file with content similar to the following:

"""
flowchart LR
    root_node[/root\]
    style root_node fill:#ffffff,stroke:#333,stroke-width:2px
    root_node --> node_folder1[/folder1\]
    style node_folder1 fill:#ff00ff,stroke:#333,stroke-width:2px
    ...
"""

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
