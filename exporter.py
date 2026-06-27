from tqdm import tqdm
from cli import parse_args
from config import DEFAULT_OUTPUT_DIR
from api import (
    get_solved_problems,
    get_submission_list,
    get_submission_details,
    get_problem_data,
)
from filesystem import (
    save_solution,
    already_exported,
    get_summary,
)
from markdown import create_root_readme
from git_utils import (
    git_add,
    git_commit,
    git_push,
    git_has_changes,
)


def main():

    args = parse_args()
    output_dir = args.output or DEFAULT_OUTPUT_DIR

    problems = get_solved_problems()

    if args.difficulty:
        difficulty_map = {
            "easy": 1,
            "medium": 2,
            "hard": 3,
        }

        problems = [
            p
            for p in problems
            if p["difficulty"] == difficulty_map[args.difficulty]
        ]

    new_problems = []
    skipped = 0

    for problem in problems:

        if not args.force and already_exported(problem, output_dir):
            skipped += 1
        else:
            new_problems.append(problem)

    print(f"\nFound {len(problems)} solved problems.")
    print(f"Already exported : {skipped}")
    print(f"New problems     : {len(new_problems)}")

    success = 0
    failed = 0

    if new_problems:

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

                save_solution(
                    problem,
                    details,
                    problem_data,
                    output_dir,
                )

                success += 1

            except Exception as e:
                failed += 1
                tqdm.write(f"Failed: {problem['title']}")
                tqdm.write(f"Reason: {e}")

    else:

        print("\nEverything is already up to date.")

    summary = get_summary(output_dir)
    create_root_readme(summary, output_dir)
    if args.push:

        if success == 0 and not git_has_changes(output_dir):
            print("\nNo new solutions exported.")
            print("No repository changes detected.")
            print("Skipping Git commit.")
            return

        print("\nRunning Git commands...")

        result = git_add(output_dir)

        if result.returncode != 0:
            print(result.stderr)
            return

        result = git_commit(
            output_dir,
            f"Add {success} new LeetCode solution(s)",
        )

        if result.returncode != 0:
            print(result.stderr)
            return

        result = git_push(output_dir)

        if result.returncode != 0:
            print(result.stderr)
            return

        print("Git push completed successfully!")

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