import psutil
from modules import colorprint

def proccheck(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        print (colorprint.colored(proc.name().lower(),colorprint.WARN))
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print (colorprint.colored("Running processes could'nt be read: Ensure you are running the app in admin mode",colorprint.FAIL))
    return False