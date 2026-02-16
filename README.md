# sliding-window-gdg-decoder

This repo is a fork of https://github.com/gongaa/SlidingWindowDecoder,
refactored to be able to be built easier.

## Install `sw-gdg` packag

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
| `data-noise.ipynb`         | Introduces basic usage of GDG, and is for producing Figure 4 of our paper.                                                                                                                                                                                                                                     |
| `ibm.ipynb`                | Aims to reproduce the results in Figure 3 of the [IBM paper arXiv v1](https://arxiv.org/pdf/2308.07915v1.pdf) (they updated their numerical results in v2). `N72circuit.svg` is the visualization of the noiseless, single syndrome cycle Stim circuit of their Figure 7 for the \[[72,12,6]\] code.           |
| `misc.ipynb`               | Is not related to our paper, but demonstrates my implementation of the following papers: [BP4+OSD](https://quantum-journal.org/papers/q-2021-11-22-585/pdf/), [2BGA codes](https://arxiv.org/pdf/2306.16400.pdf), [CAMEL](https://arxiv.org/pdf/2401.06874.pdf), [BPGD](https://arxiv.org/pdf/2312.10950.pdf). |
| `round-analysis.ipynb`     | Takes a closer look at the parity check matrix, explains the basic concept of sliding window decoding and show how the windows are extracted.                                                                                                                                                                  |
| `sliding-window-gdg.ipynb` | Uses GDG on each window for decoding, for Figure 3 and 7.                                                                                                                                                                                                                                                      |
| `sliding-window-osd.ipynb` | Vontains the complete pipleline of code/circuit creation, window extraction and BP+OSD is used to decode each window.                                                                                                                                                                                          |
| `syndrome-code.ipynb`      | Is related to Appendix B.                                                                                                                                                                                                                                                                                      |

## Remarks by the original author (parts of FAQ.md from original repo)

### 1. How is your BB syndrome extraction circuit different from the [official implementation](https://github.com/sbravyi/BivariateBicycleCodes)?

After uncommenting lines 145, 170, 206 from `src/build_circuit.py` you should
be able to recover their results. I wrote this circuit and ran all the relevant
numerics before Bravyi et al. updated their paper to version two on arXiv (and
released their source code). In the author comments for arXiv v2 they said that
they fixed some bugs and hence logical error rate went up. At my time of
programming, I tried to match up with their first version, so I removed all
possible extra error sources (idling errors and flips before transversal
measurement). By extra I mean those that do not affect the circuit-level PCM,
but the prior probabilities associated with some columns of the PCM.

#### 2.3 I am using Linux and I managed to compile, however, my CPU is not Intel i9 13900K, can I still use GDG?

Yes, you can

- either by using single thread version of GDG only (toggle
  `multi_thread=False`). Single thread GDG (with suitable parameters) is still
  faster and more accurate than BP+OSD when used in window decoding.
- or, if your CPU is similar, you can still try running multi-thread GDG; if it
  does not work, you can change the thread to core assignment in line 605 and
  612 of `/src/include/bpgd.cpp` (please read through `Data noise.ipynb` before
  doing so).

#### 2.4 How did you measure the worst-case latency of GDG?

As claimed in the abstract of our paper, the worst-case latency is around 3ms.
This is demonstrated in `Sliding Window GDG.ipynb`. Please note that we only
measure the *theoretical* worst-case latency, namely those samples that GDG
failed to converge on. Otherwise, there would be occasional spikes at 10ms,
this is a problem with all CPU decoders; it is also encounted in the
[Google's surface code experiments](https://arxiv.org/pdf/2408.13687) Figure
S3. I think this is an OS issue and though I linked to
[this post](https://shuhaowu.com/blog/2022/01-linux-rt-appdev-part1.html), I
did not solve it myself.

Switching to GPU could be a solution. In my latency probing of the CUDA BP
decoder, I did not observe such spikes, therefore I plan to implement a CUDA
version of GDG. I should say beforehand that I don't expect the *theoretical*
worst-case latency to improve much, since 200 iterations of CUDA BP takes 2ms
on my RTX4090.

### 3. Heuristics

#### 3.1 How do you tune BP+OSD parameters?

For the scaling factor, on code-capacity noise (data qubit noise), I try all
four values from {0.5, 0.625, 0.8, 1.0} and pick the best one. For BB codes,
see Fig. 4 from our paper for the best scaling factors. For circuit-level
noise, from my experience $1.0$ is okay, probably because the Tanner graph is
highly-irregular.

For BP iterations, I just set it to 100~200 for code-capcity noise without any
tuning; I think a suitable scaling factor is more important there. However, for
circuit-level noise, since I was doing the shortening trick to the wide
circuit-level PCM (see `Sliding Window OSD.ipynb` for details) before running
GDG, I found that running BP for too many iterations before shortening causes
error floor.

#### 3.2 What are the main features of GDG?

GDG is an ensembled BP-based decoder and there is no dependency within the
ensemble. Moreover, it is iterative and each time it chooses the
most-likely-to-flip VN to decimate. Each agent within the ensemble either
decimates that VN according to the sign of the BP posterior LLR, or contrary to
that, this is prefixed for each agent.

#### 3.3 If I want to design other decoders, what heuristics can be transferred there?

- One could use LLR history to perform decisions, in our paper, we mostly only
  used the sum of the history, maybe better criterions can be devised.
- The shortening trick for circuit-level noise could be widely applicable.
