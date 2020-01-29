"""
Tool: Mal-Evolve
Author: Wrickdev Ghosh
"""

import sys,time,getpass
from modules import process_check,colorprint,listvms
from pyVmomi import vim

user = "devops"
host = "localhost"
port = 443

def PrintVmInfo(vm, depth=1):
   """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
   maxdepth = 10

   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         PrintVmInfo(c, depth+1)
      return

   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
   if isinstance(vm, vim.VirtualApp):
      vmList = vm.vm
      for c in vmList:
         PrintVmInfo(c, depth + 1)
      return

   summary = vm.summary
   print("Name       : ", summary.config.name)
   print("Path       : ", summary.config.vmPathName)
   print("Guest      : ", summary.config.guestFullName)
   annotation = summary.config.annotation
   if annotation != None and annotation != "":
      print("Annotation : ", annotation)
   print("State      : ", summary.runtime.powerState)
   if summary.guest != None:
      ip = summary.guest.ipAddress
      if ip != None and ip != "":
         print("IP         : ", ip)
   if summary.runtime.question != None:
      print("Question  : ", summary.runtime.question.text)
   print("")


def sanity_check():
    """
    Checks if the fwg prerequisite conditions are met
    1. vmware-hostd service should be running
    2. Template VMs should be present
    """
    """
    Sanity Check 1
    """
    print (colorprint.colored("[+] Running Sanity Checks ",colorprint.INFO))
    time.sleep(0.5)
    print (colorprint.colored("[+] Checking if VMware Workstation Server service is running! ",colorprint.INFO))
    time.sleep(0.5)
    if process_check.proccheck("vmware-hostd") is True:
        print (colorprint.colored("[+] VMware Workstation Server service is running! ",colorprint.INFO))
        time.sleep(0.5)
    else:
        print (colorprint.colored("[+] ERROR: Please ensure that VMWare Workstation is running and template VMs are shared! ",colorprint.FAIL))
        time.sleep(0.5)
        SystemExit
    """
    Sanity Check 2
    """
    print (colorprint.colored("[+] Checking if Template VMs are present! ",colorprint.INFO))
    time.sleep(0.5)
    password = getpass.getpass(prompt="Enter VMware Workstation/ESXi password -")
    vmList = listvms.GetVMs(host,user,password,port)
    for vm in vmList:
            PrintVmInfo(vm)
    

if __name__ == '__main__':

    sanity_check()