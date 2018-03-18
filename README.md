# gym-fuzz1ng

Fuzzing gym environment based on afl (american fuzzy lop).

## Installation

```
# Note that running setup.py bdist_wheel takes a bit a time as it builds our
# afl mod as well as the available targets.
pip install .
```

## Available environments

### `FuzzLibPNGEnv`

- **action_space**: `Discrete(283)` composed of a dictionary of magic tokens,
  bytes and an EOF action.
