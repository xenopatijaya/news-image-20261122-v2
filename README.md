[![Competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/xenopatijaya/news-image-20261122-v2/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/xenopatijaya/news-image-20261122-v2/reward.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# news-image-20261122 v2 — The World in One Day

Entry for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122): one 1024×1024 image summing up world news on **Sunday 22 November 2026**. A front-page broadsheet with three illustrated leads (COP31 running into Sunday with no deal in Antalya, Hong Kong's Election Committee polling day, and Australia's defence minister rejecting a U.S. report on AUKUS submarines), eleven illustrated story cards, and twenty-six numbered briefs — **40 dated stories across 7 regions**, every one of them first reported on Sunday 22 November 2026 itself. This v2 replaces the v1 page, whose cards still carried several 19–21 November stories; the date discipline is the headline change. Every picture is drawn in code with Pillow — no photos.

## Run

```sh
python3 draw.py   # renders entry.png (1024x1024, deterministic)
python3 main.py   # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

Requires Python 3.13 and Pillow. No network access is used at run time.
