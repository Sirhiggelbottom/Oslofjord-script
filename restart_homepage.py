import subprocess
import argparse

def restartPorts():
    try:
        command = f"lsof -i"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        result = process.stdout

        if result == "":
            print("No result")
            return
        
        pids = []
        pid = None

        ports = []
        port = None

        lines = result.splitlines()
        for line in lines[1:]:
            columns = line.split()

            if len(columns) < 9:
                print("Error, ports not available")
                return

            process_name = columns[0]
            
            if process_name == "node" or process_name == "python3":
                pid = columns[1]
                port = int(columns[8].split(":")[1].split(" ")[0])

                pids.append(pid)
                ports.append(port)

        for pID in pids:
            subprocess.run(f"kill {pID}")

        for newPort in ports:
            if newPort == 3000:
                print("Restarting server")
                subprocess.run(f"python3 start_backend.py", shell=True)
            elif newPort == 9999:
                print("Restarting client")
                subprocess.run(f"python3 start_host.py", shell=True)


    except Exception as e:
        print(f"Error: {e}")
        

def restart(port):
    try:
        command = f"lsof -i :{port}"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        result = process.stdout
               

        if result == "":
            print(f"No processes found on port: {port}")
            return
        
        
        print(f"Processes found on port {port}:")
        print(result)

        
        pid = None

        lines = result.splitlines()
        for line in lines[1:]:
            columns = line.split()

            if len(columns) < 2:
                print("Error, PID not available")
                return
            else:
                pid = columns[1]


        if pid == None:
            print("Error, couldn't find the PID")
            return
        
        print(f"Stopping process: {pid}")

        subprocess.run(f"kill {pid}", shell=True)

        new_port = int(port)

        if new_port == 3000:
            
            try:

                print("Restarting server")
                subprocess.run(f"python3 start_backend.py", shell=True)

            except Exception as e:
                print(f"Error, kunne ikke restarte Backend server.\nGrunn: {e}")


        elif new_port == 9999:
            
            try:

                print("Restarting client")
                subprocess.run(f"python3 start_host.py", shell=True)
            except Exception as e:
                print(f"Error, kunne ikke restarte Host server.\nGrunn: {e}")               

            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Restarting process if the process uses the specified port')
    parser.add_argument('--port', type=int, help='The port to check for running processes')
    parser.add_argument('--both', type=str, help='Restart both servers')

    args = parser.parse_args()

    if args.both is not None:
        restartPorts()
    elif args.port is None:
        port = input("Please specify to port to check: ")
    else:
        port = args.port
        
    restart(port)