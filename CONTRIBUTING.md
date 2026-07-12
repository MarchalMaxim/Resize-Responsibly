# Contributing

## Reporting Issues

Before filing an issue, check for existing reports:

```bash
gh issue list --state open
```

If no similar issue exists, create a new one with:

```bash
gh issue create --title "Brief summary" --body "Detailed description"
```

Include:
- Expected behavior
- Actual behavior
- Reproduction steps
- Environment details

## Pull Requests

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Concise message"`
4. Push: `git push origin HEAD`
5. Open a PR with `gh pr create --fill`

All PRs should:
- Reference related issues
- Include clear commit messages
- Be based on the latest main branch

Happy contributing!