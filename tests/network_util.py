import socket
from time import time as now


def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


# code.activestate.com/recipes/576655-wait-for-network-service-to-appear
def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    s = socket.socket()
    # Following line prevents this method from interfering with process
    # it is waiting for on localhost.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if timeout:
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error:
            pass
        else:
            s.close()
            return True
