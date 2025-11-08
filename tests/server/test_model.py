import pytest

from py61850.common import (
    CdcControlModelOptions,
    CdcOptions,
    ReportOptions,
    ReportTriggerOptions,
)
from py61850.server import DataObject, IedModel, LogicalNode, ModelNodeType


def test_create_model_from_config_file_invalid():
    """Test the ``create_model_from_config_file`` function with an invalid filename."""
    with pytest.raises(RuntimeError):
        IedModel.create_from_config_file(b"./invalid.cfg")


def test_create_model_from_config_file():
    """Test the ``create_model_from_config_file`` function."""

    ied = IedModel.create_from_config_file(b"./model.cfg")

    ld = ied.logical_device_by_instance("GenericIO")
    assert ld is not None
    assert ld.model_type == ModelNodeType.LOGICAL_DEVICE
    assert ld.name == b"GenericIO"


def test_model_creation():
    ied = IedModel("testmodel")
    ld = ied.create_logical_device("ld0")
    lln0 = ld.create_logical_node("LLN0")
    lln0_mod = lln0.create_cdc_ens("Mod")
    lln0_health = lln0.create_cdc_ens("Health")

    lln0.create_setting_group_control_block(1, 1)

    # Add a temperature sensor LN
    ttmp1 = ld.create_logical_node("TTMP1")
    ttmp1_tmpsv = ttmp1.create_cdc_sav("TmpSv", False)

    temperatureValue = ttmp1_tmpsv.child("instMag.f")
    temperatureTimestamp = ttmp1_tmpsv.child("t")

    ggio1 = ld.create_logical_node("GGIO1")
    ggio1_anIn1 = ggio1.create_cdc_apc(
        "AnOut1",
        False,
        CdcOptions(0),
        CdcControlModelOptions.MODEL_HAS_CANCEL | CdcControlModelOptions.MODEL_SBO_ENHANCED,
    )

    dataset = lln0.create_dataset("events")
    dataset.create_dataset_entry("TTMP1$MX$TmpSv$instMag$f")

    rpt_options = (
        ReportOptions.SEQ_NUM | ReportOptions.TIME_STAMP | ReportOptions.REASON_FOR_INCLUSION
    )

    lln0.create_report_control_block(
        "events01",
        "events01",
        False,
        None,
        1,
        ReportTriggerOptions.DATA_CHANGED,
        rpt_options,
        50,
        0,
    )
    lln0.create_report_control_block(
        "events02",
        "events02",
        False,
        None,
        1,
        ReportTriggerOptions.DATA_CHANGED,
        rpt_options,
        50,
        0,
    )

    lln0.create_goose_control_block("gse01", "events01", "events", 1, 200, 3000)

    assert ied.name == b"testmodel"

    ld1 = ied.logical_device_by_instance("ld0")
    assert ld1 is not None
    assert ld1.model_type == ModelNodeType.LOGICAL_DEVICE
    assert ld1.name == b"ld0"

    lln01 = ied.model_node_by_reference("testmodelld0/LLN0")
    assert lln01 is not None
    assert isinstance(lln01, LogicalNode)

    lln0_mod1 = ied.model_node_by_reference("testmodelld0/LLN0.Mod")
    assert lln0_mod1 is not None
    assert isinstance(lln0_mod1, DataObject)

    lln0_health1 = ied.model_node_by_reference("testmodelld0/LLN0.Health")
    assert lln0_health1 is not None
    assert isinstance(lln0_health1, DataObject)
