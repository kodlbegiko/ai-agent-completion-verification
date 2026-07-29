# Environment Preflight

Generated evidence is stored in `evidence/environment/environment.json` and `logs/environment/preflight.log`.

Current high-level classification:

- Local Python execution: VERIFIED
- Node.js: VERIFIED
- Local Git: VERIFIED
- Python virtual environments: VERIFIED
- Python sqlite3 module: VERIFIED
- SQLite CLI: UNAVAILABLE
- C compiler and Make: VERIFIED
- Playwright Python package: VERIFIED; browser executable NOT VERIFIED
- Docker/Podman: UNAVAILABLE
- External DNS/network from shell: UNAVAILABLE
- Background subprocesses: VERIFIED
- GitHub connector authentication/read: VERIFIED for public/private repositories, commits, PRs, Actions runs, jobs, and logs
- GitHub branch/file/commit/draft-PR write: VERIFIED in disposable repository `kodlbegiko/test1`
- GitHub smoke PR: `https://github.com/kodlbegiko/test1/pull/2` (closed without merge; test file removed on branch)
- GitHub repository creation: UNAVAILABLE through exposed connector
- Git tag, Release, and asset upload: UNAVAILABLE through exposed connector; repository workflow prepared as fallback
