#!/usr/bin/env python3
import re
import sys

# Règles pour Conventional Commits
PATTERN = re.compile(r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}$")


def validate_commit_msg(commit_msg_file):
    with open(commit_msg_file, "r") as f:
        commit_msg = f.read().strip()

    if not PATTERN.match(commit_msg):
        print("ERREUR : Le message de commit ne respecte pas Conventional Commits.")
        print("Format attendu : <type>(<scope>): <description>")
        print("Types autorisés : feat, fix, docs, style, refactor, test, chore")
        print(f"Message reçu : {commit_msg}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_commit_msg(sys.argv[1])
    else:
        print("ERREUR : Fichier de message de commit non fourni.")
        sys.exit(1)
