import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        description="Export accepted LeetCode submissions."
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-export all problems even if they already exist.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory.",
    )

    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Export only problems of a certain difficulty.",
    )

    

    return parser.parse_args()