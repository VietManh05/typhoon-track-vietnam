"""Pre-commit configuration contract tests."""

import shutil
import subprocess
import sys
from pathlib import Path

import yaml


def test_precommit_config_declares_file_and_message_stages(tmp_path) -> None:
    config_path = Path(".pre-commit-config.yaml")
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    local = next(repo for repo in config["repos"] if repo["repo"] == "local")
    hook = next(
        item for item in local["hooks"] if item["id"] == "conventional-commit-msg"
    )
    assert hook["stages"] == ["commit-msg"]
    assert hook["entry"] == "python scripts/validate_commit_msg.py"

    # Exercise pre-commit in an isolated repository. The real worktree is dirty
    # by design, and pre-commit correctly refuses an unstaged config there.
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy2(config_path, repo / config_path.name)
    shutil.copy2(
        "scripts/validate_commit_msg.py", repo / "scripts/validate_commit_msg.py"
    )
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(
        ["git", "add", ".pre-commit-config.yaml", "scripts/validate_commit_msg.py"],
        cwd=repo,
        check=True,
    )

    valid = repo / "valid.txt"
    invalid = repo / "invalid.txt"
    valid.write_text("feat(api): add forecast endpoint\n", encoding="utf-8")
    invalid.write_text("Update files\n", encoding="utf-8")
    base = [
        sys.executable,
        "-m",
        "pre_commit",
        "run",
        "conventional-commit-msg",
        "--hook-stage",
        "commit-msg",
        "--commit-msg-filename",
    ]
    assert subprocess.run([*base, str(valid)], cwd=repo, check=False).returncode == 0
    assert subprocess.run([*base, str(invalid)], cwd=repo, check=False).returncode == 1
