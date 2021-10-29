# Compare UV-Vis spectra

## How to use

1. Upload UV-Vis JSON files converted using [uv2json](https://github.com/chanana/uv2json)
2. Calculate the Euclidean (or Cosine) distance between them
3. Download the final distance matrix

## Setup

Run `setup_env.sh` **or** the following set of commands

```bash
python3 -m venv .venv # setup venv

source .venv/bin/activate # activate environment

pip install --upgrade pip wheel \
            black flake8 \
            dash_bootstrap_components \
            plotly numpy pandas # install packages
```

## Notes on interpretation

1. Euclidean distances are the same as L2 norms and are referenced as such in the functions. <b>Larger number = more dissimilar samples</b>.
2. [Cosine scores](https://en.wikipedia.org/wiki/Cosine_similarity) are typically between `[-1, 1]`. -1 means completely different and 1 means exactly the same. Since UV-Vis spectra are typically positive, this is modified to `[0, 1]` with <b>0 = completely different and 1 = exactly the same</b>.