---
name: backlog-connectors
description: Import and export backlogs from CSV, Excel, Jira, and YouTrack without pretending a live connection exists.
---

# Backlog connectors

## No account required

| Source | Command |
|---|---|
| CSV | `python3 cli/mazu.py import csv FILE` |
| Jira CSV export | `import jira-csv FILE` |
| YouTrack CSV export | `import youtrack-csv FILE` |
| Excel xlsx, first sheet | `import xlsx FILE` |
| Out | `export csv FILE` or `export xlsx FILE` |

Columns, any mix: Summary, Title, Name, Issue Type, Type, Status, State, Story Points, Estimation, Issue Key, Issue Id, Id, Description. Delimiter comma, semicolon, or tab.

## Tokens

`python3 cli/mazu.py connectors` prints whether env is present. It does not print secrets.

- Jira: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_TOKEN`, then `pull jira --jql "project = ABC"`.
- YouTrack: `YOUTRACK_URL`, `YOUTRACK_TOKEN`, then `pull youtrack --jql "project: ABC"`.

If a variable is missing, the command exits and names the CSV path. That is not a successful import.

Other trackers come in through their CSV or xlsx export and the same columns. There is no per-product plugin until an API has been checked against a real response.

## Mapping

Epic stays an epic. Story and Feature become stories. Bug and Task become tasks. Unknown types become stories. To Do, Open, In Progress, Review, and Done map onto the five columns. Anything else stays `backlog`. Points are kept only when they are Fibonacci. Other estimates are dropped. They are not converted into hours.

## Boundaries

Always: keep the original key in `external_id`.
Ask First: overwrite an existing project store.
Never: invent issues that were not in the file or the API response.
