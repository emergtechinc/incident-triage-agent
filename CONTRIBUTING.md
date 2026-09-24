# How we work

**Branch name:** `ticket-<n>-<short-name>` — e.g. `ticket-5-loop`.

**Commit messages:** what changed and why, not what file you touched.
`bounds: stop before spending, not after` beats `updated bounds.py`.

**Pull requests:** reference the issue (`Closes #5`). Say what you did and anything you were unsure
about — "I wasn't sure whether X" is the most useful line in a PR.

**Reviewing:** you are not looking for style. Look for: does it do what the ticket asked, would you
understand it in six months, and does it handle the case the test does not cover. Approve when it is
good enough to build on — not when it is perfect.

**If the tests are wrong**, argue it on the issue before changing them. Sometimes they will be.

**Never commit a key.** `.env` is gitignored. If one ever lands in a commit, say so immediately —
revoking is thirty seconds and there is no version of this where hiding it is better.
