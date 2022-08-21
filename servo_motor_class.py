import ctypes

import dynamixel_sdk
import numpy as np
import user_variables
from Dynamixel_parameters_class import *
from dynamixel_sdk import *
from user_variables import *
from record_data_class import *

class initialise_Dynamixel(object):
    def __init__(self):
        self.portHandler = self.initialisePortHandler()
        self.packetHandler = self.initialisePacketHandler()
        self.open_port()
        return None

    def initialisePortHandler(self):
        self.portHandler = PortHandler(DynamixelParameters.Port)  # Initialize PortHandler Structs
        return self.portHandler

    def initialisePacketHandler(self):
        self.packetHandler = PacketHandler(DynamixelControlTable.PROTOCOL_VERSION)
        return self.packetHandler

    def initialise_bulk_read(self):
        self.groupread_num = GroupBulkRead(self.portHandler, self.packetHandler)
        return self.groupread_num

    def initialise_bulk_write(self):
        self.groupwrite_num = GroupBulkWrite(self.portHandler, self.packetHandler)
        return self.groupwrite_num

    def open_port(self):
        # Open the serial port
        if self.portHandler.openPort():
            print("Port Opened!")
        else:
            quit("Failed to open the port!")

        if self.portHandler.setBaudRate(DynamixelParameters.BAUDRATE):
            print("Baudrate changed to " + str(DynamixelParameters.BAUDRATE) + " Bit/s.")
        else:
            quit("Failed to change the baudrate!")
        return None

    def close_port(self):
        self.portHandler.closePort()
        print("Port Closed!")
        return None



class motor(object):
    def __init__(self, portHandler, packetHandler, groupread_num, groupwrite_num, identity):
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        self.identity = identity
        self.ID = None
        self.groupread_num = groupread_num
        self.groupwrite_num = groupwrite_num


        if identity == "Elbow":
            self.ID = DynamixelParameters.DXL2_ID
        elif identity == "Shoulder":
            self.ID = DynamixelParameters.DXL1_ID
        else:
            quit("Error. Unknown motor Identity.")

        self.record_data = RecordMotorData()

        return None


    def reboot_motor(self):
        self.packetHandler.reboot(self.portHandler, self.ID)
        print(str(self.identity), " motor rebooted!")

    def set_mode(self):
        if UserVariables.motor_method == "position":
            mode = DynamixelControlTable.POSITION
        elif UserVariables.motor_method == "velocity":
            mode = DynamixelControlTable.VELOCITY
        elif UserVariables.motor_method == "torque":
            mode = DynamixelControlTable.TORQUE

        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_OPERATING_MODE, mode)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")
        else:
            print(self.identity + " motor set to " + str(UserVariables.motor_method) + " mode.")

        time.sleep(0.1)
        if UserVariables.motor_method == "position": #setting the motor gains by calling the function
            self.set_motor_gains_position()
            self.set_position_limit()
        elif UserVariables.motor_method == "velocity":
            self.set_motor_gains_velocity()
            self.set_velocity_limit()

        return None

    def set_motor_gains_position(self):
        if self.identity == "Shoulder":
            list = [UserVariables.Kp_position_shoulder,UserVariables.Ki_position_shoulder,UserVariables.Kd_position_shoulder]
            list_addresses = [DynamixelControlTable.ADDR_MX_POSITION_P_GAIN,DynamixelControlTable.ADDR_MX_POSITION_I_GAIN,DynamixelControlTable.ADDR_MX_POSITION_D_GAIN]
        elif self.identity == "Elbow":
            list = [UserVariables.Kp_position_elbow, UserVariables.Ki_position_elbow, UserVariables.Kd_position_elbow]
            list_addresses = [DynamixelControlTable.ADDR_MX_POSITION_P_GAIN, DynamixelControlTable.ADDR_MX_POSITION_I_GAIN, DynamixelControlTable.ADDR_MX_POSITION_D_GAIN]

        for i in range(3):
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, int(list_addresses[i]), int(list[i]))
            if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                quit(self.identity + " motor may be disconnected.")
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                quit(self.identity + " motor may be disconnected.")

        print(self.identity + " motor gains set.")

    def set_motor_gains_velocity(self):
        if self.identity == "Shoulder":
            list = [UserVariables.Kp_velocity_shoulder,UserVariables.Ki_velocity_shoulder]
            list_addresses = [DynamixelControlTable.ADDR_MX_VELOCITY_P_GAIN,DynamixelControlTable.ADDR_MX_VELOCITY_I_GAIN]
        elif self.identity == "Elbow":
            list = [UserVariables.Kp_velocity_elbow,UserVariables.Ki_velocity_elbow]
            list_addresses = [DynamixelControlTable.ADDR_MX_VELOCITY_P_GAIN, DynamixelControlTable.ADDR_MX_VELOCITY_I_GAIN]

        for i in range(2):
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, int(list_addresses[i]), int(list[i]))
            if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                quit(self.identity + " motor may be disconnected.")
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                quit(self.identity + " motor may be disconnected.")

        print(self.identity + " motor gains set.")

    def set_position_limit(self):
        if self.identity == "Shoulder":
            lower = UserVariables.elbow_position_min
            upper = UserVariables.elbow_position_max
        elif self.identity == "Elbow":
            lower = UserVariables.shoulder_position_min
            upper = UserVariables.shoulder_position_max

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_POSITION_LOWER_LIMIT, lower)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_POSITION_UPPER_LIMIT, upper)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")
        print(self.identity + " motor position limits set.")

    def set_velocity_limit(self):
        if self.identity == "Shoulder":
            limit = UserVariables.elbow_velocity_lim
        elif self.identity == "Elbow":
            limit = UserVariables.shoulder_velocity_lim

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_VELOCITY_LIMIT, limit)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")
        print(self.identity + " motor velocity limit set.")


    def enable_motor(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_TORQUE_ENABLE, DynamixelControlTable.TORQUE_ENABLE)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")
        else:
            print(self.identity + " motor enabled.")
        return None

    def disable_motor(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, DynamixelControlTable.ADDR_MX_TORQUE_ENABLE, DynamixelControlTable.TORQUE_DISABLE)
        if dxl_comm_result != DynamixelControlTable.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit(self.identity + " motor may be disconnected.")
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit(self.identity + " motor may be disconnected.")
        else:
            print(self.identity + " motor disabled.")
        return None

    def add_read_param(self): #Update and write new
        #Add parameter storage
        dxl_addparam_result = self.groupread_num.addParam(self.ID, DynamixelControlTable.ADDR_MX_PRESENT_POSITION, DynamixelControlTable.LEN_MX_PRESENT_POSITION)
        if dxl_addparam_result != 1:
            print(str(self.identity) + " groupBulkRead addparam failed")
        return None

    def add_write_param_torque(self, current): #Update and write new
        if current < 0:
            current = current + 65536#add 65536 for the correct datapacket

        data = "{0:#0{1}x}".format(current,6) #Make the Hex string the correct length by prefixing zeros for a total length of 4 bits, plus '0x'.
        #print(data)
        #Get bytes and determine the position, for little endian.
        high_byte_int = int(data[2:4], base=16)
        low_byte_int = int(data[4:], base=16)

        if high_byte_int >= low_byte_int:   #determine position of bytes (little endian)
            data = [low_byte_int, high_byte_int]
        elif high_byte_int < low_byte_int:
            data = [low_byte_int, high_byte_int]

        #print("Low: ", low_byte_hex, "\tint:", low_byte_int)
        #print("High: ",high_byte_hex, "\tint: ", high_byte_int)

        #Send byte data to groupwrite_num object.

        if UserVariables.motor_method == "torque":
            dxl_addparam_result = self.groupwrite_num.addParam(self.ID, DynamixelControlTable.ADDR_MX_GOAL_CURRENT,DynamixelControlTable.LEN_MX_GOAL_CURRENT, data)
        elif UserVariables.motor_method == "position":
            dxl_addparam_result = self.groupwrite_num.addParam(self.ID, DynamixelControlTable.ADDR_MX_GOAL_POSITION,DynamixelControlTable.LEN_MX_GOAL_POSITION, data)


        if dxl_addparam_result != 1:
            print(str(self.identity) + " groupBulkWrite addparam failed")
        return None

    def add_write_param_velocity(self, velocity): #Update and write new
        #velocity = 1023
        if velocity < 0:
            residual = 255
            velocity = 65536 - abs(velocity) #add 65536 for the correct datapacket
        else:
            residual = 0

        data = "{0:#0{1}x}".format(velocity,6) #Make the Hex string the correct length by prefixing zeros for a total length of 4 bits, plus '0x'.

        high_byte_int = int(data[2:4], base=16)
        low_byte_int = int(data[4:], base=16)

        if high_byte_int >= low_byte_int:  # determine position of bytes (little endian)
            data = [low_byte_int, high_byte_int,residual,residual]
        elif high_byte_int < low_byte_int:
            data = [low_byte_int, high_byte_int,residual,residual]
        #print(data)

        #print("Low: ", hex(low_byte_int), "\tint:", low_byte_int)
        #print("High: ",hex(high_byte_int), "\tint: ", high_byte_int)

        #Send byte data to groupwrite_num object
        dxl_addparam_result = self.groupwrite_num.addParam(self.ID, DynamixelControlTable.ADDR_MX_GOAL_VELOCITY,DynamixelControlTable.LEN_MX_GOAL_VELOCITY, data)

        if dxl_addparam_result != 1:
            print(str(self.identity) + " groupBulkWrite addparam failed")
        return None

    def add_write_param_position(self, position): #Update and write new
        # if position < 0:
        #     position = position + 65536#add 65536 for the correct datapacket
        #
        #position = 1500

        data = "{0:#0{1}x}".format(int(position*(4096/360)),6) #Make the Hex string the correct length by prefixing zeros for a total length of 4 bits, plus '0x'.
        #print(data)
        #Get bytes and determine the position, for little endian.
        high_byte_int = int(data[2:4], base=16)
        low_byte_int = int(data[4:], base=16)

        if high_byte_int >= low_byte_int:   #determine position of bytes (little endian)
            data = [low_byte_int, high_byte_int, 0, 0]
        elif high_byte_int < low_byte_int:
            data = [low_byte_int, high_byte_int, 0, 0]
        #print(data)

        #print("Low: ", low_byte_hex, "\tint:", low_byte_int)
        #print("High: ",high_byte_hex, "\tint: ", high_byte_int)

        #Send byte data to groupwrite_num object

        if UserVariables.motor_method == "position":
            dxl_addparam_result = self.groupwrite_num.addParam(self.ID, DynamixelControlTable.ADDR_MX_GOAL_POSITION,DynamixelControlTable.LEN_MX_GOAL_POSITION, data)


        if dxl_addparam_result != 1:
            print(str(self.identity) + " groupBulkWrite addparam failed")
        return None

    def read_motor_encoder(self):
        # if UserVariables.motor_method == "position":
        #     self.position = 0
        #     self.record_data.position(self.position)  # record a new position datapoint
        #     return self.position

        dxl_getdata_result = self.groupread_num.isAvailable(self.ID, DynamixelControlTable.ADDR_MX_PRESENT_POSITION,DynamixelControlTable.LEN_MX_PRESENT_POSITION)
        if dxl_getdata_result != 1:
            print("Error: [ID:%03d] groupBulkRead getdata failed" % (self.ID))
        self.position = self.groupread_num.getData(self.ID, DynamixelControlTable.ADDR_MX_PRESENT_POSITION, DynamixelControlTable.LEN_MX_PRESENT_POSITION)/4096*360

        self.record_data.position(self.position) #record a new position datapoint
        return self.position

    def move_torque(self, current):
        self.add_write_param_torque(current) #send the new currents to the motors

    def move_position(self, position):
        self.add_write_param_position(position)

    def move_velocity(self, velocity):
        self.add_write_param_velocity(velocity)


    def move_to_home(self):
        return None

class SendRecieveBulk(object):
    def __init__(self, groupread_num, groupwrite_num):
        """
        :param groupread_num: Dynamixel object
        :param groupwrite_num: Dynamixel object

        This class handles the writing of bulk parameters that update the motor torque, or velocity or acceleration.
        """
        self.groupread_num = groupread_num
        self.groupwrite_num = groupwrite_num
        return None

    def transmit_read(self):
        self.groupread_num.txRxPacket()
        return None

    def transmit_write(self):
        self.groupwrite_num.txPacket()
        return None

    def clear_read_param(self):
        self.groupread_num.clearParam()
        return None

    def clear_write_param(self):
        self.groupwrite_num.clearParam()
        return None