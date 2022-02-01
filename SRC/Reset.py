import subprocess
from sys import argv

def kill(Bot, Chrome):

    try:
        subprocess.call(["kill", Bot])
        subprocess.call(["kill", Chrome])
    except:
        print("Error: Could not kill process")
        return False

    return True

def reset():
    subprocess.call(["python3", "entrypoint.py"])

if __name__ == "__main__":

    ScriptPID = argv[1]
    ChromePID = argv[2]

    if kill(ScriptPID, ChromePID):
        reset()
        exit(0)
    else:
        print("Error: Could not kill process")
        exit(1)