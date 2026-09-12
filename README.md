# Cave-Console-Game

A short console text adventure, written to try out text adventure creation and saving/loading.

## Requirements

Python 2. `maincode.py` uses `print` statements and `raw_input()`, so it raises a `SyntaxError` under `python3`.

## How to Run

```bash
python2 maincode.py
```

The game may be started from any working directory; the save path is resolved relative to `maincode.py` itself.

## How to Play

Answers are typed at the `>` prompt and are case-sensitive.

- `YES` or `NO` — whether a save file exists, whether to enter the cave, and whether to open the chest
- `DOWN` or `LEAVE` — at the hole in the chest
- `SAVE` — at any decision, to save progress and quit

## Saving

Progress is written to `savefile.txt` beside `maincode.py` — the copy tracked in this repository. Typing `SAVE` records the name of the decision the player stopped at, and answering `YES` to the opening question resumes from it. Answering `YES` when that file is empty or absent is not an error; the game reports that no save was found and starts from the beginning. Because the file is tracked, playing the game leaves a modification in the working tree; `git checkout -- savefile.txt` discards it.

## License

Licensed under the Stephenson Software Non-Commercial License (Stephenson-NC). See [LICENSE](LICENSE).
