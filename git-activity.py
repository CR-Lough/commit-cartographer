import git
from collections import defaultdict
import sys
import os

def get_folder_commit_counts(repo_path):
    """
    Get commit counts for each folder in the repository,
    but only for files that currently exist.
    
    Args:
        repo_path (str): Path to the Git repository
        
    Returns:
        dict: Dictionary mapping folder paths to commit counts
    """
    try:
        repo = git.Repo(repo_path)
    except git.exc.InvalidGitRepositoryError:
        print(f"Error: {repo_path} is not a valid Git repository", file=sys.stderr)
        return {}

    # Get current folder structure
    current_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            # Skip .git folder
            if '.git' in root:
                continue
            # Get path relative to repo root
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, repo_path)
            current_files.append(rel_path)

    folder_counts = defaultdict(int)
    
    # Get all commits, but only count those for existing files
    for commit in repo.iter_commits():
        for file in commit.stats.files.keys():
            # Only count commits for files that currently exist
            if file in current_files:
                # Split the path and increment count for each parent folder
                parts = file.split('/')
                for i in range(len(parts) - 1):  # Exclude the file itself
                    folder = '/'.join(parts[:i+1])
                    if folder:  # Skip empty strings
                        folder_counts[folder] += 1
    
    return dict(folder_counts)

def generate_gradient_colors(num_steps):
    """
    Generate a list of colors for a gradient.
    
    Args:
        num_steps (int): Number of steps in the gradient
        
    Returns:
        list: List of hex color codes
    """
    colors = []
    for i in range(num_steps):
        # Calculate the color based on the step
        r = int(255 * (i / (num_steps - 1)))
        g = int(255 * (1 - (i / (num_steps - 1))))
        b = 255  # Keep blue constant
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    return colors

def generate_mermaid(folder_counts):
    """
    Generate a Mermaid flowchart diagram from folder commit counts.
    Maximum depth of 4 levels from root, using a 10-step color gradient.
    
    Args:
        folder_counts (dict): Dictionary mapping folder paths to commit counts
        
    Returns:
        str: Mermaid flowchart diagram as a string
    """
    if not folder_counts:
        return "flowchart LR\n    root_node[/root\\]"
        
    total_commits = sum(folder_counts.values())
    min_count = min(folder_counts.values())
    max_count = max(folder_counts.values())
    
    # Generate 10-step gradient colors
    gradient_colors = generate_gradient_colors(10)
    
    mermaid = ["flowchart LR"]
    
    # Add root node with trapezoid shape
    mermaid.append("    root_node[/root\\]")
    mermaid.append("    style root_node fill:#ffffff,stroke:#333,stroke-width:2px")
    
    # Process folder paths up to 4 levels deep
    for folder, count in folder_counts.items():
        # Skip folders deeper than 4 levels
        if folder.count('/') > 3:
            continue
        
        # Map commit count to gradient color
        if total_commits > 0:
            normalized_count = (count - min_count) / (max_count - min_count)
            color_index = int(normalized_count * (len(gradient_colors) - 1))
            color = gradient_colors[color_index]
        else:
            color = '#ffffff'
        
        parts = folder.split('/')
        node_name = f"node_{folder.replace('/', '_')}"
        
        # Handle top-level folders and subfolders
        if '/' not in folder:  # Top-level folder
            parent_name = "root_node"
            folder_label = folder
        else:  # Subfolder
            parent_name = f"node_{'/'.join(parts[:-1]).replace('/', '_')}"
            folder_label = parts[-1]
        
        # Use folder shape for nodes
        mermaid.append(f"    {parent_name} --> {node_name}[/{folder_label}\\]")
        mermaid.append(f"    style {node_name} fill:{color},stroke:#333,stroke-width:2px")
    
    return "\n".join(mermaid)

if __name__ == "__main__":
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    try:
        counts = get_folder_commit_counts(repo_path)
        
        diagram = generate_mermaid(counts)
        
        # Write to markdown file
        with open('git-activity.md', 'w') as f:
            f.write("# Git Repository Activity Diagram\n\n")
            f.write("```mermaid\n")
            f.write(diagram)
            f.write("\n```\n")
            
        print(f"Diagram has been written to git-activity.md")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)