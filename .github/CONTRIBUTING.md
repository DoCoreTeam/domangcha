# Contributing to DOMANGCHA

Thank you for your interest in contributing to DOMANGCHA — the 16-agent AI automation crew for Claude Code. This document explains how to contribute effectively.

## Table of Contents

- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Adding a New Agent](#adding-a-new-agent)
- [Coding Conventions](#coding-conventions)
- [Commit Message Format](#commit-message-format)
- [Code of Conduct](#code-of-conduct)

---

## Issues

### Bug Reports

If you found a bug, please open an issue using the **Bug Report** template. Include:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, shell, Claude Code version)

### Feature Requests

For new ideas or improvements, open an issue using the **Feature Request** template. Describe:

- The problem you are trying to solve
- Your proposed solution
- Any alternatives you considered

---

## Pull Requests

1. **Fork** the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the [Coding Conventions](#coding-conventions) below.

3. Test your changes locally before submitting.

4. Open a Pull Request against `main` with a clear description of what changed and why.

5. Address any review feedback promptly.

---

## Adding a New Agent

All agents live in `domangcha/agents/`. To add a new agent:

1. Create a new directory: `domangcha/agents/DC-YOUR-AGENT/`
2. Add a `AGENT.md` file describing the agent's role, model tier, primary skills, and responsibilities.
3. Follow the existing agent format — see `domangcha/agents/DC-DEV-OPS/` as a reference.
4. Update `domangcha/CLAUDE.md` to register the new agent in the agent table.
5. Document the agent in `README.md` under the appropriate category (PLANNER / GENERATOR / EVALUATOR / SUPPORT).

---

## Coding Conventions

### Shell Scripts

- All scripts must be POSIX-compatible bash.
- After editing `install.sh` or any shell script, validate syntax before committing:
  ```bash
  bash -n scripts/your-script.sh
  ```
- Use `#!/usr/bin/env bash` as the shebang line.
- Prefer absolute paths in scripts where applicable.
- Keep scripts focused — one clear responsibility per script.

### Markdown Files

- Keep lines readable (no hard wrapping required, but avoid extremely long lines).
- Use ATX-style headings (`#`, `##`, `###`).
- Code blocks must specify the language for syntax highlighting.

### File Size

- Files must not exceed 300 lines. Split large files into focused modules.

---

## Commit Message Format

All commits must follow this format:

```
v{VERSION}: description of the change
```

Examples:

```
v2.0.12: Add DC-NEW agent for data analysis
v2.0.13: Fix install.sh path resolution on macOS
```

The version number must match the current value in `domangcha/VERSION`. Do not increment MINOR or MAJOR versions unless the change warrants it and is explicitly discussed with the maintainer.

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you agree to uphold these standards:

- Use welcoming and inclusive language.
- Respect differing viewpoints and experiences.
- Accept constructive criticism gracefully.
- Focus on what is best for the community.
- Show empathy toward other contributors.

Violations may be reported to the project maintainer at kko2349@gmail.com.

---

Thank you for helping make DOMANGCHA better.
