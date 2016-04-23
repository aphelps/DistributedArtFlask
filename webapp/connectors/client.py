from hmtl.client import HMTLClient

server_client = None

def create_client(address):
    global server_client
    if server_client is not None:
        print("* Client already created ")
        return server_client

    print("* Creating HMTL Client.  address=%s" % address)

    try:
        server_client = HMTLClient(address=address, verbose=True)
        return server_client
    except Exception as e:
        print("ERROR: Failed to create client: %s" % e)
        return None