import subprocess


def run_git_command(args, repo_path):

    result = subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    return result

def git_add(repo_path):
    return run_git_command(["add", "."], repo_path)


def git_commit(repo_path, message):
    return run_git_command(
        ["commit", "-m", message],
        repo_path,
    )


def git_push(repo_path):
    return run_git_command(
        ["push", "origin", "main"],
        repo_path,
    )