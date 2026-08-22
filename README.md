# Cave-Console-Game

A short console text adventure, written to try out text adventure creation and saving/loading.

## Requirements

Python 2. `maincode.py` uses `print` statements and `raw_input()`, so it raises a `SyntaxError` under `python3`.

## How to Run

```bash
python2 maincode.py
```

### Known limitation

The save path at the top of `maincode.py` is a hardcoded absolute Windows path pointing at the author's own machine, and the `savefile.txt` tracked in this repository is never read or written. What that means depends on the platform:

- On another Windows machine, the named directory does not exist, so the run ends in an `IOError` right after the opening question.
- On Linux or macOS, backslashes are ordinary filename characters rather than path separators. Answering `NO` therefore creates a junk file literally named `C:\Users\Daniel\Desktop\python\ProjectCave\savefile.txt` in the current directory and the game plays on from there, while answering `YES` ends in an `IOError` until such a file exists.

See [#2](https://github.com/Stephenson-Software/Cave-Console-Game/issues/2).

## How to Play

Answers are typed at the `>` prompt and are case-sensitive.

- `YES` or `NO` — whether a save file exists, whether to enter the cave, and whether to open the chest
- `DOWN` or `LEAVE` — at the hole in the chest
- `SAVE` — at any decision, to save progress and quit

Typing `SAVE` at the second or third decision raises a `NameError` when the session was started by loading a save rather than by starting a new game. See [#3](https://github.com/Stephenson-Software/Cave-Console-Game/issues/3).

## License

Licensed under the Stephenson Software Non-Commercial License (Stephenson-NC). See [LICENSE](LICENSE).
