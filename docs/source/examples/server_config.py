# ---
# jupyter:
#   jupytext_format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Server simple

# Create the model from a configuration file

import datetime
import os
import time

from py61850.server import ClientConnection, IedModel, IedServer, IedServerConfig


def on_connection_change(client: ClientConnection, connected: bool):
    """Callback used when the connection status to the serve change.

    Parameters
    ----------
    client : ClientConnection
        Client at the origin of the change
    connected : bool
        Indicate whether the new state is connected or disconnected
    """
    if connected:
        print(f"Client {client.local_address()} is connected to {client.peer_address()}.")
    else:
        print(f"Client {client.local_address()} is disconnected.")


current_file_directory = os.path.dirname(os.path.realpath(__file__))
iedModel = IedModel.create_from_config_file(os.path.join(current_file_directory, "model.cfg"))
iedModel.name = "TestIED"

# spcso1: DataObject = iedModel.model_node_by_short_reference("GenericIO/GGIO1.SPCSO1")
anin1 = iedModel.model_node_by_short_reference("GenericIO/GGIO1.AnIn1")
temperatureValue = anin1.child("mag.f")  # type:ignore
temperatureTimestamp = anin1.child("t")  # type:ignore

config = IedServerConfig()

ied_server = IedServer(iedModel, config)


ied_server.register_connection_change(on_connection_change)

print("start")
ied_server.start(102)
val = 0.0

while True:
    time.sleep(2)
    ied_server.lock_data_model()
    ied_server.update_utc_time(
        temperatureTimestamp,  # type:ignore
        datetime.datetime.now().astimezone(),
    )
    ied_server.update_float(temperatureValue, val)  # type:ignore
    ied_server.unlock_data_model()
    val += 0.1
