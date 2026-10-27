import vitis, inspect
client = vitis.create_client()
print("has create_hls_component:", hasattr(client, 'create_hls_component'))
for attr in dir(client):
    if 'hls' in attr.lower():
        print("attr:", attr)
