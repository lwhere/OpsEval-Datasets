# Scripts

## network_few_shot.py

Please split `data/test/Wired Network.json` to `data/test/Wired Network English.json` and `data/test/Wired Network Chinese.json` before executing the script.

3-shot is used for prompting.

### Parameters
- `en`: `1` for `data/test/Wired Network English.json`, `0` for `data/test/Wired Network Chinese.json`
- `cot`: `1` for using chain-of-thought
- `noq`: number of queries, `1` or `5`
- `model`: GroqCloud models: `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma-7b-it`, `whisper-large-v3`

## network_score.py

Used with `network_few_shot.py` to match answers and calculate scores. Same parameters as `network_few_shot.py`.
