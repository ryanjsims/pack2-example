from DbgPack import AssetManager
from glob import glob
from pathlib import Path

test_server = r"/mnt/c/Users/Public/Daybreak Game Company/Installed Games/PlanetSide 2 Test/Resources/Assets"
manager = AssetManager([Path(p) for p in glob(test_server + "/*.pack2")])
for key in manager:
    if key.name.endswith(".dme"):
        print(key.name)

##To export model:
#f = open("Weapon_TR_MaxAntiVehicleRight001_Lod0_LODAuto.dme", "wb")
#f.write(manager["Weapon_TR_MaxAntiVehicleRight001_Lod0_LODAuto.dme"].get_data())
#f.close()
