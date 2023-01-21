# Contributing to the project

This guide is intended for developers who want to contribute to the project. It contains information about how to set up the development environment and how to run and/or debug the application.

## Table of Contents

- [Contributing to the project](#contributing-to-the-project)
  - [Table of Contents](#table-of-contents)
  - [Getting started](#getting-started)
  - [Development](#development)
    - [Environment setup](#environment-setup)
      - [Prerequisites](#prerequisites)
    - [Python modules](#python-modules)
    - [Debug and run the application](#debug-and-run-the-application)
    - [Build the docker image](#build-the-docker-image)
    - [Testing](#testing)

## Getting started

Contributions are made to this repo via Issues and Pull Requests (PRs). Before you open a new issue or PR, please make sure that you have searched for existing Issues and PRs before creating your own.

## Development

In this section, you will find information about how to set up the development environment and how to run and/or debug the application.

### Environment setup

#### Prerequisites

- [Python 3.10](https://www.python.org/downloads/) with Pip
- [Docker](https://docs.docker.com/get-docker/) *(optional)*

When all prerequisites are installed, clone the repository and navigate to the project root directory. Use Pip to install the dependencies required to run the application:

```bash
pip install -r requirements.txt
```

### Python modules

The project uses a range of Python modules from PyPI to run the application and are listed in the `requirements.txt` file. In case you want to add a new module, make sure to add it to `requirements.txt`.

### Debug and run the application

The application can be started by using the flask development server. To start the server in debug mode, run the following command:

```bash
flask --app src/app.py --debug run
```

When in debug mode, the application will restart when changes are made to the source code and also provide a debugger in case of an exception to display traceback in a web browser and a call stack in the terminal.

If you want to run the application without debug mode, remove the `--debug` flag:

```bash
flask --app src/app.py run
```

### Build the docker image

The docker image can be built by running the following command:

```bash
docker build -t <MY-IMAGE-TAG>  .
```

Replace `<MY-IMAGE-TAG>` with the desired image tag to be used when running the image.

### Testing

The application uses no external testing framework and therefore does not require any additional setup. Instead, the application uses the built-in `unittest` module to run tests. Test files are located in the project alongside the source code and are named `*_test.py`.

To run a test you run the selected file as a regular python file, for example:

```console
pepper@pc:~/rps$ python src/prediction_test.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```
