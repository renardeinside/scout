# SCOUT (Single-cell and Cytoarchitecture Analysis of Organoids using Unbiased Techniques)

This project is a fork of original [SCOUT](https://github.com/chunglabmit/scout) project, with some simplifications and Docker packaging in-place.

Ready to use docker packages could be found [here](https://hub.docker.com/r/renardeinside/scout).

## Using the dockerized image

- Pull the image from Docker via:

```bash
docker pull renardeinside/scout:latest
```

- Run the image to see available commands:

```bash
docker run renardeinside/scout:latest
```

- To provide data from your local machine please use docker volume mounts:

```bash
cd /your/directory/with/data
docker run -v "$(pwd):/scout/data" renardeinside/scout:latest <scout commands and parameters>
```

Please use the [walkthough documentation](https://chunglabmit.github.io/scout/test_data.html#walkthrough-with-test-data) for examples.

## TBDs

- Refactor dependency management (split main CLI from experimental notebooks etc)
- Appy code formatting (black + isort)
