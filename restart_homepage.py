import subprocess
import argparse

def restart(port):
    try:
        command = f"lsof -i :{port}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        text_result = result.stdout
               

        if text_result == "":
            print(f"No processes found on port: {port}")
            return
        
        
        print(f"Processes found on port {port}:")
        print(text_result)

        
        pid = None

        lines = text_result.splitlines()
        for line in lines[1:]:
            columns = line.split()

            if len(columns) < 2:
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

    args = parser.parse_args()

    if args.port is None:
        port = input("Please specify to port to check: ")
    else:
        port = args.port
        
    restart(port)