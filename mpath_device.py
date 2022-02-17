#!/usr/bin/env python3
import re, os, time, sys, getopt

def parse_mdev(val):
    m_d = re.findall('mpa[a-z]*', val)
    return m_d

def parse_ldev(val):
    l_d = re.findall('sd[a-z]*', val)
    return l_d

def scan_newd():
    os.system('for host in `ls /sys/class/scsi_host`;do echo ${host}; echo "- - -" > /sys/class/scsi_host/${host}/scan;done')
    newdev = mpath()
    newm_devices = parse_mdev(newdev)
    for newm_dev in range(0, len(newm_devices)):
        if newm_devices[newm_dev] in z:
            continue
        else:
            print("new devices in file new_dev")
            with open ('new_dev', 'a') as db:
                db.write(newm_devices[newm_dev] + '\n')

def del_all_md():
    print("Delete devices: ", ", ".join(m_devices))
    os.system('multipath -F')
    time.sleep(2)
    print("delete devices: ", ", ".join(l_devices))
    for l_device in range(0, len(l_devices)):
        print("do delete: ", l_devices[l_device])
        os.system('echo "1" > /sys/block/' + l_devices[l_device] + '/device/delete')
        time.sleep(2)

def del_md(m_dev):
    print("delete device: ", m_dev)
    mdev = mpath(m_dev)
    hdds = parse_ldev(mdev)
    os.system('multipath -f m_dev')
    print("do delete devices: ", ", ".join(hdds))
    for hdd in range(0, len(hdds)):
        print("Do delete: ", hdds[hdd])
        os.system('echo "1" > /sys/block/' + hdds[hdd] + '/device/delete')
        time.sleep(2)


def rescan_d(m_dev):
    mdev = mpath(m_dev)
    hdds = parse_ldev(mdev)
    for hdd in range(0, len(hdds)):
         os.system('echo "1" > /sys/block/' + hdds[hdd] + '/device/rescan')
    #pvresize

def mpath (dev):
    if dev == None:
        m_p = os.popen('multipath -ll').read()
    else:
        m_p = os.popen('multipath -ll ' + dev).read()
    return m_p
def info():
    print('''                 multipath-devices
        -s | --scan scan 
        -r mdevice | --rescan mdevice rescan multipath 
        -d mdevice | --delmd mdevice remove multipath devices  and all pathes
        -D | --delall Dell all multipath devices and pathes''')
argv = sys.argv[1:]
if len(argv) == 0:
    info()
    exit(1)
try:
    options, args = getopt.getopt(argv,"sd:r:Dh",
                                  ["scan",
                                   "delmd =",
                                   "rescan =",
                                   "delall",
                                   "help"])
except:
    info()
    exit(1)

for name, value in options:
    if name in ['-s', '--scan']:
        scan_newd()
    elif name in ['-d', '--delmd ']:
        del_md(value)
    elif name in ['-r', '--rescan ']:
        rescan_d(value)
    elif name in ['-D', '--delall']:
        del_all_md()
    elif name in ['-h', '--help']:
        info()

#print("save in file: before_scan_device")
#os.system('multipath -ll > before_scan_device')
#db = '/home/coder/before_scan'
#with open (db, 'r') as file:
#    z = file.read()
#m_devices = parse_mdev(z)
#l_devices = parse_ldev(z)
