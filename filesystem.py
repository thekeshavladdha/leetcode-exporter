import os
import json
from markdown import create_readme


def get_folder_name(problem):

    folder_name = f'{problem["id"]:04d}-{problem["title"]}'
    folder_name = folder_name.replace(" ", "-")

    invalid = '<>:"/\\|?*'

    for ch in invalid:
        folder_name = folder_name.replace(ch, "")

    return folder_name


def get_problem_path(problem, output_dir):

    return os.path.join(
        output_dir,
        get_folder_name(problem),
    )


def save_solution(problem, details, problem_data, output_dir):

    folder_name = get_folder_name(problem)

    path = get_problem_path(problem, output_dir)

    os.makedirs(path, exist_ok=True)

    submission = details["data"]["submissionDetails"]

    if submission is None:
        raise Exception("Submission details unavailable.")

    language = submission["lang"]["name"]

    extension = {
        "cpp": ".cpp",
        "python3": ".py",
        "java": ".java",
        "javascript": ".js",
    }.get(language.lower(), ".txt")

    filename = os.path.join(path, "solution" + extension)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(submission["code"])

    difficulty_map = {
        1: "Easy",
        2: "Medium",
        3: "Hard",
    }

    metadata = {
        "id": problem["id"],
        "title": problem["title"],
        "slug": problem["slug"],
        "difficulty": difficulty_map.get(problem["difficulty"], "Unknown"),
        "language": language,
        "runtime": submission["runtimeDisplay"],
        "memory": submission["memoryDisplay"],
        "timestamp": submission["timestamp"],
        "tags": [
            tag["name"]
            for tag in problem_data["data"]["question"]["topicTags"]
        ],
    }

    with open(
        os.path.join(path, "metadata.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(metadata, f, indent=4)

    create_readme(path, metadata)

    return {
        "id": problem["id"],
        "title": problem["title"],
        "folder": folder_name,
        "language": language,
        "difficulty": difficulty_map.get(problem["difficulty"], "Unknown"),
    }


def already_exported(problem, output_dir):

    path = get_problem_path(problem, output_dir)

    return os.path.exists(path)


def get_summary(output_dir):

    summary = []

    if not os.path.exists(output_dir):
        return summary

    for folder in os.listdir(output_dir):

        metadata_path = os.path.join(
            output_dir,
            folder,
            "metadata.json",
        )

        if not os.path.exists(metadata_path):
            continue

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        summary.append(
            {
                "id": metadata["id"],
                "title": metadata["title"],
                "difficulty": metadata["difficulty"],
                "language": metadata["language"],
                "folder": folder,
            }
        )

    summary.sort(key=lambda x: x["id"])

    return summary