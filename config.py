import inspect
import os
from typing import List


class BaseConfig(object):
    # Environment flags
    ENVIRONMENT = None
    IS_DEV = None

    # Authentication
    AUTH_HOST = os.environ.get("AUTH_HOST", default=None)
    AUTH_SERVICE_REALM = os.environ.get("AUTH_SERVICE_REALM", default="namak")
    AUTH_SERVICE_CLIENT_ID = os.environ.get("AUTH_SERVICE_CLIENT_ID", default="warehouse-binning-service")
    AUTH_SERVICE_CLIENT_SECRET = os.environ.get("AUTH_SERVICE_CLIENT_SECRET", default=None)

    # Rabbit MQ
    RABBITMQ_EXCHANGE_NAME = os.environ.get("RABBITMQ_EXCHANGE_NAME", default="namak.logistics.binning")
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", default=5672)
    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", default=None)
    RABBITMQ_USER = os.environ.get("RABBITMQ_USER", default=None)
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", default=None)
    RABBITMQ_VIRTUALHOST = os.environ.get("RABBITMQ_VIRTUALHOST", default=None)

    # Postgres
    PG_USER = os.environ.get("PG_USER", default="benjamin")
    PG_PASSWORD = os.environ.get("PG_PASSWORD", default="")
    PG_HOST = os.environ.get("PG_HOST", default="localhost")
    PG_PORT = os.environ.get("PG_PORT", default="5432")
    PG_DATABASE = os.environ.get("PG_DATABASE", default="binning")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode=require"

    # Logging
    ELASTIC_LOGGING_URI = os.environ.get("ELASTIC_LOGGING_URI", default=None)
    SUMO_LOGGING_URI = os.environ.get("SUMO_LOGGING_URI", default=None)

    # external APIs
    NAMAK_ROOT_URI = os.environ.get("NAMAK_ROOT_URI", default=None)
    LEGACY_API_URI = os.environ.get("LEGACY_API_URI", default=None)

    # Product locks
    # how long a product lock is initally valid until it's closed
    PRODUCT_LOCK_INITIAL_LIFETIME_MINUTES = 20
    # how long a product lock is extended upon operator interactivity
    PRODUCT_LOCK_EXTENSION_LIFETIME_MINUTES = 15

    # Flask configuration
    # This needs to be set in order to trigger the error handlers for authentication stuff
    PROPAGATE_EXCEPTIONS = True

    def validate(self) -> List[str]:
        """ Performs a quick self-test and checks whether all settings have a value assigned (not None) """

        missing = []
        for name, val in inspect.getmembers(self):
            if name.startswith("_"):
                continue
            if val is None:
                missing.append(name)

        return missing


class DevelopmentConfig(BaseConfig):
    # Environment flags
    ENVIRONMENT = "DEV"
    IS_DEV = True

    # AUTH
    AUTH_HOST = os.environ.get("AUTH_HOST", default="https://api-dev.felfel.ch/auth")
    AUTH_SERVICE_CLIENT_SECRET = os.environ.get("AUTH_SERVICE_CLIENT_SECRET", default=None)

    # Rabbit MQ
    RABBITMQ_HOST = "rabbitmq.namak.ch"
    RABBITMQ_USER = "namak-dev"
    RABBITMQ_PASSWORD = "Ahji4ahmahVi5chae4jaijeicohV7gae"
    RABBITMQ_VIRTUALHOST = "namak-dev"

    ELASTIC_LOGGING_URI = "https://listener.logz.io:8071/?token=itAcKdeCyHzxLpkJMmBDazlEdlIyQvwo&type=dev/logistics/binning"
    SUMO_LOGGING_URI = "https://collectors.de.sumologic.com/receiver/v1/http/ZaVnC4dhaV2bjNoP4SPTO9kxcjdNBNYMhf8MTZci1zG3HYsjnWh4vNCneVeWp7HZGW4cbimAzXDMQLnYTDTfQV9IxAZgLuLcwQD4EA4lWeCk7Ovu1GQpcw=="

    # external APIs
    WAREHOUSE_API_URI = os.environ.get("BINNING_SCOPE_API_URI", default="https://felfel-dev.azure-api.net")
    LEGACY_API_URI = os.environ.get("LEGACY_API_URI", default="https://api-dev.felfel.ch")


class ProductionConfig(BaseConfig):
    # Environment flags
    ENVIRONMENT = "PROD"
    IS_DEV = False

    # AUTH
    AUTH_HOST = os.environ.get("AUTH_HOST", default="https://auth.felfel.ch/auth")

    ELASTIC_LOGGING_URI = "https://listener.logz.io:8071/?token=itAcKdeCyHzxLpkJMmBDazlEdlIyQvwo&type=prod/logistics/binning"
    SUMO_LOGGING_URI = "https://collectors.de.sumologic.com/receiver/v1/http/ZaVnC4dhaV197bMLJ4vjvvzniIjUSoJlHoe2n-L7vy6RG0Gt2HUxO3ycTA9SNR77vBTg6Sprqn5XDBHBOE3ClC6TCwsojqW_RTGlkPO4YaAXkv1uDv6CFw=="

    LEGACY_API_URI = os.environ.get("LEGACY_API_URI", default="https://api.felfel.ch")