from enum import Enum, Flag


class CdcOptions(Flag):
    PICS_SUBST = 1 << 0
    BLK_ENA = 1 << 1
    # Add d (description) data attribute
    DESC = 1 << 2
    # Add dU (unicode description) data attribute
    DESC_UNICODE = 1 << 3
    # Add cdcNs and cdcName required when a CDC is an extension to the standard
    AC_DLNDA = 1 << 4
    # Add dataNs (data namespace) required for extended CDCs
    AC_DLN = 1 << 5
    # Add the unit data attribute
    UNIT = 1 << 6
    FROZEN_VALUE = 1 << 7
    ADDR = 1 << 8
    ADDINFO = 1 << 9
    INST_MAG = 1 << 10
    RANGE = 1 << 11
    UNIT_MULTIPLIER = 1 << 12
    AC_SCAV = 1 << 13
    MIN = 1 << 14
    MAX = 1 << 15
    AC_CLC_O = 1 << 16
    RANGE_ANG = 1 << 17
    PHASE_A = 1 << 18
    PHASE_B = 1 << 19
    PHASE_C = 1 << 20
    PHASE_NEUT = 1 << 21
    PHASES_ABC = PHASE_A | PHASE_B | PHASE_C
    PHASES_ALL = PHASE_A | PHASE_B | PHASE_C | PHASE_NEUT
    STEP_SIZE = 1 << 22
    ANGLE_REF = 1 << 23


def extra_cdc_options(*allowed: CdcOptions):
    """Indicate valid CdcOption in addition to the standard options"""

    def decorator(func):
        standard_options = (
            CdcOptions.DESC | CdcOptions.DESC_UNICODE | CdcOptions.AC_DLNDA | CdcOptions.AC_DLN
        )
        func._valid_options = standard_options
        for opt in allowed:
            func._valid_options |= opt
        return func

    return decorator


# # Options that are only valid for DPL CDC
# # DPL_HWREV = 1 << 17)
# # DPL_SWREV = 1 << 18)
# # DPL_SERNUM = 1 << 19)
# # DPL_MODEL = 1 << 20)
# # DPL_LOCATION = 1 << 21)

# # Add mandatory data attributes for LLN0 (e.g. LBL configRef)
# # AC_LN0_M = 1 << 24)
# # AC_LN0_EX = 1 << 25)
# # AC_DLD_M = 1 << 26)


class CdcControlModelOptions(Flag):
    MODEL_NONE = 0
    MODEL_DIRECT_NORMAL = 1
    MODEL_SBO_NORMAL = 2
    MODEL_DIRECT_ENHANCED = 3
    MODEL_SBO_ENHANCED = 4

    MODEL_HAS_CANCEL = 1 << 4
    MODEL_IS_TIME_ACTIVATED = 1 << 5

    OPTION_ORIGIN = 1 << 6
    OPTION_CTL_NUM = 1 << 7
    OPTION_ST_SELD = 1 << 8
    OPTION_OP_RCVD = 1 << 9
    OPTION_OP_OK = 1 << 10
    OPTION_T_OP_OK = 1 << 11
    OPTION_SBO_TIMEOUT = 1 << 12
    OPTION_SBO_CLASS = 1 << 13
    OPTION_OPER_TIMEOUT = 1 << 14


# # Minimum measured value
# # CDC_OPTION_61400_MIN_MX_VAL = 1 << 10)

# # Maximum measured value
# # CDC_OPTION_61400_MAX_MX_VAL = 1 << 11)

# # Total average value of data
# # CDC_OPTION_61400_TOT_AV_VAL = 1 << 12)

# # Standard deviation of data
# # CDC_OPTION_61400_SDV_VAL = 1 << 13)

# # Rate of increase
# # CDC_OPTION_61400_INC_RATE = 1 << 14)

# # Rate of decrease
# # CDC_OPTION_61400_DEC_RATE = 1 << 15)

# # Setpoint or parameter access level (low/medium/high)
# # CDC_OPTION_61400_SP_ACS = 1 << 16)

# # Time periodical reset (hourly/daily/weekly/monthly)
# # CDC_OPTION_61400_CHA_PER_RS = 1 << 17)

# # Command access level
# # CDC_OPTION_61400_CM_ACS = 1 << 18)

# # Total time duration of a state
# # CDC_OPTION_61400_TM_TOT = 1 << 19)

# # Daily counting data
# # CDC_OPTION_61400_COUNTING_DAILY = 1 << 20)

# # Monthly counting data
# # CDC_OPTION_61400_COUNTING_MONTHLY = 1 << 21)

# # Yearly counting data
# # CDC_OPTION_61400_COUNTING_YEARLY = 1 << 22)

# # Total counting data
# # CDC_OPTION_61400_COUNTING_TOTAL = 1 << 23)

# # All counting data
# # CDC_OPTION_61400_COUNTING_ALL (CDC_OPTION_61400_COUNTING_DAILY | CDC_OPTION_61400_COUNTING_MONTHLY | CDC_OPTION_61400_COUNTING_YEARLY | CDC_OPTION_61400_COUNTING_TOTAL)
