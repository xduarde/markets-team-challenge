# markets-team-challenge

Project to extract and ingest market crypto data from GeckoAPI. Data pipeline developed in Python, orchestrated in Airflow and implemented in Docker.


## Getting Started

### Installation

Clone the repository.

```bash
git clone https://github.com/xduarde/markets-team-challenge.git
```
```bash
cd markets-team-challenge
```


## Usage

The pipeline is deployed from a [Docker](https://docs.docker.com/get-docker/) container, through an [Airflow image](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

The follow command deploys the environment and initialize the pipeline:

```bash
docker compose up --build
```

![alt text](/img/denue-diagram.png)

In order to monitor the ingest_crypto_data, access the Airflow Web Server in:

> **[http://localhost:8080/](http://localhost:8080/)** 



## License

Distributed under the MIT License. See LICENSE for more information.