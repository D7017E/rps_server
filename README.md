# Rock-Paper-Scissors

This is a repo for the rock-paper-scissor module.

## Prerequisites

- Python 3 - [Download and install Python 3](https://www.python.org/downloads/).

- Docker - [Download and install Docker](https://docs.docker.com/get-docker/). This is required to run the application in a container.

### Install dependencies

Use Pip to install the dependencies required to run the application.

```bash
pip install -r requirements.txt
```

## Usage

### Run the application

Start the application with:

```bash
flask --app src/app.py run
```

### Run the application in a container

Build the container with:

```bash
docker build -t rps_server .
```

Run the container with:

```bash
docker run -d --name rps_server -p 5000:5000 rps_server
```

The server is now running on port 5000 on your local machine and should be accessible at [http://localhost:5000](http://localhost:5000).

## Development

### Dependencies

All dependencies are managed by pip and are listed in the `requirements.txt` file.

If a new dependency is added, make sure to update the requirement file with name and version of the new dependency. The same applies when removing a dependency. To automatically update the requirements file `requirements.txt`, run:

```bash
pipreqs
```

NOTE: This will overwrite the existing `requirements.txt` file and will not take into account any manual changes made to the file such as manually specified package versions.

### Flask debug mode

To enable debug mode, use the `--debug` option when starting the application:

```bash
flask --app src/app.py --debug run
```

Debug mode will reload the application when changes are made to the source code and also provide a debugger in case of an exception to display traceback in browser.
