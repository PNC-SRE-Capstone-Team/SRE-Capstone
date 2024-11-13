variable "proxmox_api_url" {
  description = "URL of the Proxmox API"
  type        = string
  default     = "https://kunigami.damdiel.com:8006/api2/json"
}

variable "proxmox_user" {
  description = "Proxmox API user"
  type        = string
  default     = "terraformSA@pve!azureToken"
}

variable "key_vault_name" {
  description = "Name of the Azure Key Vault"
  type        = string
  default     = "bluelockKeyVault"
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "homelabRG"
}

variable "proxmox_api_secret_name" {
  description = "Name of the secret in Azure Key Vault that holds the Proxmox API key"
  type        = string
  default     = "kunigamiAPISecret"
}

variable "proxmox_node" {
  description = "Proxmox node where the VMs will be created"
  type        = string
  default     = "kunigami"
}

variable "template_name" {
  description = "Name of the VM template to clone for the Kubernetes control plane and worker nodes"
  type        = string
  default     = "ubuntu-24.04-template"
}

# variable "root_password" {
#   description = "Root password for the VMs"
#   type        = string
# }

variable "worker_count" {
  description = "Number of worker nodes to create"
  type        = number
  default     = 3
}

variable "master_count" {
  description = "Number of master nodes to create"
  type        = number
  default     = 3
}
