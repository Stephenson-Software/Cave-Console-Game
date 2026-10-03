# Cave-Console-Game

[![Play in your browser](https://img.shields.io/badge/Play-in%20your%20browser-2ea44f)](https://danielstephenson.dev/play/cave-console-game)

A short console text adventure, written to try out text adventure creation and saving/loading.

## Requirements

Python 3, standard library only. (It was written for Python 2 and ported to Python 3 when it was put in the browser.)

## How to Run

```bash
python3 maincode.py
```

The game may be started from any working directory; the save path is resolved relative to `maincode.py` itself.

## How to Play

Answers are typed at the `>` prompt; case and surrounding spaces do not matter (`yes`, `YES` and ` Yes ` are the same answer).

- `YES` or `NO` — whether a save file exists, whether to enter the cave, and whether to open the chest
- `DOWN` or `LEAVE` — at the hole in the chest
- `SAVE` — at any decision, to save progress and quit

## Saving

Progress is written to `savefile.txt` beside `maincode.py` — the copy tracked in this repository. Typing `SAVE` records the name of the decision the player stopped at, and answering `YES` to the opening question resumes from it. Answering `YES` when that file is empty or absent is not an error; the game reports that no save was found and starts from the beginning. Because the file is tracked, playing the game leaves a modification in the working tree; `git checkout -- savefile.txt` discards it.

## Tests

The tests in `tests/` play the game with scripted answers and check every ending, saving and loading. They use only the standard library and save to a temporary file, so `savefile.txt` is left untouched:

```bash
python3 -m unittest discover -s tests -t .
```

## Play in your browser
The same game, unmodified, runs in a browser tab under [tak](https://github.com/Stephenson-Software/tak)'s console runtime (Python via Pyodide): https://cave.play.danielstephenson.dev, listed with the rest at [danielstephenson.dev/play](https://danielstephenson.dev/play). To build and serve it locally (needs `tak` installed):
```
python3 web/build_zip.py
python3 -c "from tak.web.serve import main; main(root='.', title='Cave')"
```
Pushes to `master` deploy it to [arcade](https://github.com/Stephenson-Software/arcade) (`.github/workflows/browser.yml`).

## License

Licensed under the Stephenson Software Non-Commercial License (Stephenson-NC). See [LICENSE](LICENSE).
