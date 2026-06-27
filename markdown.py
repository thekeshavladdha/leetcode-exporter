import os

def create_readme(path, metadata):

    with open(
        os.path.join(path, "README.md"),
        "w",
        encoding="utf-8",
    ) as f:

        f.write(f"# {metadata['title']}\n\n")

        f.write(f"**Problem ID:** {metadata['id']}\n\n")
        f.write(f"**Difficulty:** {metadata['difficulty']}\n\n")
        f.write(f"**Language:** {metadata['language']}\n\n")
        f.write(f"**Runtime:** {metadata['runtime']}\n\n")
        f.write(f"**Memory:** {metadata['memory']}\n\n")

        f.write("## Tags\n\n")

        if metadata["tags"]:
            for tag in metadata["tags"]:
                f.write(f"- {tag}\n")
        else:
            f.write("No tags available.\n")

def create_root_readme(summary):

    easy = 0
    medium = 0
    hard = 0

    language_map = {
        "cpp": "C++",
        "python3": "Python",
        "java": "Java",
        "javascript": "JavaScript",
    }

    # Count problems by difficulty
    for problem in summary:

        if problem["difficulty"] == "Easy":
            easy += 1

        elif problem["difficulty"] == "Medium":
            medium += 1

        else:
            hard += 1

    # Sort by problem ID
    summary.sort(key=lambda x: x["id"])

    content = "# LeetCode Solutions\n\n"

    content += "## Statistics\n\n"

    content += f"- Total Solved: {len(summary)}\n"
    content += f"- Easy: {easy}\n"
    content += f"- Medium: {medium}\n"
    content += f"- Hard: {hard}\n\n"

    content += "---\n\n"

    content += "| ID | Problem | Difficulty | Language |\n"
    content += "|----|---------|------------|----------|\n"

    for problem in summary:

        language = language_map.get(
            problem["language"].lower(),
            problem["language"],
        )

        content += (
            f"| {problem['id']:04d} "
            f"| [{problem['title']}](output/{problem['folder']}) "
            f"| {problem['difficulty']} "
            f"| {language} |\n"
        )

    with open(os.path.join("output", "README.md"), "w", encoding="utf-8") as f:
        f.write(content)