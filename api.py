
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


