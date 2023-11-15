import win32file
import win32con
import win32api
import winioctlcon
import struct

def hex_dump(data):
    # Group the bytes into lines of 16 bytes each
    lines = [data[i:i+16] for i in range(0, len(data), 16)]

    for line in lines:
        hex_line = ' '.join(f'{byte:02X}' for byte in line)
        char_line = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in line)

        print(f'{hex_line.ljust(48)} {char_line}')

def create_file(file_path):
    desired_access = win32file.GENERIC_READ | win32file.GENERIC_WRITE
    share_mode = win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE
    creation_disposition = win32con.OPEN_EXISTING
    flags_and_attributes = 0

    file_handle = win32file.CreateFile(file_path, desired_access, share_mode, None, creation_disposition, flags_and_attributes, None)

    if file_handle == win32file.INVALID_HANDLE_VALUE:
        print("Error opening file:", win32api.GetLastError())
        return None

    return file_handle

def process_and_print_buffer(buffer, operation_name):
    print(f"{operation_name} Output Buffer:")
    print(buffer.hex())
    hex_dump(buffer)
    # You can add additional processing logic based on your needs

def device_io_control(file_handle, control_code, input_buffer, input_size, output_buffer, output_size):
    # win32file.DeviceIoControl(disk_handle,IOCTL_SCSI_PASS_THROUGH_DIRECT  , data,         0,          None)
    #           DeviceIoControl(Device,     IoControlCode                   , InBuffer ,    OutBuffer , Overlapped )
    result = win32file.DeviceIoControl(file_handle, control_code, input_buffer, output_buffer, None)

    if result:
        print(f"{control_code} succeeded")
        process_and_print_buffer(output_buffer, f"{control_code}")
    else:
        print(f"Error in {control_code}:", win32api.GetLastError())

def close_handle(file_handle):
    win32file.CloseHandle(file_handle)


def get_model_name(file_handle):
    # Assuming IOCTL_SCSI_PASS_THROUGH_DIRECT is used to retrieve SCSI information
    IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4D014
    input_buffer = b'\x00' * 44
    output_buffer = bytearray(44)

    print(file_handle)

    result = win32file.DeviceIoControl(file_handle, IOCTL_SCSI_PASS_THROUGH_DIRECT, input_buffer, output_buffer, None)

    if result:
        # Process the output buffer to get the model name (adjust the offset and length based on your device's response)
        model_name = output_buffer[16:32].decode('utf-8').strip('\0')
        print(f"Model Name: {model_name}")
    else:
        print("Error in IOCTL_SCSI_PASS_THROUGH_DIRECT:", win32api.GetLastError())


# #	Time of Day	Thread	Module	API	Return Value	Error	Duration
#  5553	2:37:31.782 PM	1	FXASPI.dll	CreateFileA ( "\\.\D:", GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL )	0x00000264		0.0000983


file_path = r"\\.\E:"
file_handle = create_file(file_path)

if file_handle:
    try:
        # IOCTL_STORAGE_QUERY_PROPERTY
        IOCTL_STORAGE_QUERY_PROPERTY = 0x2D1400
        input_buffer = b'\x00' * 8 + b'\x03' + b'\x00' * 3
        output_buffer = bytearray(8)
        print("== IOCTL_STORAGE_QUERY_PROPERTY ")
        device_io_control(file_handle, IOCTL_STORAGE_QUERY_PROPERTY, input_buffer, 12, output_buffer, 8)

        # Another IOCTL_STORAGE_QUERY_PROPERTY
        input_buffer = b'\x00' * 8 + b'\x03' + b'\x00' * 3
        output_buffer = bytearray(116)
        print("== IOCTL_STORAGE_QUERY_PROPERTY ")
        device_io_control(file_handle, IOCTL_STORAGE_QUERY_PROPERTY, input_buffer, 12, output_buffer, 396)

        # IOCTL_SCSI_GET_ADDRESS
        IOCTL_SCSI_GET_ADDRESS = 0x41018 # 0x0004100C 
        output_buffer = bytearray(8)
        print("== IOCTL_SCSI_GET_ADDRESS ")
        device_io_control(file_handle, IOCTL_SCSI_GET_ADDRESS, None, 0, output_buffer, 8)

        get_model_name(file_handle)

        # IOCTL_SCSI_PASS_THROUGH_DIRECT
        IOCTL_SCSI_PASS_THROUGH_DIRECT = 0x4d014
        input_buffer = b'\x00' * 44
        output_buffer = bytearray(44)
        print("== IOCTL_SCSI_PASS_THROUGH_DIRECT ")
        device_io_control(file_handle, IOCTL_SCSI_PASS_THROUGH_DIRECT, input_buffer, 44, output_buffer, 44)


    finally:
        # Close the file handle
        close_handle(file_handle)