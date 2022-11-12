# Rock-Paper-Scissors

A server application to expose an interface to an saved TensorFlow model and use it to identify a gesture from an image.

## Prerequisites

- Python 3 - [Download and install Python 3](https://www.python.org/downloads/).

- Docker - [Download and install Docker](https://docs.docker.com/get-docker/). This is required to run the application in a container.

### Install dependencies

Use Pip to install the dependencies required to run the application.

```bash
pip install -r requirements.txt
```

## Usage

The trained AI model should be created according to the structure presented in the TensorFlow documentation [save and serialize models](https://www.tensorflow.org/guide/keras/save_and_serialize#savedmodel_format) and must be placed in the `saved_models` directory.

The table below shows the environment variables available to configure the application. These variables can be set in a `.env` file (see [python-dotenv](https://github.com/theskumar/python-dotenv#getting-started)) in the root directory of the project or in the current terminal using the `export` command, e.g. `export AI_INPUT_SHAPE=(1, 100, 100, 1)`. Variables set in the `.env` file have higher precedence over the ones set in the terminal.

| Variable         | Default            | Description                                                  |
| ---------------- | ------------------ | ------------------------------------------------------------ |
| `AI_MODEL_NAME`  | `pneumonia`        | Name of saved model to use, stored in `saved_models` folder. |
| `AI_INPUT_SHAPE` | `(1, 100, 100, 1)` | Shape of image to feed to the AI model.                      |

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
