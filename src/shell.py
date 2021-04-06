import subprocess

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = ""
    
    while True:
        out = proc.stdout.readline()
        err = proc.stderr.readline()
        if out == '' and proc.poll() is not None:
            break
        if out:
            output += out
        if err:
            output += err

    return output

