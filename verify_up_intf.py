#!/usr/bin/env python3

'''
This script reads interface data from these files.
1) up_ethernet.yaml
2) up_portchannel.yaml
After login to the switch, it verifies these interfaces are UP.
'''

import logging
import secrets
import argparse
import yaml
from napalm import get_network_driver

parser = argparse.ArgumentParser()
parser.add_argument('--switch_ip')
parser.add_argument('--switch_os', default='nxos_ssh', choices=['ios', 'nxos_ssh'])
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='session.log', level=logging.INFO, format=FORMAT)

def main(switch_ip, switch_os):
    with open('up_ethernet.yaml') as f:
        up_ethernet_old = yaml.safe_load(f)

    with open('up_portchannel.yaml') as f:
        up_portchannel_old = yaml.safe_load(f)

    driver = get_network_driver(switch_os)
    device = driver(switch_ip, secrets.sw_user, secrets.sw_pwd)
    device.open()

    # device.get_interfaces returns a dictionary
    # The interface names are keys of the dictionary
    # The values are another dictionary showing following info
    #   descrition
    #   is_enabled
    #   is_up
    #   last_flapped
    #   mac_address
    #   speed
    interface_list = device.get_interfaces()
    logging.debug(interface_list)
    device.close()

    up_ethernet_new = {}
    up_portchannel_new = {}
    for interface, details in interface_list.items():
        if 'Ethernet' in interface and details['is_up']:
            up_ethernet_new[interface] = details
        if 'ort-channel' in interface and details['is_up']:
            up_portchannel_new[interface] = details


    # Ensure every interface in old list is also present in the new list
    print('Verifying Ethernet interfaces')
    for interface in up_ethernet_old:   
        if interface not in up_ethernet_new:
            print('** {} is not up **\n'.format(interface))
    print('Verifying Port Channels')
    for interface in up_portchannel_old: 
        if interface not in up_portchannel_new:
            print('** {} is not up **\n'.format(interface))

if __name__ == "__main__":
    main(args.switch_ip, args.switch_os)