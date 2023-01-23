# arXiv Daily
This project creates an issue on every work day with the latest arXiv pre-prints matching a given set of keywords. It also creates a TL;DR summary automatically using [BART](https://huggingface.co/facebook/bart-base).

## Usage( github actions)

#### 1. Clone and create new repository on Github

- Create a repository to get notification in your github.
-  **click "Settings"->"Secrets"->"New repository secret"** 

```python
Name: GITHUB
# Authentication for user filing issue (must have read/write access to repository to add issue to)
Value: your_github_username,your_github_token
```

#### 2. Update `config.py`

```python

# The repository to add this issue to
REPO_OWNER = 'changeme'
REPO_NAME = 'changeme'

# Set new submission url of subject
NEW_SUB_URL = 'https://arxiv.org/list/cs/new'

# Keywords to search
KEYWORD_LIST = ["changeme"]
```

#### 3.  Workflow

To test the functionality, you can click " Run Workflow button" for an immediate run.

