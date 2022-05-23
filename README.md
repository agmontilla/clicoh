# ClicOH - Technical Interview

This is an app that offers the basic functionality of an ecommerce platform

## Running the app

To run this app, you need to install docker first. After that you move to the folder that you have download this repo, then you should execute

```bash
docker build -t {IMAGE_NAME}
```

Where `{IMAGE_NAME}` is the name of the images that will be created. After creating the image, you can run a container using:

```bash
docker run -d --name {CONTAINER_NAME} -p 8080:8080 {IMAGE_NAME}
```

Again, `{CONTAINER_NAME}` is just the name of the container what you prefer.

## TODO

### High Priority :red_circle:

- Add more tests
- Add integration with a DB like postgresql instead of sqlite (adding the possibility to deploy this app in heroku or pythonanywhere)
- Remove hardcode values
- Add samples of responses in decorator to documenting in a better way (using swagger)

### Medium Priority :white_circle:

- Create function as `create_app` in conftest
- Add docstrings to functions

### Low Priority :large_blue_circle:

- Caching poetry installation is not working
- Adding coverage report (testing)
