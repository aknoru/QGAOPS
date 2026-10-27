# 2026-10-27T04:20:47.486884800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="PARALLEL")
comp.run(operation="SYNTHESIS")

comp = client.get_component(name="SEQUENTIAL")
comp.run(operation="SYNTHESIS")

vitis.dispose()

vitis.dispose()

