# OpenCTI PT NAD Connector

Connector for IoC distribution from OpenCTI to PT NAD.

The connector enables integration between OpenCTI platform and PT NAD, allowing creation and population of reputation lists in PT NAD with IOCs hosted in OpenCTI. The connector supports customizzation of both the names of the reputation lists created and the types of indicators of compromise being transmissted.

## Configuration and Installation
### OpenCTI Configuration

#### OpenCTI Connector User Creation

To create a user, you need to follow the path `Settings -> Security -> Users`, click on the “+” icon at the bottom of the screen. In the window that appears,enter your username, email, password and be sure to add it to the `Connectors` group. After creating a user, you need to save his access token - it will be required for the connector to work with OpenCTI.


#### OpenCTI IoC Distribution Settings
To distribute indicators via OpenCTI, go to `Data -> Data Sharing` and create a Stream. It can be public or private. If the Stream is private, its Stream ID will be required when setting up the connector.


### Connector Installation

#### Requirements
- Python >= 3.11
- pip

#### Configuration

| Parameter | Env var | Required | Description |
|----------|---------|------------|----------|
| `opencti_url` | `OPENCTI_URL` | Yes | OpenCTI URL|
| `opencti_token` | `OPENCTI_TOKEN` | Yes | Connector user token |
| `connector_id` | `CONNECTOR_ID` | Yes | A valid arbitrary `UUIDv4` that must be unique for this connector. |
| `connector_name` | `CONNECTOR_NAME` | Yes | Connector Name |
| `connector_type` | `CONNECTOR_TYPE` | Yes | Connector Type (always `STREAM`) |
| `connector_live_stream_id` | `CONNECTOR_LIVE_STREAM_ID` | Yes | OpenCTI STREAM ID |
| `connector_scope` | `CONNECTOR_SCOPE` | No | Distributed IoC Type  (by default `ip,dn,url,md5`) |
| `ptnad_url` | `PTNAD_URL` | Yes | PT NAD URL |
| `ptnad_ssl_verify` | `PTNAD_SSL_VERIFY` | No | By default ssl verification is off |
| `ptnad_token` | `PTNAD_TOKEN` | Yes (if you use PT MC) | PT NAD Access Token |
| `ptnad_username` | `PTNAD_USERNAME` | Yes (if token absent) | PT NAD Username |
| `ptnad_password` | `PTNAD_PASSWORD` | Yes (if token absent) | PT NAD Password |
| `ptnad_ip_replist_name` | `PTNAD_IP_REPLIST_NAME` | No | Name of IP Reputation List (by default `opencti-ip-replist`) |
| `ptnad_dn_replist_name` | `PTNAD_DN_REPLIST_NAME` | No | Name of DNS Reputation List (by default `opencti-dn-replist`) |
| `ptnad_url_replist_name` | `PTNAD_URL_REPLIST_NAME` | No | Name of URL Reputation List (by default `opencti-url-replist`) |
| `ptnad_md5_replist_name` | `PTNAD_MD5_REPLIST_NAME` | No | Name of MD5 Reputation List (by default `opencti-md5-replist`) |
| `ptnad_ip_external_key` | `PTNAD_IP_EXTERNAL_KEY` | No | `external_key` parameter for IP Reputation List (by default `opencti-ip`) |
| `ptnad_dn_external_key` | `PTNAD_DN_EXTERNAL_KEY` | No | `external_key` parameter for DNS Reputation List (by default`opencti-dn`) |
| `ptnad_url_external_key` | `PTNAD_URL_EXTERNAL_KEY` | No | `external_key` parameter URL Reputation List (by default `opencti-url`) |
| `ptnad_md5_external_key` | `PTNAD_MD5_EXTERNAL_KEY` | No |  `external_key` parameter MD5 Reputation List (by default `opencti-md5`) |


#### Dependicies Installation
```
pip install -r src/requirements.txt
```
#### Start connector
```
cd src
python ptnad_connector.py
```

#### Launch in Container

Repository contains `Dockerfile` for image building and `docker-compose.yaml` for running the connector.

> To create several reputatiom lists of the the same IoC types you must launch separate connector instance with different `external_key` and Reputation List Name


## License
The Project Distributed with MIT License. [License file](../../LICENSE)