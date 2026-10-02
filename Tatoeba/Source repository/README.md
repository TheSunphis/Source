# Tatoeba Japanese–English Sentence Packs

232,778 unique Japanese sentences with English translations and furigana,
**ordered by everyday commonness** (rank 1 = most everyday), packaged into
packs of 100 JSON files × 250 sentences.

## Layout

```
Tatoeba/
├── Pack 1/    pack1_001.json … pack1_100.json    ranks 1–25,000      (most everyday)
├── Pack 2/    pack2_001.json … pack2_100.json    ranks 25,001–50,000
├── …
├── Pack 9/    pack9_001.json … pack9_100.json    ranks 200,001–225,000
├── Pack 10/   pack10_001.json … pack10_032.json  ranks 225,001–232,778 (partial: 7,778 sentences)
└── Source repository/
    ├── README.md                        (this file)
    ├── manifest.json                    (machine-readable index of every pack & file)
    ├── tatoeba_all_pairs_sorted.json.bz2 (the master dataset the packs were split from)
    └── scripts/
        ├── tatoeba_bulk.py              (download + build pairs from Tatoeba exports)
        ├── sort_by_frequency.py         (everyday-commonness scoring & ranking)
        └── split_packs.py               (packaging into packs/files)
```

## File schema

Each pack file is self-describing:

```json
{
  "meta": { "pack": 1, "file": 1, "sentences": 250, "rank_range": [1, 250], "source": "...", "license": "..." },
  "sentences": [
    {
      "rank": 1,                          // 1 = most everyday/common
      "freq_score": 7.07,                 // higher = more everyday (see below)
      "ja_id": 11053934,                  // Tatoeba sentence id
      "ja": "いつしたい？",
      "ja_furigana": "いつしたい？",        // reading, format 漢字[漢|かん]; plain text if no kanji
      "translations": [                   // ALL direct English translations
        { "en_id": 6949897, "en": "When do you like to do that?" }
      ]
    }
  ]
}
```

All translations of one Japanese sentence live in the same file — a sentence
never spans two files.

## Totals

| | |
|---|---|
| Unique Japanese sentences | 232,778 |
| Translation pairs | 280,520 |
| Packs | 10 (last one partial) |
| Files | 932 (100 per pack; Pack 10 has 32) |
| Sentences per file | 250 (Pack 10's last file has 28) |

## How the ranking works

`freq_score` = mean **zipf word frequency** of the sentence's content words
(nouns/verbs/adjectives/adverbs/interjections, UniDic lemmas via fugashi),
using the **wordfreq** Japanese frequency data (built from Twitter, subtitles
and the web — a proxy for everyday language), minus a 0.05-per-token length
penalty. Unknown/rare words count as 1.0 and pull the score down hard.
Function words (particles etc.) are excluded so they can't inflate scores.
Ties are broken by sentence length, then id. It is a good approximation, not
ground truth.

## Source & license

- Data: **Tatoeba.org** weekly exports, https://downloads.tatoeba.org/exports/
  (per-language files; export of 2026-09-26).
- Sentences are **CC BY 2.0 FR** (some CC0). Attribution: Tatoeba.org
  contributors. If you redistribute these packs, keep the attribution.

## Regenerating everything from scratch

```bash
pip install requests fugashi unidic-lite wordfreq
python scripts/tatoeba_bulk.py --all                # -> tatoeba_all_pairs.json   (~25 s)
python scripts/sort_by_frequency.py                 # -> tatoeba_all_pairs_sorted.json (~25 s)
python scripts/split_packs.py                       # -> Tatoeba/Pack 1..10 + manifest
```

Generated: 2026-10-02.
