from leetcode_api import (
    get_solved_problems,
    get_submission_list,
    get_submission_details,
    get_problem_data,
    save_solution,
    create_root_readme,
)

def main():
    
    print("Inside main")
    problems = get_solved_problems()

    print(f"\nFound {len(problems)} solved problems.\n")

    success = 0
    failed = 0
    summary = []
    
    for index, problem in enumerate(problems, start=1):

        try:
            print(f"[{index}/{len(problems)}] {problem['title']}")

            submissions = get_submission_list(problem["slug"])

            submission_list = submissions["data"]["questionSubmissionList"]["submissions"]

            if not submission_list:
                print("   ⚠ No accepted submissions found.\n")
                failed += 1
                continue

            latest = submission_list[0]

            details = get_submission_details(int(latest["id"]))

            problem_data = get_problem_data(problem["slug"])
            
            submission = details["data"]["submissionDetails"]

            if submission is None:
                raise Exception("Submission details unavailable.")

            info = save_solution(problem, details, problem_data)

            summary.append({
                "id": problem["id"],
                "title": problem["title"],
                "difficulty": info["difficulty"],
                "language": info["language"],
                "folder": info["folder"],
            })

            success += 1
            

        except Exception as e:
            failed += 1
            print(f"      Failed to export '{problem['title']}'")
            print(f"      Reason: {e}\n")

    print("\n" + "=" * 50)
    print("Export Complete!")
    print("=" * 50)
    print(f"Successfully exported : {success}")
    print(f"Failed               : {failed}")
    print(f"Total                : {success + failed}")
    create_root_readme(summary)
    print("Root README generated!")
    
if __name__ == "__main__":
    main()