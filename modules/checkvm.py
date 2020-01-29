from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import atexit


host="localhost"
user="devops"
password="Fosla2015!"
port=443

def listvms(uuid):
    try:
        service_instance = connect.SmartConnect(host=host,user=user,pwd=password,port=port)
        atexit.register(connect.Disconnect, service_instance)
        search_index = service_instance.content.searchIndex
        vm = search_index.Find

    except vmodl.MethodFault as error:
        return "Caught vmodl fault : " + error.msg

 
    return 0