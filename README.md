# gym-fuzz1ng

Fuzzing gym environment based on afl (american fuzzy lop) for a variety of well
known libraries (libpng for now) as well as simpler examples (coming soon).

The action space of these environments is discrete with size based on the
dictionary used for fuzzing. The size of the action space therefore varies from
one environment to another.

The environment simulates the following game:

- each action appends a token from the dictionary to the current input
- the current input is run and the additional coverage received from the token
  addition is returned as reward (might be 0).
- if EOF is received or the input goes beyond a maximum size, the input data
  coverage is compared to the total coverage of the game. If no new coverage
  was discovered from the previous input data (since last EOF) the game is
  ended.

## Installation

```
# Note that running setup.py bdist_wheel takes a bit a time as it builds our
# afl mod as well as the available targets.
pip install .

# You can then test that everything works by running our dummy example.
python test/dummy.py
```

## Available environments

### `FuzzLibPNGEnv`

Fuzzing environment for libpng-1.6.34 (recent).

- **action_space**: `Discrete(283)` dictionary composed of magic tokens and
  all 255 bytes.
