
"""
Python program for listing the vms on an Workstation/ESX / vCenter host
"""

from __future__ import print_function

from pyVim.connect import SmartConnect, Disconnect
import atexit
import ssl

def GetVMs(host,user,password,port):
   """
   Simple program for listing the virtual machines on a system.
   """

   context = None
   if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()
   si = SmartConnect(host=host,
                     user=user,
                     pwd=password,
                     port=443,
                     sslContext=context)
   if not si:
       print("Could not connect to the specified host using specified "
             "username and password")
       return -1

   atexit.register(Disconnect, si)

   content = si.RetrieveContent()
   for child in content.rootFolder.childEntity:
      if hasattr(child, 'vmFolder'):
         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         
   return vmList
