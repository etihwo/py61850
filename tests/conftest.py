"""
A module containing testing utilities and fixtures.
"""

import pytest

from py61850.server import IedModel, IedServer


@pytest.fixture(scope="session")
def ied_server_model_port():
    """Create and start a server from the model.cfg configuration"""
    ied_model = IedModel.create_from_config_file(b"./model.cfg")
    ied_server = IedServer(ied_model)
    port = 5000
    ied_server.start(port)
    yield ied_server, port
    ied_server.stop()
