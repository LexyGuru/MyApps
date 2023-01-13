import psutil

def get_pid_by_name(process_name):
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == process_name.lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def wait_for_process_to_end(process_names):
    procs = []
    for process_name in process_names:
        pid = get_pid_by_name(process_name)
        if not pid:
            print(f"Process {process_name} not found.")
            continue
        procs.append(psutil.Process(pid))
    psutil.wait_procs(procs)
    for proc in procs:
        print(f"Process {proc.name()} with pid {proc.pid} has ended.")

process_names = ["Autologon.exe", "Autologon64.exe", "Autologon64a.exe"]
wait_for_process_to_end(process_names)
