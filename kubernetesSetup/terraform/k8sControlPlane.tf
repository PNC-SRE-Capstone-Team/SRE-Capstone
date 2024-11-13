resource "proxmox_vm_qemu" "k8s_control_plane" {
  vmid        = 200 + "${count.index + 1}"
  count       = var.master_count
  name        = "k8s-control-plane-${count.index + 1}"
  target_node = var.proxmox_node
  cores       = 4
  memory      = 8192
  scsihw      = "virtio-scsi-pci"
  bootdisk    = "scsi0"
  tags        = "k8s,control"
  agent       = 1
  
  disk {
    size         = "50G"
    type         = "disk"
    storage      = "local-zfs"
    slot         = "scsi0"
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  clone = var.template_name
}