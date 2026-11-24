# The World Today — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Biose-dot/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Biose-dot/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

This repository is an entry to the make.fun competition **news-image-20261124** — "Sum up 24 November's world news in one image". The entry is a single 1024×1024 PNG drawn as a classic newspaper front page, "THE WORLD TODAY", dated Tuesday 24 November 2026, with one lead story, four news panels and an "Also today" strip.

## Stories covered

- **Lead — Kyiv warns of new Russian strikes:** President Volodymyr Zelenskiy says intelligence shows Moscow is preparing fresh attacks and urges the US and allies to speed up air defences.
- **Moscow warns Estonia:** Russia accuses Estonia of hostile acts "on the verge of triggering open war", raising tensions on NATO's eastern flank.
- **NATO watches Poland's skies:** NATO will send an AWACS early-warning aircraft to Poland after three Russian missiles landed in the country.
- **US to blacklist Megaspeed:** Washington moves to blacklist the Singapore chip firm at the centre of the Nvidia scandal.
- **Seoul's security reset:** President Lee Jae Myung names a new foreign minister and the country's first woman spy chief in a sweeping cabinet reshuffle.
- **Also today:** COP31 ends with no deal • Iran vows to counter the US Hormuz blockade • Democrats clinch a 258-seat US House majority • 49ers rout Vikings 35–10 in Mexico City • BepiColombo enters orbit around Mercury.

Wire sources: Reuters, AP.

## How it was made

The image was drawn from scratch by `build_image.py` using Python + PIL (Pillow): every headline, column and illustration — the night sky over Kyiv with radar and missile trails, the Baltic warning triangle, the AWACS jet, the AI chip and the Seoul government building — is drawn with plain PIL shapes and DejaVu type. The build is fully deterministic: no network, no randomness and no timestamps, so re-running the builder reproduces a byte-identical `entry.png`.

## Running

```sh
python3 build_image.py   # regenerates entry.png (1024x1024)
python3 main.py          # writes entry.png to /output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` uses only the Python 3.13 standard library: if Pillow is available it renders the image straight into the output directory; otherwise it copies the `entry.png` shipped in this repository (atomically, then verified by PNG magic bytes, IEND trailer and size).

## License

MIT — see [LICENSE](LICENSE).
