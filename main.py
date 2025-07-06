# developed by: https://github.com/Daradege
# 1404/04/15 - (july 6, 2025)

import psutil
import os
import sys
import tkinter
from tkinter import ttk
import time
import jdatetime
import datetime
import subprocess
import re
import distro
import webbrowser

__version__ = "0.1.0"

def open_site(url):
    webbrowser.open(url)

def get_graphic_card_info():
    try:
        graphic_card_info = os.popen("lspci | grep -i vga").read().split(":")[2].strip()
        return graphic_card_info.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_platform_info():
    try:
        dist = f"{distro.name()} {distro.version()} {distro.codename().capitalize()}"
        return dist.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_system_uptime():
    try:
        uptime = os.popen("uptime -p").read()
        return uptime.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_system_cores_count():
    try:
        cores_count = os.cpu_count()
        return cores_count
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_cpu_model():
    try:
        cpu_model = os.popen("cat /proc/cpuinfo | grep 'model name'").read().split('\n')[0].split(':')[1].strip()
        return cpu_model.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_graphic_driver_info():
    try:
        graphic_driver_info = os.popen("glxinfo | grep 'OpenGL vendor string'").read()
        return graphic_driver_info.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_system_memory_info():
    try:
        memory_info = psutil.virtual_memory()
        return memory_info
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_system_disk_info():
    try:
        disk_info = psutil.disk_usage('/')
        return disk_info
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_user_info():
    try:
        user_info = os.popen("whoami").read().strip()
        return user_info
    except Exception as e:
        print(f"Error: {e}")
        return None

def network_connection_status():
    try:
        network_status = subprocess.run(["ping", "-c", "1", "google.com"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2).returncode == 0
        return network_status
    except (Exception, subprocess.TimeoutExpired) as e:
        print(f"Error: {e}")
        return False

def network_updown(interval=0.1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    upload = net2.bytes_sent - net1.bytes_sent
    download = net2.bytes_recv - net1.bytes_recv

    kb_upload = upload / 1024
    kb_download = download / 1024
    return kb_upload, kb_download

def has_python_installed():
    try:
        python_version = sys.version.split()[0]
        if python_version:
            return python_version
        else:
            return "Python is not installed."
    except Exception as e:
        print(f"Error: {e}")
        return None

def has_java_installed():
    try:
        result = subprocess.run(["java", "-version"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output = result.stderr.strip().split("\n")

        version_line = output[0] if output else "Unknown"
        vendor_line = output[1] if len(output) > 1 else ""
        vm_line = output[2] if len(output) > 2 else ""

        version_match = re.search(r'version\s+"([\d._]+)"', version_line)
        version = version_match.group(1) if version_match else "Undefinemd"

        if "OpenJDK" in version_line or "OpenJDK" in vendor_line:
            vendor = "OpenJDK"
        elif "Java(TM)" in version_line or "HotSpot" in vm_line:
            vendor = "Oracle"
        elif "GraalVM" in vendor_line or "GraalVM" in vm_line:
            vendor = "GraalVM"
        elif "Temurin" in vendor_line or "Adoptium" in vendor_line:
            vendor = "Temurin (Adoptium)"
        else:
            vendor = "Undefined"

        return f"{vendor} {version}"

    except FileNotFoundError:
        return "Java is not installed."


def has_nodejs_installed():
    try:
        nodejs_version = os.popen("node -v").read()
        if nodejs_version:
            return nodejs_version.strip()
        else:
            return "Node.js is not installed."
    except Exception as e:
        print(f"Error: {e}")
        return None

def has_php_installed():
    try:
        php_version = os.popen("php -v").read()
        if php_version:
            return php_version.strip()
        else:
            return "PHP is not installed."
    except Exception as e:
        print(f"Error: {e}")
        return None

def has_dotnet_installed():
    try:
        dotnet_version = os.popen("dotnet --version").read()
        if dotnet_version:
            return dotnet_version.strip()
        else:
            return ".NET is not installed."
    except Exception as e:
        print(f"Error: {e}")
        return None

def time_shamsi():
    try:
        now = jdatetime.datetime.now()
        return now.strftime("%Y/%m/%d %H:%M:%S")
    except Exception as e:
        print(f"Error: {e}")
        return None

def time_gregorian():
    try:
        now = datetime.datetime.now()
        return now.strftime("%Y/%m/%d %H:%M:%S")
    except Exception as e:
        print(f"Error: {e}")
        return None
    

root = tkinter.Tk()
root.title("DTBox System Information")

root.geometry("500x500")

tabControl = ttk.Notebook(root)

graphics_tab = ttk.Frame(tabControl)
date_and_time_tab = ttk.Frame(tabControl)
system_info_tab = ttk.Frame(tabControl)
network_tab = ttk.Frame(tabControl)
software_tab = ttk.Frame(tabControl)
os_tab = ttk.Frame(tabControl)
creator_tab = ttk.Frame(tabControl)

tabControl.add(graphics_tab, text='Graphics')
tabControl.add(date_and_time_tab, text='Date and Time')
tabControl.add(system_info_tab, text='System Info')
tabControl.add(network_tab, text='Network')
tabControl.add(software_tab, text='Software')
tabControl.add(os_tab, text='OS')
tabControl.add(creator_tab, text='Creator')

tabControl.pack(expand=1, fill="both")

# ----------

lbframe_graphics = ttk.LabelFrame(graphics_tab, text='Graphics')
lbframe_graphics.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_graphic_card_info = ttk.Label(lbframe_graphics, text=f'Graphic Card Info: {get_graphic_card_info()}')
lb_graphic_card_info.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_graphic_driver_info = ttk.Label(lbframe_graphics, text=f'Graphic Driver Info: {get_graphic_driver_info()}')
lb_graphic_driver_info.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# ----------

def tick_time():
    lb_time_shamsi.config(text=f'Time Shamsi: {time_shamsi()}')
    lb_time_gregorian.config(text=f'Time Gregorian: {time_gregorian()}')
    lb_time_epoch.config(text=f'Time Epoch: {time.time()}')
    root.after(1000, tick_time)

lbframe_date_and_time = ttk.LabelFrame(date_and_time_tab, text='Date and Time')
lbframe_date_and_time.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_time_shamsi = ttk.Label(lbframe_date_and_time, text=f'Time Shamsi: {time_shamsi()}')
lb_time_shamsi.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_time_gregorian = ttk.Label(lbframe_date_and_time, text=f'Time Gregorian: {time_gregorian()}')
lb_time_gregorian.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
lb_time_epoch = ttk.Label(lbframe_date_and_time, text=f'Time Epoch: {time.time()}')
lb_time_epoch.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
lb_time_zone = ttk.Label(lbframe_date_and_time, text=f'Time Zone: {time.tzname[0]} | {time.tzname[1]}')
lb_time_zone.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
lb_time_zone_offset = ttk.Label(lbframe_date_and_time, text=f'Time Zone Offset: {time.timezone}')

tick_time()

# ----------

def tick_system():
    lb_cpu_info.config(text=f'CPU Model: {get_cpu_model()}')
    lb_ram_info.config(text=f'RAM Info: {round(get_system_memory_info().used / (1024 ** 3),2)} GB / {round(get_system_memory_info().total / (1024 ** 3),2)} GB ({get_system_memory_info().percent}%)')
    lb_disk_info.config(text=f'Disk Info (/): {round(get_system_disk_info().total / (1024 ** 3), 2)} GB')
    lb_system_uptime.config(text=f'Uptime: {get_system_uptime()}')
    root.after(3000, tick_system)

lbframe_system_info = ttk.LabelFrame(system_info_tab, text='System Info')
lbframe_system_info.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_cpu_info = ttk.Label(lbframe_system_info, text=f'CPU Model: {get_cpu_model()}')
lb_cpu_info.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_ram_info = ttk.Label(lbframe_system_info, text=f'RAM Info: {round(get_system_memory_info().used / (1024 ** 3),2)} GB / {round(get_system_memory_info().total / (1024 ** 3),2)} GB ({get_system_memory_info().percent}%)')
lb_ram_info.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
lb_disk_info = ttk.Label(lbframe_system_info, text=f'Disk Info (/): {round(get_system_disk_info().total / (1024 ** 3), 2)} GB')
lb_disk_info.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
lb_system_uptime = ttk.Label(lbframe_system_info, text=f'System Uptime: {get_system_uptime()}')
lb_system_uptime.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

tick_system()

# ----------

def tick_network():
    network_data = network_updown()
    lb_network_upload_data.config(text=f'Network Uploading Data: {round(network_data[0], 2)} KB')
    lb_network_download_data.config(text=f'Network Downloading Data: {round(network_data[1], 2)} KB')
    root.after(1000, tick_network)

def tick_network_is_on():
    lb_network_status.config(text=f'Network Status: {network_connection_status()}')
    root.after(5000, tick_network_is_on)

lbframe_network = ttk.LabelFrame(network_tab, text='Network')
lbframe_network.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
lb_network_status = ttk.Label(lbframe_network, text=f'Network Status: {network_connection_status()}')
lb_network_status.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_network_upload_data = ttk.Label(lbframe_network, text=f'Network Uploading Data: {round(network_updown()[0] / (1024 ** 2), 2)} MB')
lb_network_upload_data.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

lb_network_download_data = ttk.Label(lbframe_network, text=f'Network Downloading Data: {round(network_updown()[1] / (1024 ** 2), 2)} MB')
lb_network_download_data.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

tick_network()
tick_network_is_on()

# ----------

lbframe_software = ttk.LabelFrame(software_tab, text='Software')
lbframe_software.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_python_version = ttk.Label(lbframe_software, text=f'Python Version: {has_python_installed()}')
lb_python_version.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_java_version = ttk.Label(lbframe_software, text=f'Java Version: {has_java_installed()}')
lb_java_version.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

lb_node_version = ttk.Label(lbframe_software, text=f'Node Version: {has_nodejs_installed()}')
lb_node_version.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

lb_php_version = ttk.Label(lbframe_software, text=f'PHP Version: {has_php_installed()}')
lb_php_version.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

lb_dotnet_version = ttk.Label(lbframe_software, text=f'.NET Version: {has_dotnet_installed()}')
lb_dotnet_version.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

# ----------

lbframe_os = ttk.LabelFrame(os_tab, text='OS')
lbframe_os.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_os_name = ttk.Label(lbframe_os, text=f'OS Name: {get_platform_info()}')
lb_os_name.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_os_user = ttk.Label(lbframe_os, text=f'OS User: {get_user_info()}')
lb_os_user.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# ----------

lbframe_creator = ttk.LabelFrame(creator_tab, text='Creator')
lbframe_creator.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_creator_name = ttk.Label(lbframe_creator, text=f'Creator Name: Ali Safamanesh')
lb_creator_name.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

lb_creator_github = ttk.Label(lbframe_creator, foreground="blue", text=f'Creator Github: https://github.com/Daradege')
lb_creator_github.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
lb_creator_github.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/Daradege"))

lb_project_license = ttk.Label(lbframe_creator, text=f'Project License: GPL V3')
lb_project_license.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

lb_github_button = ttk.Button(lbframe_creator, text="Go To Github", command=lambda: webbrowser.open_new_tab("https://github.com/Daradege/DTBox"))
lb_quit_button = ttk.Button(lbframe_creator, text="Quit", command=root.quit)
lb_github_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
lb_quit_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

root.mainloop()