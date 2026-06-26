# LeetCode Exporter

Automatically export your accepted LeetCode submissions using the official LeetCode GraphQL API.

The exporter downloads your latest accepted solution for every solved problem and generates a clean folder structure containing:

- Source code
- Metadata
- Problem README
- Root statistics README

---

## Features

- Export all solved LeetCode problems
- Supports multiple programming languages
- Creates one folder per problem
- Generates metadata.json
- Generates README.md for every problem
- Generates a root README with statistics
- Stores runtime and memory usage
- Exports problem tags
- Handles API failures gracefully
- Continues exporting even if one problem fails

---

## Installation

Clone the repository

```bash
git clone https://github.com/thekeshavladdha/leetcode-exporter.git
cd leetcode-exporter
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file

```env
LEETCODE_SESSION=your_session_cookie
CSRFTOKEN=your_csrf_token
```

---

## Usage

Run

```bash
python exporter.py
```

---

## Output Structure

```
output/
│
├── 0001-Two-Sum/
│   ├── solution.cpp
│   ├── metadata.json
│   └── README.md
│
├── 0002-Add-Two-Numbers/
│   ├── solution.cpp
│   ├── metadata.json
│   └── README.md
│
└── ...
```

---

## Example Metadata

```json
{
    "id": 1,
    "title": "Two Sum",
    "difficulty": "Easy",
    "language": "cpp",
    "runtime": "3 ms",
    "memory": "11.8 MB",
    "tags": [
        "Array",
        "Hash Table"
    ]
}
```

---

## Generated README

Each exported problem contains its own README with:

- Problem ID
- Difficulty
- Runtime
- Memory
- Tags

---

## Requirements

- Python 3.10+
- requests
- python-dotenv

---

## Roadmap

- [x] Export accepted submissions
- [x] Metadata generation
- [x] README generation
- [x] Root README generation
- [x] Tags support
- [x] Incremental export
- [x] Progress bar
- [ ] CLI arguments
- [ ] GitHub Actions
- [ ] PyPI package

---

## License

MIT License
