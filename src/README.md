# Scripts

## network_run.py

Please split `data/test/Wired Network.json` to `data/test/Wired Network English.json` and `data/test/Wired Network Chinese.json` before executing the script.

### Parameters
- `en`: Language. `1` for `Wired Network English.json`, `0` for `Wired Network Chinese.json`.
- `cot`: Chain-of-thought. `1` for using CoT, `0` otherwise.
- `noq`: Number of queries for self-consistency. Suggest `5` for sc.
- `shot`: Few-shot. `0` for zero-shot, `3` for 3-shot.
- `model`: GroqCloud models. `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma-7b-it`, `whisper-large-v3`.
- `structure`: Response format (Not API parameter). `json` for returning JSON.

## network_score.py

Used with `network_run.py` to match answers and calculate scores. Same parameters as `network_run.py`.

## Leaderboard

### Wired Network Operations (English)
| | Zero-shot | | | | 3-shot | | | | |
|------|------|------|------|------|------|------|------|------|------|
| Models | Naïve | SC | CoT | CoT+SC | Naïve | SC | CoT | CoT+SC | Best Score |
| Gemma-7B-IT | 21.05 | 20.54 | 12.58 | 12.71 | 49.94 | 50.19 | 47.11 | 47.88 | 50.19 |
