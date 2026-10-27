import vitis
client = vitis.create_client()
print("HLS/COMP METHODS:", [m for m in dir(client) if 'hls' in m.lower() or 'comp' in m.lower()])
