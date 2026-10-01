# Expressions2 Tool-Only Morphology Runtime

The user approved the recommended SudachiPy-first gate.

- SudachiPy: 0.7.0, CPython 3.10+ ABI3, manylinux 2.28 x86_64
- SudachiDict Core: 20260723.1
- Licence route: Apache 2.0 plus the dictionary component notices recorded in the source registry
- Purpose: deterministic candidate normalization and morphology only
- Output authority: none; morphology cannot establish expression attestation or family admission

Install only into excluded temporary storage:

```bash
python3 -m pip install --no-deps --require-hashes \
  --target .cache/expressions2-morphology-runtime \
  -r work/expressions2/runtime/requirements-linux-x86_64.lock
```

Do not install into the application runtime, add the dependency to Koto production, or commit the installed files. Candidate and build manifests must record the exact runtime and dictionary snapshot hashes.
