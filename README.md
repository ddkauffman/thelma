# THELMA

A web-based [Django](https://www.djangoproject.com/) application for observatory engineering telemetry plots, analysis, and trending.

The application's intended purpose is to provide engineers a front-end to JWST Engineering Telemetry Archive (JETA). JETA is a component of jSka, which was derived from the Ska tools for the Chandra spacecraft, as a superset of those tools retro fitted for JWST. Thelma is designed to encapsulate the most commonly used tools for rapid anomaly response and analysis. The capability to manage the telemetry archive and monitor archive status via a browser is also a key feature of the application.

## Getting Started

- TBD

### Prerequisites

For a list of python packages required to run the application see requirements.txt in repository root.

Thelma depends on a separete RESTful API [RAVEN](https://github.com/spacetelescope/RAVEN) to handle the direct interface with jSka.

## Environment Variables

For local development environment variables configured in a `.env` file. These same variables
need to be set inside the Docker container for running on server in test or production.


```bash
# Service-level Variables
WORKERS=2
PORT=8002

# Application-level Variables
# THELMA_SECRET_KEY maps directly and is used in the same way as https://docs.djangoproject.com/en/1.11/ref/settings/#secret-key
THELMA_SECRET_KEY=<a secret key>

# Version Information
# Follows closely the semver.org definition
MAJOR_VERSION=1
MINOR_VERSION=0
PATCH_LEVEL=0
RELEASE=pre-alpha

# TELEMETRY API Variables
TELEMETRY_API_HOST=<fqdn of API host>
TELEMETRY_API_PORT=<api port>

# Django Configuration
DJANGO_SETTINGS_MODULE=config.settings.base

# Not relevant when running locally, but matters on a remote dev, test or prod server.
# Must be provided by sys/network admin. The default below is for Mac docker's defaults.
NETWORK_SUBNET=10.0.0.0/24
```

### Installing

- TBD

## Running the tests

```bash
python manage.py test
```

## Coding Style

https://github.com/spacetelescope/style-guides

## Built With

* [Django](https://docs.djangoproject.com/en/1.11/)- The web framework used is Django 1.11.x
* [Foundation](https://foundation.zurb.com/sites.html) - Responsive framework
* [Chandra Tools](https://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/index.html) - Built around Chandra Tools

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [THELMA](https://github.com/ddkauffman/thelma).


## Authors

* **David Kauffman** - *Initial work* - [David Kauffman](https://github.com/ddkauffman)

## Acknowledgments

* Amanda Arvai
* Tom Aldcroft
* Jean Connelly
