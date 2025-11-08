# ---
# jupyter:
#   jupytext_format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Client
# This client is configurated to match the {doc}``server_dynamic`` example.

# ## Import
# Import required module for the example.

import time

from py61850.client import (
    ControlObject,
    IedConnection,
    IedConnectionState,
    ReasonForInclusion,
    Report,
)
from py61850.common import (
    ACSIClass,
    ControlModel,
    FunctionalConstraint,
    MmsValue,
    ReportOptions,
    ReportTriggerOptions,
)

# ## Callback
# Create callback for connection status.


def on_connection_state_change(connection: IedConnection, state: IedConnectionState):
    """Callback triggered when the collection state is changed

    Parameters
    ----------
    connection : IedConnection
        _description_
    state : IedConnectionState
        New state
    """
    print(f"Connection status is {state}")


def on_connection_closed(connection: IedConnection):
    """Callback when the connection is closed

    Parameters
    ----------
    connection : IedConnection
        _description_
    """
    print("Connection is closed")


def on_termination(obj: ControlObject):
    print("Action is done")


# Create callback to be triggered when a new report is received


def on_report(rpt: Report):
    """Call back triggered when a new report is received

    Parameters
    ----------
    rpt : Report
        _description_
    """
    print("Report received")
    print(f"    rpt.buf_ovfl: {rpt.buf_ovfl}")
    print(f"    rpt.conf_rev: {rpt.conf_rev}")
    print(f"    rpt.dataset_name: {rpt.dataset_name}")
    print(
        f"    rpt.entry_id: {tmp if (tmp:=rpt.entry_id) is None else ' '.join(format(val, '02x') for val in tmp)}"
    )
    print(f"    rpt.more_seqments_follow: {rpt.more_seqments_follow}")
    print(f"    rpt.rcb_reference: {rpt.rcb_reference}")
    print(f"    rpt.rpt_id: {rpt.rpt_id}")
    print(f"    rpt.seq_num: {rpt.seq_num}")
    print(f"    rpt.sub_seq_num: {rpt.sub_seq_num}")
    print(f"    rpt.timestamp: {rpt.timestamp}")

    print("    content of the report:")
    values = rpt.dataset_values
    for i in range(values.size()):
        if (
            rpt.has_reason_for_inclusion
            and rpt.get_reason_for_inclusion(i) == ReasonForInclusion.NOT_INCLUDED
        ):
            print(f"        item: {i} not included")
            continue

        print(f"        item: {i}")
        if rpt.has_data_reference:
            print(f"            {rpt.get_data_reference(i)}")
        print(f"            {rpt.get_reason_for_inclusion(i)}")
        print(f"            {values.get_element(i)}")


# ## Connection
# Create the connection

ied_connection = IedConnection()
hostname = "127.0.0.1"
port = 102
ied_connection.on_connection_state_change(on_connection_state_change)
ied_connection.on_connection_closed(on_connection_closed)
ied_connection.connect(hostname, port)

# ## Browsing data


# To get the list of logical devices and logical nodes, you can use the following functions:
# - {py:class}``get_logical_devices <py61850.client.IedConnection.get_logical_devices>`` to retrieve the list of all logical devices
# - {py:class}``get_logical_nodes <py61850.client.IedConnection.get_logical_nodes>`` to retrieve the list of logical nodes for a specific logical device


# Read logical devices and logical nodes

logical_devices = ied_connection.get_logical_devices()
for ld in logical_devices:
    print(f"LD: {ld}")
    for ln in ied_connection.get_logical_nodes(ld):
        print(f"  LN: {ln}")

# To get the content of logical nodes, you can use the following functions:
# - {py:class}``get_logical_node_variables <py61850.client.IedConnection.get_logical_node_variables>`` to have all child element of the logical node
# - {py:class}``get_logical_node_directory <py61850.client.IedConnection.get_logical_node_directory>``
# to retrieve only a specific class such {py:class}``DATA_OBJECT <py61850.common.ACSIClass.DATA_OBJECT>``
# or {py:class}``DATA_SET <py61850.common.ACSIClass.DATA_SET>``


# Read all content of a logical node

print("Content of IEDNameLD0/LLN0:")
for obj in ied_connection.get_logical_node_variables("IEDNameLD0/LLN0"):
    print(f"  {obj}")

# Read only some class of a logical node

for obj in ied_connection.get_logical_node_directory("IEDNameLD0/LLN0", ACSIClass.DATA_OBJECT):
    print(f"  DO: {obj}")
for obj in ied_connection.get_logical_node_directory("IEDNameLD0/LLN0", ACSIClass.DATA_SET):
    print(f"  Dataset: {obj}")

# To get the content of datobject or complexe data attribute, you can use the following functions:
# - {py:class}``get_data_directory <py61850.client.IedConnection.get_data_directory>``
# - {py:class}``get_data_directory_fc <py61850.client.IedConnection.get_data_directory_fc>`` to retrieve also the functional constraint
# - {py:class}``get_data_directory_by_fc <py61850.client.IedConnection.get_data_directory_by_fc>`` to read only data attribute with a specific functional constraint

# Read data attribute of a reference

for obj in ied_connection.get_data_directory("IEDNameLD0/LLN0.Mod.Oper.origin"):
    print(f"  {obj}")

# Read data attribute of a reference and include the functionnal constraint in the result

for obj in ied_connection.get_data_directory_fc("IEDNameLD0/LLN0.Mod"):
    print(f"  {obj}")

# Read data attribute with a specific functionnal constraint of a reference

for obj in ied_connection.get_data_directory_by_fc("IEDNameLD0/LLN0.Mod", FunctionalConstraint.ST):
    print(f"  {obj}")

# To read and write values, you can use the following functions:
# - {py:class}``read_boolean <py61850.client.IedConnection.read_boolean>``
# - {py:class}``read_int32 <py61850.client.IedConnection.read_int32>``
# - {py:class}``read_uint32 <py61850.client.IedConnection.read_uint32>``
# - {py:class}``read_int64 <py61850.client.IedConnection.read_int64>``
# - {py:class}``read_float <py61850.client.IedConnection.read_float>``
# - {py:class}``read_string <py61850.client.IedConnection.read_string>``
# - {py:class}``read_timestamp <py61850.client.IedConnection.read_timestamp>``
# - {py:class}``read_quality <py61850.client.IedConnection.read_quality>``
# - {py:class}``read_value <py61850.client.IedConnection.read_value>`` for complexe values
# - {py:class}``write_boolean <py61850.client.IedConnection.write_boolean>``
# - {py:class}``write_int32 <py61850.client.IedConnection.write_int32>``
# - {py:class}``write_uint32 <py61850.client.IedConnection.write_uint32>``
# - {py:class}``write_float <py61850.client.IedConnection.write_float>``
# - {py:class}``write_string <py61850.client.IedConnection.write_string>``
# - {py:class}``write_octet_string <py61850.client.IedConnection.write_octet_string>``
# - {py:class}``write_value <py61850.client.IedConnection.write_value>`` for complexe values

val = ied_connection.read_float("IEDNameLD0/PTOC1.StrVal.setMag.f", FunctionalConstraint.SP)
print(f"Value of IEDNameLD0/PTOC1.StrVal.setMag.f: {val}")
ied_connection.write_float("IEDNameLD0/PTOC1.StrVal.setMag.f", FunctionalConstraint.SP, val + 1.0)
val = ied_connection.read_float("IEDNameLD0/PTOC1.StrVal.setMag.f", FunctionalConstraint.SP)
print(f"Value of IEDNameLD0/PTOC1.StrVal.setMag.f: {val}")


# ## Setting group control block
# There is no specific function for setting group control block. You should use the read and write
# function.

act_sg = ied_connection.read_uint32("IEDNameLD0/LLN0.SGCB.ActSG", FunctionalConstraint.SP)
num_of_sgs = ied_connection.read_uint32("IEDNameLD0/LLN0.SGCB.numOfSGs", FunctionalConstraint.SP)
print(f"Current setting group is {act_sg}/{num_of_sgs}")


# ## Control

# To send control command to the server, you first need to read the control object. Then you can configure it with the following functions:
# - {py:class}``set_test_mode <py61850.client.ControlObject.set_test_mode>``
# - {py:class}``set_origin <py61850.client.ControlObject.set_origin>``
# - {py:class}``set_interlock_check <py61850.client.ControlObject.set_interlock_check>``
# - {py:class}``set_synchro_check <py61850.client.ControlObject.set_synchro_check>``
# - {py:class}``use_constant_t <py61850.client.ControlObject.use_constant_t>``

# When the control mode is {py:class}``DIRECT_ENHANCED <py61850.common.ControlModel.DIRECT_ENHANCED>``
# or {py:class}``SBO_ENHANCED <py61850.common.ControlModel.SBO_ENHANCED>``, you can get the feedback
# when command has been processed.

# Depending on the control mode, you can perform operation with one or 2 of the following functions:
# - {py:class}``select <py61850.client.ControlObject.select>``
# - {py:class}``select_with_value <py61850.client.ControlObject.select_with_value>``
# - {py:class}``operate <py61850.client.ControlObject.operate>``

ctrl = ied_connection.read_control("IEDNameLD0/LLN0.Mod")
ctrl.on_termination(on_termination)  # only used in ENHANCED
control_model = ctrl.control_model
value = 1
if control_model == ControlModel.DIRECT_NORMAL:
    if ctrl.operate(MmsValue.new_int8(value)):
        print("Operate command succeed")
    else:
        error = ctrl.get_last_appl_error()
        print(f"Operate command fail {error.add_cause}")
elif control_model == ControlModel.DIRECT_ENHANCED:
    if ctrl.operate(MmsValue.new_int8(value)):
        print("Operate command succeed")
    else:
        error = ctrl.get_last_appl_error()
        print(f"Operate command fail {error.add_cause}")
elif control_model == ControlModel.SBO_NORMAL:
    if ctrl.select():
        print("Select command succeed")
    else:
        print("Select command fail")
    if ctrl.operate(MmsValue.new_int8(value)):
        print("Operate command succeed")
    else:
        error = ctrl.get_last_appl_error()
        print(f"Operate command fail {error.add_cause}")
elif control_model == ControlModel.SBO_ENHANCED:
    if ctrl.select_with_value(MmsValue.new_int8(value)):
        print("Select command succeed")
    else:
        print("Select command fail")
    if ctrl.operate(MmsValue.new_int8(value)):
        print("Operate command succeed")
    else:
        error = ctrl.get_last_appl_error()
        print(f"Operate command fail {error.add_cause}")


# ## Dataset

dataset = ied_connection.read_dataset("IEDNameLD0/LLN0.DsRpt")
print(ied_connection.get_dataset_directory(dataset.reference))
print(dataset.values)

# ## Report control block
# Create a report control block and subscribe it.

urcba = ied_connection.read_rcb("IEDNameLD0/LLN0.RP.URCBA")
urcba.on_report(on_report)
urcba.subscribe(
    trg_ops=ReportTriggerOptions.INTEGRITY,
    intg_pd=5000,
)

brcba = ied_connection.read_rcb("IEDNameLD0/LLN0.BR.BRCBA")
brcba.on_report(on_report)
brcba.subscribe(
    trg_ops=ReportTriggerOptions.DATA_CHANGED,  # | ReportTriggerOptions.INTEGRITY,
    intg_pd=5000,
    opt_flds=ReportOptions.ENTRY_ID
    | ReportOptions.TIME_STAMP
    | ReportOptions.REASON_FOR_INCLUSION,
)
print(brcba.dataset_reference)


# ## Files
# To manage file on the ied server, you can use the following functions:
# - {py:class}``get_files <py61850.client.IedConnection.get_files>``
# - {py:class}``download_file <py61850.client.IedConnection.download_file>``
# - {py:class}``delete_file <py61850.client.IedConnection.delete_file>``
# - {py:class}``upload_file <py61850.client.IedConnection.upload_file>``

files = ied_connection.get_files()
for file in files:
    print(file.filename)
    break

content = ied_connection.download_file(b"dummy.txt")
print(content.decode("utf-8"))

# Just wait or perform an infinite loop to received report

time.sleep(20)


ied_connection.close()


# This notebook can be downloaded as {download}`client_simple.py`
