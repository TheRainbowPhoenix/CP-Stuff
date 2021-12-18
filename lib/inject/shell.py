import os
import sys
import pyrasite


def shell():
    """Open a Python shell in a running process"""

    usage = "Usage: pyrasite-shell <PID>"
    if not len(sys.argv) == 2:
        print(usage)
        sys.exit(1)
    try:
        pid = int(sys.argv[1])
    except ValueError:
        print(usage)
        sys.exit(1)

    ipc = pyrasite.PyrasiteIPC(pid, 'ReversePythonShell')
    ipc.connect()

    print("Pyrasite Shell %s" % pyrasite.__version__)
    print("Connected to '%s'" % ipc.title)

    prompt, payload = ipc.recv().split('\n', 1)
    print(payload)

    try:
        import readline
    except ImportError:
        pass

    # py3k compat
    try:
        input_ = raw_input
    except NameError:
        input_ = input

    try:
        while True:
            try:
                input_line = input_(prompt)
            except EOFError:
                input_line = 'exit()'
                print('')
            except KeyboardInterrupt:
                input_line = 'None'
                print('')

            ipc.send(input_line)
            payload = ipc.recv()
            if payload is None:
                break
            prompt, payload = payload.split('\n', 1)
            if payload != '':
                print(payload)
    except:
        print('')
        raise
    finally:
        ipc.close()


if __name__ == '__main__':
    shell()