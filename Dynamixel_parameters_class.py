class DynamixelParameters(object):
    Port = "COM6"
    DXL1_ID = 1  # Shoulder
    DXL2_ID = 2  # Elbow
    BAUDRATE = 3000000



class DynamixelControlTable(object):
    ADDR_MX_TORQUE_ENABLE = 64
    ADDR_MX_OPERATING_MODE = 11
    ADDR_MX_GOAL_POSITION = 116
    ADDR_MX_GOAL_CURRENT = 102
    ADDR_MX_GOAL_VELOCITY = 104
    ADDR_MX_PRESENT_POSITION = 132

    #Dynamixel Mode Values (position, velocity, torque)
    POSITION = 3
    VELOCITY = 1
    TORQUE = 0

    #Position Mode gains
    ADDR_MX_POSITION_P_GAIN = 84
    ADDR_MX_POSITION_I_GAIN = 82
    ADDR_MX_POSITION_D_GAIN = 80

    # Velocity Mode gains
    ADDR_MX_VELOCITY_P_GAIN = 78
    ADDR_MX_VELOCITY_I_GAIN = 76

    #Limits
    ADDR_MX_POSITION_UPPER_LIMIT = 48
    ADDR_MX_POSITION_LOWER_LIMIT = 52
    ADDR_MX_VELOCITY_LIMIT = 44
    ADDR_MX_TORQUE_LIMIT = 38

    #Data Byte Length
    LEN_MX_GOAL_CURRENT = 2
    LEN_MX_GOAL_POSITION = 4
    LEN_MX_GOAL_VELOCITY = 4
    LEN_MX_PRESENT_POSITION = 2
    LEN_MX_POSITION_LIMIT = 4
    LEN_MX_VELOCITY_LIMIT = 4
    LEN_MX_TORQUE_LIMIT = 2

    #Protocol version
    PROTOCOL_VERSION = 2.0

    TORQUE_ENABLE = 1  # Value for enabling the torque
    TORQUE_DISABLE = 0  # Value for disabling the torque

    COMM_SUCCESS = 0  # Communication Success result value
    COMM_TX_FAIL = -1001  # Communication Tx Failed

    dxl_addparam_result = False  # AddParam result
    dxl_getdata_result = False  # GetParam result
    dxl1_present_position = 0  # Present position
    dxl2_led_value_read = 0
