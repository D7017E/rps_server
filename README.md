# Rock-Paper-Scissors

A server application to expose an interface to an saved TensorFlow model and use it to identify a gesture from an image.

## Prerequisites

- Python 3.10 - [Download and install Python](https://www.python.org/downloads/).

- Docker - [Download and install Docker](https://docs.docker.com/get-docker/). This is required to run the application in a container.

### Install dependencies

Use Pip to install the dependencies required to run the application.

```bash
pip install -r requirements.txt
```

## Usage

The trained AI model should be created according to the structure presented in the TensorFlow documentation [save and serialize models](https://www.tensorflow.org/guide/keras/save_and_serialize#savedmodel_format) and must be placed in the `saved_models` directory.

The table below shows the environment variables available to configure the application. These variables can be set in the current terminal using the `export` command, e.g. `export RPS_SCHEMA_HOSTNAME=https://example.com/`.

| Variable              | Default                  | Description                                                  |
| --------------------- | ------------------------ | ------------------------------------------------------------ |
| `RPS_SCHEMA_HOSTNAME` | `http://localhost:5000/` | The external hostname used by end-user to access the server. |

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

### Endpoints

#### /predict/hand (method: GET)
* Description: This endpoint takes in a list of base64 encoded images and their shape, and returns a weighted prediction of the gesture shown in the images.
* Request Body:

```
{
    "image_list": [
        "base64 encoded image1",
        "base64 encoded image2",
        ...
    ],
    "shape": [height, width, channels]
}
```
image_list: An array of base64 encoded images

shape: Shape of the images in the format of [height, width, channels]

* Response:

```
{
    "prediction": "predicted gesture",
    "images": [
        "http://localhost:5000/predict/hand/image/image1.jpg",
        "http://localhost:5000/predict/hand/image/image2.jpg",
        ...
    ]
}
```

* prediction: A string representing the predicted gesture
images: An array of URLs to the images processed by the API. This field will be None if the images were not stored.



#### /predict/hand/image/\<filename>
The /predict/hand/image/\<filename> endpoint is a Flask route that allows you to retrieve the images that were processed by the API.

/predict/hand/image/\<filename> (method: GET)
* Description: This endpoint is used to retrieve the images processed by the API.
* Parameters:
    * filename: the name of the image file you want to retrieve.
* Response:
    * Returns the image file with the specified filename.

This endpoint is triggered when the client requests the URLs that are returned in the images field of the /predict/hand endpoint response. The filename parameter in this endpoint is extracted from the URL, it is used to locate the image on the server.

You will need to make sure that the images are stored in a location that is accessible by the API, and that the file path is properly configured in the code.

It's important to note that this endpoint requires the send_file method from the Flask library to work.

In summary, the /predict/hand/image/\<filename> endpoint is a Flask route that allows you to retrieve the images that were processed by the API, by providing the name of the image file. It uses the send_file method to retrieve the image file and send it to the client.