## RUN IMAGE FROM GHCR 

```sh
docker run --gpus all -it --env-file .env ghcr.io/semantic-search/neural-talk2

```

To build the docker image locally, run: 

```git
    git clone --recurse-submodules https://github.com/semantic-search/neural-talk2

```

```
docker build -t neural-talk .
```

```
docker run --gpus all --env-file .env -it neural-talk
```
