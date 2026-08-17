# Cave-Console-Game

A short console text adventure, written to try out text adventure creation and saving/loading.

## Requirements

Python 2. `maincode.py` uses `print` statements and `raw_input()`, so it raises a `SyntaxError` under `python3`.

## How to Run

```bash
python2 maincode.py
```

### Known limitation

The game does not currently run to completion on machines other than the author's: the save path at the top of `maincode.py` is a hardcoded absolute Windows path, and both branches of the opening question open it, so the run ends in an `IOError` after the first answer and before the first decision. See [#2](https://github.com/Stephenson-Software/Cave-Console-Game/issues/2).

## How to Play

Answers are typed at the `>` prompt and are case-sensitive.

- `YES` or `NO` — whether a save file exists, whether to enter the cave, and whether to open the chest
- `DOWN` or `LEAVE` — at the hole in the chest
- `SAVE` — at any decision, to save progress and quit

Typing `SAVE` at the second or third decision raises a `NameError` when the session was started by loading a save rather than by starting a new game. See [#3](https://github.com/Stephenson-Software/Cave-Console-Game/issues/3).

## License

Licensed under the Stephenson Software Non-Commercial License (Stephenson-NC). See [LICENSE](LICENSE).
