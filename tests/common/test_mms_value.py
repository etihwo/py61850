from py61850.common import MmsType, MmsValue


def test_bool():
    val = MmsValue.new_bool(True)
    assert val.get_type() == MmsType.BOOLEAN
    assert val.to_bool() is True
    val.set_bool(False)
    assert val.get_type() == MmsType.BOOLEAN
    assert val.to_bool() is False


def test_float():
    val = MmsValue.new_float(1.25)
    assert val.get_type() == MmsType.FLOAT
    assert val.to_float() == 1.25
    val.set_float(2.5)
    assert val.get_type() == MmsType.FLOAT
    assert val.to_float() == 2.5


def test_double():
    val = MmsValue.new_float(1.25)
    assert val.get_type() == MmsType.FLOAT
    assert val.to_double() == 1.25
    val.set_double(2.5)
    assert val.get_type() == MmsType.FLOAT
    assert val.to_double() == 2.5


def test_int8():
    val = MmsValue.new_int8(-10)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == -10
    val.set_int8(20)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == 20


def test_int16():
    val = MmsValue.new_int32(-10)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == -10
    val.set_int16(20)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == 20


def test_int32():
    val = MmsValue.new_int32(-10)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == -10
    val.set_int32(20)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int32() == 20


def test_int64():
    val = MmsValue.new_int64(10)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int64() == 10
    val.set_int64(20)
    assert val.get_type() == MmsType.INTEGER
    assert val.to_int64() == 20


def test_uint32():
    val = MmsValue.new_uint32(10)
    assert val.get_type() == MmsType.UNSIGNED
    assert val.to_uint32() == 10
    val.set_uint32(20)
    assert val.get_type() == MmsType.UNSIGNED
    assert val.to_uint32() == 20
