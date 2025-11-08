# ---
# jupyter:
#   jupytext_format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Dynamic server
# ## Import
# Import required module for the example.

import os
import time

from py61850.common import CdcControlModelOptions, MmsDataAccessError, MmsValue
from py61850.server import (
    CheckHandlerResult,
    ClientConnection,
    ControlAction,
    ControlHandlerResult,
    DataAttribute,
    DataObject,
    IedModel,
    IedServer,
    SelectStateChangedReason,
    SettingGroupControlBlock,
)

# ## Callback


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


def on_active_setting_group_change(
    sgcb: SettingGroupControlBlock,
    client: ClientConnection,
    val: int,
) -> bool:
    """Callback when the active setting group is changed

    Parameters
    ----------
    sgcb : SettingGroupControlBlock
        Setting group control block where the setting group is changed
    client : ClientConnection
        Client which trigger the change
    val : int
        New setting group

    Returns
    -------
    bool
        True to indicate the server can perform the chnage False to reject
        the change.
    """
    print(
        f"Client {client.local_address()} change active setting group from {sgcb.act_sg} to {val}."
    )
    return True


def on_edit_setting_group_change(
    sgcb: SettingGroupControlBlock,
    client: ClientConnection,
    val: int,
) -> bool:
    """Callback when the edit setting group is changed

    Parameters
    ----------
    sgcb : SettingGroupControlBlock
        Setting group control block where the setting group is changed
    client : ClientConnection
        Client which trigger the change
    val : int
        New setting group

    Returns
    -------
    bool
        True to indicate the server can perform the chnage False to reject
        the change.
    """
    print(
        f"Client {client.local_address()} change edit setting group from {sgcb.edit_sg} to {val}."
    )
    return True


def on_edit_setting_group_confirmed(
    sgcb: SettingGroupControlBlock,
    val: int,
):
    """Callback when the client trigger the CnfEdit of the setting group control block

    Parameters
    ----------
    sgcb : SettingGroupControlBlock
        Setting group control block where the edit setting group is confirmed
    val : int
        Value of the edit setting group

    Returns
    -------
    _type_
        _description_
    """
    print(f"CnfEdit has been changed and confirmed edit group is {val}")


def on_static(
    data_object: DataObject,
    action: ControlAction,
    ctl_value: MmsValue,
    test: bool,
    interlockCheck: bool,
) -> CheckHandlerResult:
    # Call by select and operate
    print("on_static")
    return CheckHandlerResult.ACCEPTED


def on_dynamic(
    data_object: DataObject,
    action: ControlAction,
    ctl_value: MmsValue,
    test: bool,
    sychroCheck: bool,
) -> ControlHandlerResult:
    # called only by operate
    # optional callback
    print("on_dynamic")
    return ControlHandlerResult.OK


def on_control_select_state_change(
    data_object: DataObject,
    action: ControlAction,
    test: bool,
    reason: SelectStateChangedReason,
):
    print(f"Select state changed for {data_object.name} due to {reason}")
    print(f"    client: {action.get_client_connection().local_address()}")
    print(f"    Interlock flag is {'on' if action.get_interlock_check() else 'off'}")
    print(f"    Synchrocheck flag is {'on' if action.get_synchro_check() else 'off'}")
    print(f"    test flag is {'on' if test else 'off'}")
    print(f"    Command received at {action.getT().get_time()}")
    print(f"    Originator identifier is {action.get_originator_identifier()}")
    print(f"    Originator category is {action.get_originator_category()}")
    print(action.get_control_time())  # Not working ?


def on_control_operate(
    data_object: DataObject,
    action: ControlAction,
    ctl_value: MmsValue,
    test: bool,
) -> ControlHandlerResult:
    print(f"Received control command for {data_object.name}")
    print(f"    New value is {ctl_value.get_value()}")
    print(f"    client: {action.get_client_connection().local_address()}")
    print(f"    Interlock flag is {'on' if action.get_interlock_check() else 'off'}")
    print(f"    Synchrocheck flag is {'on' if action.get_synchro_check() else 'off'}")
    print(f"    test flag is {'on' if test else 'off'}")
    print(f"    Command received at {action.getT().get_time()}")
    print(f"    Originator identifier is {action.get_originator_identifier()}")
    print(f"    Originator category is {action.get_originator_category()}")
    # print(action.get_control_time())  # Not working ?

    if data_object.name == b"Mod":
        ied_server.update_utc_time(data_object.child("t"))
        ied_server.update_int32(data_object.child("stVal"), ctl_value.get_value())

    return ControlHandlerResult.OK


def on_write(
    client: ClientConnection,
    data_attribute: DataAttribute,
    value: MmsValue,
) -> MmsDataAccessError:
    print(f"Received write command for {data_attribute.name}")
    print(f"    client: {client.local_address()}")
    return MmsDataAccessError.SUCCESS


# ## Model creation
#
# Create a Iedmodel by using the create_logical_device, create_logical_node... functions
# First create the model itself

ied_model = IedModel("IEDName")

# Add logical device to the model

ld0 = ied_model.create_logical_device("LD0")

# Add some logical nodes in logical devices

ld0_lln0 = ld0.create_logical_node("LLN0")
ld0_lphd1 = ld0.create_logical_node("LPHD1")
ld0_ptoc1 = ld0.create_logical_node("PTOC1")

# Add some data object in logical nodes

ld0_lln0_mod = ld0_lln0.create_cdc_inc(
    "Mod",
    control_options=CdcControlModelOptions.MODEL_SBO_ENHANCED,
)
ld0_lln0_beh = ld0_lln0.create_cdc_ins("Beh")
ld0_lln0_health = ld0_lln0.create_cdc_ins("Health")

ld0_ptoc1_beh = ld0_ptoc1.create_cdc_ens("Beh")
ld0_ptoc1_str = ld0_ptoc1.create_cdc_acd("Str")
ld0_ptoc1_op = ld0_ptoc1.create_cdc_act("Op")
ld0_ptoc1_strval = ld0_ptoc1.create_cdc_asg("StrVal", False)
ld0_ptoc1_ppdltmms = ld0_ptoc1.create_cdc_ing("OpDlTmms")


# ## Setting group control block
# Create a setting group control block in the LLN0 logcial node

ld0_sgcb = ld0_lln0.create_setting_group_control_block(1, 4)


# ## Dataset
# Create dataset

dataset = ld0_lln0.create_dataset("DsRpt")
dataset.create_dataset_entry("PTOC1$ST$Str")
dataset.create_dataset_entry("PTOC1$ST$Op")


# ## Report control block
# Create report control block

urcba = ld0_lln0.create_report_control_block("URCBA", "URCBA01", False, dataset.name)
brcba = ld0_lln0.create_report_control_block("BRCBA", "BRCBA01", True, dataset.name)


# Retrieve attribute for further operation

ld0_lln0_mod_t: DataAttribute = ld0_lln0_mod.child("t")  # type:ignore
ld0_ptoc1_str_t: DataAttribute = ld0_ptoc1_str.child("t")  # type:ignore
ld0_ptoc1_str_general: DataAttribute = ld0_ptoc1_str.child("general")  # type:ignore
ld0_ptoc1_ppdltmms_setval: DataAttribute = ld0_ptoc1_ppdltmms.child("setVal")  # type:ignore

# Initialise some value before creating the server

ld0_lln0_mod_t.init_value(MmsValue.new_utc_time())

# Create the server from the model

ied_server = IedServer(ied_model)

# Register callback for connection status change (connection/disconnection)

ied_server.register_connection_change(on_connection_change)

# Register callback for setting group

ied_server.register_active_setting_group_change_handler(ld0_sgcb, on_active_setting_group_change)
ied_server.register_edit_setting_group_change_handler(ld0_sgcb, on_edit_setting_group_change)
ied_server.register_edit_setting_group_confirmed_handler(ld0_sgcb, on_edit_setting_group_confirmed)

# Register control callback

ied_server.register_control_handler(ld0_lln0_mod, on_control_operate)  # Mandatory
ied_server.register_control_select_state_handler(ld0_lln0_mod, on_control_select_state_change)
ied_server.register_control_static_check_handler(ld0_lln0_mod, on_static)  # Optional
ied_server.register_control_wait_handler(ld0_lln0_mod, on_dynamic)  # Optional

# Register write handler for a specific data attribute

ied_server.register_write_handler(ld0_ptoc1_ppdltmms_setval, on_write)

# Set the base path for the file service
current_file_directory = os.path.dirname(os.path.realpath(__file__))
ied_server.set_filestore_basepath(os.path.join(current_file_directory, "file-store", ""))

# Start the server

ied_server.start(102)

# While loop to never terminate

while True:
    time.sleep(10)
    ied_server.lock_data_model()
    ied_server.update_utc_time(ld0_ptoc1_str_t)
    ied_server.update_boolean(
        ld0_ptoc1_str_general, not ied_server.get_boolean(ld0_ptoc1_str_general)
    )
    ied_server.unlock_data_model()


# This notebook can be downloaded as {download}`server_dynamic.py`
