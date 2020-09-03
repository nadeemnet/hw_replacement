hw-replacement
==============

The python scripts help during switch replacement (hw-upgrade or RMAing a switch). During switch replacement,  we need to remove all cables and then plug them back once the new switch is installed. This can introduce some issues related to mis-cabling and/or link up/down issues. These scripts help in verifying:

1) All Ethernet and Port Channels interfaces that were 'UP' before are still 'UP' after switch replacement.
2) A particular CDP neighbor is learned on the same port as before.

Interface up
------------
Following two files are used to verify interface 'UP' status.
1) gen_up_intf.py: This generates a list of interfaces that are in UP state.
2) verify_up_intf.py: Using the output from above file, this verifies that all interfaces are still in UP state after switch replacement.

These scripts use python naplam module whis is document at following link.
https://napalm.readthedocs.io/en/latest/


CDP Neighbors
-------------
Following two files verify CDP neighbors are learned correctly.
1) gen_cdp_nbrs.py: This generates a list of CDP neihbors before switch replacement.
2) verify_cdp_nbrs.py: Based on the information from above file, this verifies that all CDP neighbors are learned on the ports as before.

These scripts use ntc-templates. More infomation is available at follwoing github page.
https://github.com/networktocode/ntc-templates


Login credentials
-----------------
Switch login credentails should be stored in a seperate file called secrets.py
The contents of secrets.py
sw_user = ''
sw_pwd = ''

Example Runs:
-------------

```
On Cisco IOS switch:
python3 gen_up_intf.py --switch_ip 10.10.32.42 --switch_os ios
python3 gen_cdp_nbrs.py --switch_ip 10.10.32.42 --switch_os cisco_ios

python3 verify_up_intf.py --switch_ip 10.10.32.42 --switch_os ios
python3 verify_cdp_nbrs.py --switch_ip 10.10.32.42 --switch_os cisco_ios

On Cisco NXOS switch:
python3 gen_up_intf.py --switch_ip 10.10.32.11 --switch_os nxos_ssh
python3 gen_cdp_nbrs.py --switch_ip 10.10.32.11 --switch_os cisco_nxos

python3 verify_up_intf.py --switch_ip 10.10.32.11 --switch_os nxos_ssh
python3 verify_cdp_nbrs.py --switch_ip 10.10.32.11 --switch_os cisco_nxos
```


Note:
-----

These scripts assume that interface naming conventions are same within old and new switch. This usually means the same vendor and model of switch.

