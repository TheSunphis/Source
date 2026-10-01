# Remote Execution Gate

The user authorized the GitHub-only build by saying **Start**.

Current state:

- Repository Actions are enabled.
- The authorized classic OAuth token has `repo` but not `workflow` scope.
- GitHub rejected creation of `.github/workflows/expressions2-shadow-build.yml`.
- No local workspace, cache, runtime, evidence payload, candidate payload, or family payload is being used.
- The live `Expressions/` tree remains unchanged.

Required one-time action:

1. Re-authorize the GitHub credential with `workflow` scope, **or**
2. Manually copy `expressions2-shadow-build.yml` from this directory to `.github/workflows/` on this branch.

After that, the remote validation bootstrap can be dispatched and expanded into the private draft-release build for the 100-family commissioning batch.
