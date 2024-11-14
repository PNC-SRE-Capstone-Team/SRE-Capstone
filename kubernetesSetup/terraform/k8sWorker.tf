resource "proxmox_vm_qemu" "k8s_worker" {
  vmid        = 205 + "${count.index + 1}"
  count       = var.worker_count
  name        = "k8s-worker-${count.index + 1}"
  target_node = var.proxmox_node
  cores       = 2
  memory      = 4096
  scsihw      = "virtio-scsi-pci"
  bootdisk    = "scsi0"
  tags        = "k8s,worker"
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

  depends_on = [ 
    proxmox_vm_qemu.k8s_control_plane
   ]

}