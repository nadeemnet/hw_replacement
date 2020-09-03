#!/usr/bin/env python3
'''
This script reads data from cdp_nbrs.yaml file.
After login to the switch, it verifies CDP neigbors are learned on the correct ports
'''
import pdb
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
    with open('cdp_nbrs.yaml') as f:
        cdp_nbrs_old = yaml.safe_load(f)
    device = {
        "ip": switch_ip,
        "device_type": switch_os,
        "username": secrets.sw_user,
        "password": secrets.sw_pwd,
        "verbose": True,
        "session_log": 'session.log',
    }

    try:
        connection = ConnectHandler(**device)
        connection.enable()
        cdp_nbrs_new = connection.send_command("show cdp neighbors", use_textfsm=True)
        connection.disconnect()
    except Exception:
        print("Error: Could not make an SSH connection")
     
    if len(cdp_nbrs_new) == len(cdp_nbrs_old):
        print('INFO: old CDP neighbors: {}'.format(len(cdp_nbrs_old)))
        print('INFO: new CDP neighbors: {}'.format(len(cdp_nbrs_new)))
    else:    
        print("** Warning: CDP neighbors are not equal **")
        print('old CDP neighbors: {}'.format(len(cdp_nbrs_old)))
        print('new CDP neighbors: {}'.format(len(cdp_nbrs_new)))
    print('Ensure every nbr exists on the same port as before')
    for new_nbr in cdp_nbrs_new:
        for old_nbr in cdp_nbrs_old:
            if new_nbr['local_interface'] == old_nbr['local_interface']:
                if not new_nbr['neighbor'] == old_nbr['neighbor']:
                    print('** CDP neighbor data did not match **')
                    print('local interface:', new_nbr['local_interface'])
                    print('old nbr:', old_nbr['neighbor'])
                    print('new nbr:', new_nbr['neighbor'])

if __name__ == "__main__":
    main(args.switch_ip, args.switch_os)