import os
import sys
import subprocess

def run_command(command):
    """Executes a shell command and prints output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr}")
        sys.exit(1)

def remove_file_from_git(file_path):
    """Removes a specific file from Git history."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Exiting.")
        sys.exit(1)

    # Add file to .gitignore
    with open(".gitignore", "a") as gitignore:
        gitignore.write(f"\n{file_path}\n")

    print(f"Added {file_path} to .gitignore.")

    # Remove file from Git history using git-filter-repo
    print(f"Removing {file_path} from Git history...")
    run_command(f"git filter-repo --path {file_path} --invert-paths --force")

    # Clean up Git reflog and perform garbage collection
    print("Cleaning up Git history...")
    run_command("git reflog expire --expire=now --all")
    run_command("git gc --prune=now --aggressive")

    # Force push changes to remote
    print("Force pushing changes to remote...")
    run_command("git push origin --force --all")
    run_command("git push origin --force --tags")

    print("\n✅ File successfully removed from Git history. Rotate any leaked secrets immediately!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleanup_git_secrets.py <file-to-remove>")
        sys.exit(1)

    file_to_remove = sys.argv[1]
    remove_file_from_git(file_to_remove)

