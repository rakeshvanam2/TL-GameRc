# RabbitGame
A simple command line game of rabbit's simple life.

# Story
Help rabbit find his carrot and store it in the rabbit hole.


## Install
```bash
python -m venv ./venv
source ./venv/Scripts/activate
pip install -r requirements.txt

```
## Gameplay
- use `a` to move left and `d` to move right.
- pick carrot (`c`) using `p` (rabbit changes from `r` to `R`) and drop it in rabbit hole (`O`).
- Jump over rabbit hole using `j`.
- Press `esc` key anytime to escape the game
```bash
python main.py
```

## Testing
Test passes.
```bash
pythontest --no-header -v
```

