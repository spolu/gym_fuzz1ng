# gym-fuzz1ng

Fuzzing gym environment based on afl (american fuzzy lop).

## Available environments

### `FuzzLibPNGEnv`

- **action_space**: `Discrete(283)` composed of a dictionary of magic tokens,
  bytes and an EOF action.
