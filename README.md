# LeetCode Exporter

> Automatically export your accepted LeetCode submissions into a well-organized GitHub repository with generated documentation, metadata, and optional Git automation.

LeetCode Exporter is a Python command-line tool that automates the process of maintaining a public LeetCode solutions repository.

Instead of manually copying solutions after every accepted submission, the exporter fetches your latest accepted code directly from LeetCode, organizes it into numbered folders, generates documentation, updates the repository README, and can optionally commit and push everything to GitHub with a single command.

---

## Why I Built This

After solving a few hundred LeetCode problems, manually maintaining a GitHub repository became repetitive and error-prone.

This project was built to automate the entire workflow while keeping the exported repository clean, consistent, and easy to navigate.

---

## Features

* Export accepted LeetCode submissions
* Incremental exports (skip already exported problems)
* Force re-export when needed
* Filter exports by difficulty
* Configurable output directory
* Automatically generate:

  * Root README
  * Problem README
  * Metadata for every solution
* Automatic Git commit and push
* Modular, extensible project structure

---

## Example

Export only new solutions:

```bash
python exporter.py
```

Export and automatically push the changes:

```bash
python exporter.py --push
```

Re-export every solution:

```bash
python exporter.py --force
```

Export only hard problems:

```bash
python exporter.py --difficulty hard
```

Use a custom output directory:

```bash
python exporter.py --output "D:\LeetCode-Solutions"
```

---

## Generated Repository Structure

```text
LeetCode-Solutions/
│
├── README.md
├── 0001-Two-Sum/
│   ├── solution.cpp
│   ├── README.md
│   └── metadata.json
├── 0002-Add-Two-Numbers/
│   ├── solution.cpp
│   ├── README.md
│   └── metadata.json
└── ...
```

---

## Project Structure

```text
leetcode-exporter/
│
├── api.py
├── cli.py
├── config.py
├── exporter.py
├── filesystem.py
├── git_utils.py
├── markdown.py
└── requirements.txt
```

---

## Configuration

Create a `config.py` file and provide your LeetCode session information.

```python
LEETCODE_SESSION = "..."
CSRFTOKEN = "..."

DEFAULT_OUTPUT_DIR = r"C:\LeetCode-Solutions"
```

---

## Requirements

* Python 3.10+
* requests
* tqdm

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Roadmap

* [ ] Export individual problems
* [ ] Filter by programming language
* [ ] Improved README generation
* [ ] Publish as a PyPI package

---

## License

This project is licensed under the MIT License.
