# 2026-10-27T05:01:46.758838600
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="build")
comp.run(operation="C_SIMULATION")

comp.run(operation="SYNTHESIS")

comp.run(operation="CO_SIMULATION")

comp = client.get_component(name="SEQUENTIAL")
comp.run(operation="SYNTHESIS")

