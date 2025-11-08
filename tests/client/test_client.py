from unittest.mock import Mock

import pytest

from py61850.client import (
    IedClientError,
    IedConnection,
    IedConnectionException,
    IedConnectionState,
)
from py61850.common import ACSIClass, FunctionalConstraint
from py61850.server import IedServer


def test_connect(ied_server_model_port: tuple[IedServer, int]):
    """Test the connect close command with state change"""
    on_state_change = Mock()
    on_closed = Mock()
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.on_connection_state_change(on_state_change)
    ied_connection.on_connection_closed(on_closed)
    assert ied_connection.status == IedConnectionState.CLOSED
    ied_connection.connect("127.0.0.1", port)
    assert ied_connection.status == IedConnectionState.CONNECTED
    on_state_change.assert_called_with(ied_connection, IedConnectionState.CONNECTED)
    ied_connection.close()
    assert ied_connection.status == IedConnectionState.CLOSED
    on_state_change.assert_called_with(ied_connection, IedConnectionState.CLOSED)
    on_closed.assert_called_once_with(ied_connection)


def test_connection_error():
    ied_connection = IedConnection()
    ied_connection.set_connect_timeout(100)
    with pytest.raises(IedConnectionException) as excinfo:
        ied_connection.connect("127.0.0.1", 102)
    assert excinfo.value.error_code == IedClientError.CONNECTION_REJECTED


def test_get_logical_devices(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_logical_devices function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    logical_devices = ied_connection.get_logical_devices()
    assert len(logical_devices) == 1
    assert b"simpleIOGenericIO" in logical_devices
    ied_connection.close()


def test_get_logical_nodes(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_logical_devices function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    logical_nodes = ied_connection.get_logical_nodes(b"simpleIOGenericIO")
    assert len(logical_nodes) == 3
    assert b"LLN0" in logical_nodes
    assert b"LPHD1" in logical_nodes
    assert b"GGIO1" in logical_nodes
    ied_connection.close()


def test_get_logical_node_directory(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_logical_node_directory function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    data_objects = ied_connection.get_logical_node_directory(
        b"simpleIOGenericIO/LLN0", ACSIClass.DATA_OBJECT
    )
    assert len(data_objects) == 4
    assert b"Mod" in data_objects
    assert b"Beh" in data_objects
    assert b"Health" in data_objects
    assert b"NamPlt" in data_objects

    datasets = ied_connection.get_logical_node_directory(
        b"simpleIOGenericIO/LLN0", ACSIClass.DATA_SET
    )
    assert len(datasets) == 1
    assert b"ControlEvents" in datasets

    brcbs = ied_connection.get_logical_node_directory(b"simpleIOGenericIO/LLN0", ACSIClass.BRCB)
    assert len(brcbs) == 0

    urcbs = ied_connection.get_logical_node_directory(b"simpleIOGenericIO/LLN0", ACSIClass.URCB)
    assert len(urcbs) == 2
    assert b"ControlEventsRCB01" in urcbs
    assert b"ControlEventsRCB02" in urcbs
    ied_connection.close()


def test_get_data_directory(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_data_directory function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    data_attributes = ied_connection.get_data_directory(b"simpleIOGenericIO/LLN0.Mod")
    assert len(data_attributes) == 3
    assert b"q" in data_attributes
    assert b"t" in data_attributes
    assert b"ctlModel" in data_attributes

    ied_connection.close()


def test_get_data_directory_fc(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_data_directory function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    data_attributes = ied_connection.get_data_directory_fc(b"simpleIOGenericIO/LLN0.Mod")
    assert len(data_attributes) == 3
    assert b"q[ST]" in data_attributes
    assert b"t[ST]" in data_attributes
    assert b"ctlModel[CF]" in data_attributes

    ied_connection.close()


def test_get_data_directory_by_fc(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_data_directory_by_fc function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    data_attributes = ied_connection.get_data_directory_by_fc(
        b"simpleIOGenericIO/LLN0.Mod", FunctionalConstraint.ST
    )
    assert len(data_attributes) == 2
    assert b"q" in data_attributes
    assert b"t" in data_attributes

    data_attributes = ied_connection.get_data_directory_by_fc(
        b"simpleIOGenericIO/LLN0.Mod", FunctionalConstraint.CF
    )
    assert len(data_attributes) == 1
    assert b"ctlModel" in data_attributes

    ied_connection.close()


def test_get_dataset_directory(ied_server_model_port: tuple[IedServer, int]):
    """Use the ied server from the model.cfg and test the get_dataset_directory function"""
    ied_server, port = ied_server_model_port
    ied_connection = IedConnection()
    ied_connection.connect("127.0.0.1", port)

    dataset_entries = ied_connection.get_dataset_directory(b"simpleIOGenericIO/LLN0.ControlEvents")
    assert len(dataset_entries) == 12
    assert b"simpleIOGenericIO/GGIO1.SPCSO1.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO2.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO3.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO4.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO5.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO6.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO7.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO8.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO9.stVal[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO2.stSeld[ST]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO2.opRcvd[OR]" in dataset_entries
    assert b"simpleIOGenericIO/GGIO1.SPCSO2.opOk[OR]" in dataset_entries
    ied_connection.close()
