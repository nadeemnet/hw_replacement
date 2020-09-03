#!/usr/bin/env python3
'''
This script collects all CDP neighbors on this switch.
Results are stored in a file cdp_nbrs.yaml
This script requires ntc-templates to be installed.
More infomation is available at follwoing github page.
https://github.com/networktocode/ntc-templates
set  NET_TEXTFSM environment variable as per example below.
export NET_TEXTFSM=/netauto/sbx/ntc-ansible/ntc-templates/templates
'''
import logging
import secrets
import argparse
import yaml
from netmiko import ConnectHandler

parser = argparse.ArgumentParser()
parser.add_argument('--switch_ip')
parser.add_argument('--switch_os', default='cisco_ios', choices=['cisco_nxos', 'cisco_ios'])
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='logging.log', level=logging.INFO, format=FORMAT)


def main(switch_ip, switch_os):
    ''' main function '''
    f1 = open("cdp_nbrs.yaml", "w")
    device = {
        "ip": switch_ip,
        "device_type": switch_os,
        "username": secrets.sw_user,
        "password": secrets.sw_pwd,
        "verbose": True,
        "session_log": 'session.log',
    }
    # show cdp neighbors did not work consistently across different devices
    # An alternate is to use show cdp neighbors details command.
    # But we will have to modify the verify_cdp_nbrs.py command accordingly
    # For now, I am able to get it to work consistently after modifying textfsm template file for show cdp neighbor
    # First original line is shown and next change I made.
    #^\s+${LOCAL_INTERFACE}\s+\d+\s+${CAPABILITY}\s{2}\s*${PLATFORM}\s+${NEIGHBOR_INTERFACE} -> Record
    #^\s+${LOCAL_INTERFACE}\s+\d+\s+${CAPABILITY}\s{1}\s*${PLATFORM}\s+${NEIGHBOR_INTERFACE} -> Record
    # Looks like that file has a bug where multiple capability falgs are not handled correctly.

    try:
        connection = ConnectHandler(**device)
        connection.enable()
        result = connection.send_command("show cdp neighbors", use_textfsm=True)
        print('** CDP neighbors found: {} **'.format(len(result)))
        cdp_nbrs = yaml.dump(result)
        connection.disconnect()
    except Exception:
        print("Error: Could not make an SSH connection")

    # write yaml data into the files.
    f1.write(cdp_nbrs)
    f1.close()

if __name__ == "__main__":
    main(args.switch_ip, args.switch_os)
