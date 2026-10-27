# 2026-10-27T05:18:18.415165100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="SEQUENTIAL")
comp.run(operation="C_SIMULATION")

comp.run(operation="SYNTHESIS")

comp.run(operation="CO_SIMULATION")

comp.run(operation="PACKAGE")

comp.run(operation="IMPLEMENTATION")

comp.run(operation="IMPLEMENTATION")

comp = client.get_component(name="PARALLEL")
comp.run(operation="IMPLEMENTATION")

vitis.dispose()

