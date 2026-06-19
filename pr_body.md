Resolves #424

## Overview
This Pull Request implements the highly requested **Free: Add `agentwatch share` command to create a temporary web link for a trace** functionality into the AgentWatch CLI.

---

## Why do we need this?
**For a 5-year-old:** When our robot does a really cool trick, we want a "share" button to send a magic link to our friends so they can see it too!

**For developers:** Asking for help on Discord or GitHub is hard when pasting massive JSON logs. Developers need a way to upload a trace and get a short-link to share.

## What is it?
A new CLI command `agentwatch share <session-id>` that sanitizes a trace and securely uploads it to a public pastebin or free AgentWatch community viewer. This is a **FREE** feature.

## Suggestions for Implementation
- Strictly enforce `redact_phi` and strip out API keys or sensitive `.env` metadata before uploading.
- `POST` the trace payload to a lightweight backend.
- Return a clickable URL in the terminal.


---

### Implementation Notes 🛠️
- Implemented via the `typer` framework in `agentwatch/cli/main.py`.
- Includes a beautiful terminal UI response using `rich`.
- Validated to pass all rigorous test suites, including conditional dependency checks.
