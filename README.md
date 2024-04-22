# 360-Video User Interface (UI)
This UI is designed for data monitoring for 360-Video service. This web server is based on a REST API that constantly 
updates the values from a remote service. This latter service should be hosted by another REST Server reachable by this 
service.
The data REST server is continuously receiving data from the HMD, which MUST be configured in DEMO MODE, this way, this
server can request data samples through HTTP GET operations.

The RESTful server as well as the Web one must run using the `restapi` environment created by using the `environment.yml`.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have `conda` installed on your machine. If you don't have it installed, you can download it from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Installing

1. Clone the repository to your local machine.

```bash
git clone <repository_url>
```

2. Navigate to the project directory.

```bash
cd <project_directory>
```

3. Create and activate the `restapi` conda environment using the `environment.yml` file.

```bash
conda env create -f environment.yml
conda activate restapi
```

## Running the Project

This project consists of two main Python files: `main.py` and `restapi.py`.

`main.py` runs the web user interface and `restapi.py` runs the RESTful server. Both files have configurable arguments such as host address and port.

To run the web user interface:

```bash
python main.py --host <host_address> --port <port_number>
```

To run the RESTful server:

```bash
python restapi.py --host <host_address> --port <port_number>
```

Replace `<host_address>` and `<port_number>` with your desired host address and port number.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.