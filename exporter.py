from tqdm import tqdm

from leetcode_api import (
    get_solved_problems,
    get_submission_list,
    get_submission_details,
    get_problem_data,
    save_solution,
    create_root_readme,
    already_exported,
    get_summary,
)


def main():

    problems = get_solved_problems()
    new_problems = []
    skipped = 0

    for problem in problems:

        if already_exported(problem):
            skipped += 1
        else:
            new_problems.append(problem)

    print(f"\nFound {len(problems)} solved problems.")
    print(f"Already exported : {skipped}")
    print(f"New problems     : {len(new_problems)}\n")
    if not new_problems:
        print("Everything is already up to date.\n")

    success = 0
    failed = 0
    skipped = 0

    for problem in tqdm(
        new_problems,
        desc="Exporting",
        unit="problem",
    ):

        try:
            submissions = get_submission_list(problem["slug"])

            submission_list = submissions["data"]["questionSubmissionList"]["submissions"]

            if not submission_list:
                failed += 1
                tqdm.write(f"No accepted submission: {problem['title']}")
                continue

            latest = submission_list[0]

            details = get_submission_details(int(latest["id"]))

            problem_data = get_problem_data(problem["slug"])

            if details["data"]["submissionDetails"] is None:
                raise Exception("Submission details unavailable.")

            save_solution(problem, details, problem_data)

            success += 1

        except Exception as e:
            failed += 1
            tqdm.write(f"Failed: {problem['title']}")
            tqdm.write(f"Reason: {e}")

    create_root_readme(get_summary())

    print("\nRoot README generated!")

    print("\n" + "=" * 50)
    print("Export Complete!")
    print("=" * 50)
    print(f"Successfully exported : {success}")
    print(f"Failed               : {failed}")
    print(f"Skipped              : {skipped}")
    print(f"Total                : {success + failed + skipped}")


if __name__ == "__main__":
    main()