terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "3.0.1-rc4"  # You can specify the latest stable version or a different one
    }
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.116.0"
    }
  }
}


provider "proxmox" {
  pm_api_url      = var.proxmox_api_url
  pm_api_token_id         = var.proxmox_user
  pm_api_token_secret     = data.azurerm_key_vault_secret.proxmox_api_key.value

  #This is only needed if you haven't configured an SSL certificate for your proxmox domain
  #pm_tls_insecure = true
}

provider "azurerm" {
  features {}
}

data "azurerm_key_vault" "example" {
  name                = var.key_vault_name
  resource_group_name = var.resource_group_name
}

data "azurerm_key_vault_secret" "proxmox_api_key" {
  name         = var.proxmox_api_secret_name
  key_vault_id = data.azurerm_key_vault.example.id
}
