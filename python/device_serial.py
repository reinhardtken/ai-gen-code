import win32api
import win32con
import win32gui
import win32service
import winreg
from win32com.client import GetObject
import pythoncom

def get_device_serial_number(device_id):
    """
    Get the serial number of a device using Windows registry
    
    Args:
        device_id: Device identifier
        
    Returns:
        str: Serial number of the device or None if not found
    """
    try:
        # Open the registry key for the device
        key_path = f"SYSTEM\\CurrentControlSet\\Enum\\{device_id}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            serial_number, _ = winreg.QueryValueEx(key, "SerialNumber")
            return serial_number
    except FileNotFoundError:
        # SerialNumber key doesn't exist, try HardwareId
        try:
            key_path = f"SYSTEM\\CurrentControlSet\\Enum\\{device_id}"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                hardware_id, _ = winreg.QueryValueEx(key, "HardwareId")
                # Extract serial from hardware ID if possible
                if isinstance(hardware_id, list):
                    hardware_id = hardware_id[0]
                # Some devices encode serial in hardware ID
                if "&SERIAL" in hardware_id.upper():
                    parts = hardware_id.split("&")
                    for part in parts:
                        if part.startswith("SERIAL"):
                            return part.split("_")[1]
                return hardware_id
        except Exception:
            return None
    except Exception as e:
        print(f"Error getting serial number: {e}")
        return None

def enumerate_devices_with_serials():
    """
    Enumerate all devices and try to get their serial numbers using WMI
    """
    try:
        # Connect to WMI
        pythoncom.CoInitialize()
        wmi = GetObject("winmgmts:")
        
        # Query for devices with serial numbers
        devices = wmi.ExecQuery("SELECT * FROM Win32_PhysicalMedia")
        
        print("Devices with serial numbers:")
        for device in devices:
            if device.SerialNumber:
                print(f"Device: {device.Tag}")
                print(f"Serial Number: {device.SerialNumber.strip()}")
                print("-" * 40)
                
        # Also check Win32_DiskDrive for disk serials
        disks = wmi.ExecQuery("SELECT * FROM Win32_DiskDrive")
        print("\nDisk drives with serial numbers:")
        for disk in disks:
            if disk.SerialNumber:
                print(f"Disk: {disk.Caption}")
                print(f"Serial Number: {disk.SerialNumber.strip()}")
                print("-" * 40)
                
    except Exception as e:
        print(f"Error enumerating devices: {e}")
    finally:
        pythoncom.CoUninitialize()

def get_specific_device_serial(device_name):
    """
    Get serial number for a specific device by name using WMI
    
    Args:
        device_name (str): Name of the device
    """
    try:
        # Connect to WMI
        pythoncom.CoInitialize()
        wmi = GetObject("winmgmts:")
        
        # Query for a specific device
        devices = wmi.ExecQuery(f"SELECT * FROM Win32_DiskDrive WHERE Caption LIKE '%{device_name}%'")
        
        for device in devices:
            if device.SerialNumber:
                return device.SerialNumber.strip()
                
        return None
    except Exception as e:
        print(f"Error getting device serial: {e}")
        return None
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    print("Enumerating devices with serial numbers:")
    enumerate_devices_with_serials()
    
    # Example of getting a specific device serial (uncomment and modify as needed)
    # serial = get_specific_device_serial("USB")  # Example: USB device
    # if serial:
    #     print(f"Specific device serial: {serial}")