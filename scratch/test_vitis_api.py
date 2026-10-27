import vitis

client = vitis.create_client()
print("CLIENT METHODS:", [m for m in dir(client) if not m.startswith('_')])
