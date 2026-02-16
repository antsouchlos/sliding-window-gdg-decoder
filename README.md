# sliding-window-gdg-decoder

This repo is a fork of https://github.com/gongaa/SlidingWindowDecoder, refactored to be able to be built easier.

## Install `sw-gdg` package

### Local system

```
$ uv venv --python 3.12
$ uv pip install .
$ uv pip install jupter
$ uv run juptyter-lab
```

### In docker container

```
$ docker build . -t gdg
$ docker run --rm -it -u `id -u`:`id -g` -v $PWD:$PWD -w $PWD --network=host gdg jupyter-lab
```

## Notebook contents

| Filenem                    | Description                                                                                                                                                                                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IBM.ipynb`                | Aims to reproduce the results in Figure 3 of the [IBM paper arXiv v1](https://arxiv.org/pdf/2308.07915v1.pdf) (they updated their numerical results in v2). `N72circuit.svg` is the visualization of the noiseless, single syndrome cycle Stim circuit of their Figure 7 for the [[72,12,6]] code.             |
| `Round Analysis.ipynb`     | Takes a closer look at the parity check matrix, explains the basic concept of sliding window decoding and show how the windows are extracted.                                                                                                                                                                  |
| `Sliding Window OSD.ipynb` | Vontains the complete pipleline of code/circuit creation, window extraction and BP+OSD is used to decode each window.                                                                                                                                                                                          |
| `Data noise.ipynb`         | Introduces basic usage of GDG, and is for producing Figure 4 of our paper.                                                                                                                                                                                                                                     |
| `Sliding Window GDG.ipynb` | Uses GDG on each window for decoding, for Figure 3 and 7.                                                                                                                                                                                                                                                      |
| `Syndrome code.ipynb`      | Is related to Appendix B.                                                                                                                                                                                                                                                                                      |
| `Misc.ipynb`               | Is not related to our paper, but demonstrates my implementation of the following papers: [BP4+OSD](https://quantum-journal.org/papers/q-2021-11-22-585/pdf/), [2BGA codes](https://arxiv.org/pdf/2306.16400.pdf), [CAMEL](https://arxiv.org/pdf/2401.06874.pdf), [BPGD](https://arxiv.org/pdf/2312.10950.pdf). |

