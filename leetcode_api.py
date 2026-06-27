import json
import os
import requests
from config import LEETCODE_SESSION, CSRFTOKEN


URL = "https://leetcode.com/graphql"

headers = {
    "x-csrftoken": CSRFTOKEN,
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
    "Content-Type": "application/json",
}

cookies = {
    "LEETCODE_SESSION": LEETCODE_SESSION,
    "csrftoken": CSRFTOKEN,
}

session = requests.Session()

session.headers.update(headers)
session.cookies.update(cookies)

def graphql(operation_name, query, variables):

    response = session.post(
        URL,
        json={
            "operationName": operation_name,
            "query": query,
            "variables": variables,
        }
    )

    response.raise_for_status()

    return response.json()
def get_submission_list(question_slug):
    query = """
    query submissionList(
        $offset: Int!,
        $limit: Int!,
        $lastKey: String,
        $questionSlug: String!
    ){
      questionSubmissionList(
        offset:$offset,
        limit:$limit,
        lastKey:$lastKey,
        questionSlug:$questionSlug
      ){
        submissions{
          id
          statusDisplay
          lang
        }
      }
    }
    """

    return graphql(
        "submissionList",
        query,
        {
            "questionSlug": question_slug,
            "offset": 0,
            "limit": 20,
            "lastKey": None,
        },
    )
def get_submission_details(submission_id):
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
        runtimeDisplay
        memoryDisplay
        timestamp
        lang {
          name
        }
        topicTags {
          name
        }
      }
    }
    """

    return graphql(
        "submissionDetails",
        query,
        {
            "submissionId": submission_id
        },
    )

def get_problem_data(question_slug):

    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        difficulty

        topicTags {
          name
        }
      }
    }
    """

    return graphql(
        "questionData",
        query,
        {
            "titleSlug": question_slug
        },
    )

def get_all_problems():

    response = session.get(
        "https://leetcode.com/api/problems/all/"
    )

    response.raise_for_status()

    return response.json()

def get_solved_problems():

    data = get_all_problems()

    

    print(data["user_name"])
    print(data["num_solved"])
    solved = []

    for problem in data["stat_status_pairs"]:

        if problem["status"] == "ac":

            solved.append(
                {
                    "id": problem["stat"]["frontend_question_id"],
                    "title": problem["stat"]["question__title"],
                    "slug": problem["stat"]["question__title_slug"],
                    "difficulty": problem["difficulty"]["level"],
                }
            )

    return solved

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

def get_summary():

    summary = []

    output_path = "output"

    if not os.path.exists(output_path):
        return summary

    for folder in os.listdir(output_path):

        metadata_path = os.path.join(
            output_path,
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