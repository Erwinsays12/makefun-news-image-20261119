[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Erwinsays12/makefun-news-image-20261119/rank.svg)](https://make.fun/c/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Erwinsays12/makefun-news-image-20261119/reward.svg)](https://make.fun/c/news-image-20261119)

# World News in One Image — Thursday, 19 November 2026

A newspaper-style front page that sums up Thursday 19 November 2026 in a
single 1024×1024 image: the global rollout of Grand Theft Auto VI, the
first-ever Trump–Xi–Putin trilateral meeting set for the APEC summit in
Shenzhen, Hakeem Jeffries poised to become the first Black Speaker of the
US House, Cyclone Akvan nearing India's east coast, Voyager 1 reaching a
light-day from Earth, the EU's proposed €45bn Ukraine loan, and Pew
Research's projection that Islam becomes the world's largest religion by
2035.

## How it works

- `draw_poster.py` renders the poster with Pillow and the system DejaVu
  fonts — flat vector-style art and crisp text, no photographs, no network.
- `entry.png` is the rendered poster (1024×1024, under 1 MiB).
- `main.py` (Python 3.13, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, so both grader runs write identical
  bytes.

## Run it locally

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for the [news-image-20261119 competition](https://make.fun/c/news-image-20261119)
on [make.fun](https://make.fun).
