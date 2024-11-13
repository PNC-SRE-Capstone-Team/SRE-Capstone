from proxmoxer import ProxmoxAPI
from azure.keyvault.secrets import SecretClient
from azure.identity  import DefaultAzureCredential
import requests
import json
import os
import yaml

# Authenticate to Azure KeyVault to retrieve secrets\
credential = DefaultAzureCredential()
KVUri = f"https://bluelockkeyvault.vault.azure.net"
client = SecretClient(vault_url=KVUri, credential=credential)

# Replace these with your Proxmox credentials and server
PROXMOX_HOST = "kunigami.damdiel.com"
PROXMOX_TOKEN_ID = "azureToken"
PROXMOX_SECRET = retrieved_secret = client.get_secret("kunigamiAPISecret").value # Token Secret from Azure Key Vault
PROXMOX_USER = "terraformSA@pve"
PROXMOX_VERIFY_SSL = True  # Set to True if you want to verify SSL

# Connect to Proxmox API
proxmox = ProxmoxAPI(
    PROXMOX_HOST,
    token_name=PROXMOX_TOKEN_ID,
    token_value=PROXMOX_SECRET,
    user=PROXMOX_USER,
    verify_ssl=PROXMOX_VERIFY_SSL
)

# Fetch VM list from Proxmox
def get_vms():
    vms = []
    for node in proxmox.nodes.get():
        for vm in proxmox.nodes(node['node']).qemu.get():
            proxmox.nodes(node['node']).qemu
            vms.append(vm)
    return vms

def retrieve_interface_info(vm, vm_name):
    # Retrieve all interface info
    interfaces = proxmox.nodes((proxmox.nodes.get())[0]['node']).qemu(vm['vmid']).agent.get('network-get-interfaces')['result']

    # Filter out ip4 interface address excluding loopback. If multiple, will only take first.
    # Not built to handle empty list, will cause index error.
    vm_ip = [ip_info['ip-address'] for interface in interfaces for ip_info in interface.get('ip-addresses', []) if ip_info['ip-address-type'] == 'ipv4' and not ip_info['ip-address'].startswith('127.')][0]
    
    # Create JSON entry for each VM
    vm_entry = {
        "hostname": vm_name,
        "ip": vm_ip
    }
    return vm_entry


# Generate Ansible Inventory JSON format
def generate_json_inventory(vms):
    inventory = []

    for vm in vms:
        tags = vm.get('tags', "")
        vm_name = vm['name']
        if 'k8s' in tags:
            if 'control' in tags:
                inventory.append(retrieve_interface_info(vm, vm_name))
    for vm in vms:
        tags = vm.get('tags', "")
        vm_name = vm['name']
        if 'k8s' in tags:
            if 'worker' in tags:
                inventory.append(retrieve_interface_info(vm, vm_name))

    return inventory

if __name__ == "__main__":
    vms = get_vms()  # Ensure get_vms() is defined and working correctly

    # Generate the inventory
    inventory = generate_json_inventory(vms)

    # Print the JSON output in a readable format
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'k3sInventory.json')
    with open(file_path, "w") as json_file:
        json.dump(inventory, json_file, indent=2)