# Rock-Paper-Scissors

A web service to expose an interface to an AI model to identify a rock, paper, and scissors hand gesture in images of a person. The AI model is a combination of the MediaPipe hand detection model and a KNN utilizing a dataset of joint coordinates of a person's making a rock, paper, and scissors gesture.

This web service is one part of a project to make the robot [Pepper](https://www.aldebaran.com/en/pepper) play a game of rock paper scissors. See the [Rock-Paper-Scissors](https://github.com/PepperonIT/Rock-Paper-Scissors) repository for more information.

## Tools

- Docker - [Download and install Docker](https://docs.docker.com/get-docker/).

## Usage

A pre-built Docker image is available on [Docker Hub](https://hub.docker.com/r/pepperonit/rps_server). If you want to build your image from the source, refer to the [development guide](CONTRIBUTING.md) for more information on how to build the image.

To automatically pull the latest version of the pre-built image and create a container with it, use the following command:

```bash
docker run -d --name rps_server -p 5000:5000 -e RPS_SCHEMA_HOSTNAME=<HOSTNAME> pepperonit/rps_server:latest
```

Replace `<HOSTNAME>` with the external hostname used by the end-user to access the server. For example, if the server is running on a machine, accessible at `https://example.com:5400`, then the value of `<HOSTNAME>` should be `https://example.com:5400`. To run the server attached to the current terminal, remove the `-d` option from the command above.

The server is now running on port 5000 on your local machine and should be accessible at [http://localhost:5000](http://localhost:5000).

### Examples

#### Run the server with the latest image

Run the server with the hostname `https://example.com:5400` using the latest version of the image:

```bash
docker run -d -p 5000:5000 -e RPS_SCHEMA_HOSTNAME="https://example.com:5400" pepperonit/rps_server:latest
```

#### Persistent storage of images and joint coordinates

Run the server with a volume mounted to the container to store any images saved by the server during a gesture prediction. This is useful for any debugging purposes or to store the images for future training of the AI model. The volume should be mounted to the `/app/saved_models/data_collection` directory in the container.

```bash
docker run -d -p 5000:5000 --name rps_server \
  -v /home/pepper/rps/saved_models/data_collection:/app/saved_models/data_collection \
  -e RPS_SCHEMA_HOSTNAME="https://example.com:5400" \
  pepperonit/rps_server:latest
```

## Endpoints

There are two endpoints for the RPS-server `/predict/hand` and `/predict/hand/image/<filename>`. Where `/predict/hand/` is used to query the AI-model for the game gesture shown in the attached image. `/predict/hand/image/<filename>` is used to retrieve the image with the graphed points from mediapipe. This modified image is displayed to users as a visual aid when announcing results from game rounds.

### GET `/predict/hand/`

Takes a list of Base64 encoded images along with information about the image dimensions and data type. All images must be the same dimensions and data type. If the images do not have the same dimensions and data type, the request will fail and return an error.

* Takes
  * "image_list": [Base64, ...]
    * Currently only uses the first image from the list
  * "shape": [int, int, int]
    * shape order is, [height, width, channels]
  * "dtype": \<str>
    * a string representation of a numpy [dtype](https://numpy.org/doc/stable/reference/arrays.dtypes.html)
* Returns
  * "prediction": \<str>
    * string representation of predicted gesture, or fail state
  * "images": { processed: str, raw: str }
    * URL path on server for the image used to predict image, or None

### GET `/predict/hand/image/<filename>`

The `/predict/hand/image/<filename>` endpoint allows for retrieving the images that were processed by the AI-model. This endpoint does not take any data outside of the URL, where the \<filename> designates the location of the image on the server. This is given to the API user when a prediction request is sent. When called on an existing file path the endpoint returns that image stored there.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up the development environment on your local machine and how to suggest changes or enhancements to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
