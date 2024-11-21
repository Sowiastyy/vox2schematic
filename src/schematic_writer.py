from nbt.nbt import NBTFile, TAG_Short, TAG_String, TAG_Byte_Array, TAG_List, TAG_Compound
from io import BytesIO

def list_to_byte_array(blockdata):
    return BytesIO(len(blockdata).to_bytes(4, byteorder='big') + bytearray(blockdata))

def write_schematic(args, w, l, h, blocks, data):
    nbtfile = NBTFile()
    nbtfile.name = "Schematic"
    nbtfile.tags.append(TAG_Short(name="Width", value=w))
    nbtfile.tags.append(TAG_Short(name="Length", value=l))
    nbtfile.tags.append(TAG_Short(name="Height", value=h))
    nbtfile.tags.append(TAG_String(name="Materials", value="Alpha"))

    block_ids = []
    block_data = []
    for block in blocks:
        if isinstance(block, str) and ":" in block:
            id_part, data_part = block.split(":")
            block_ids.append(int(id_part))
            block_data.append(int(data_part))
        else:
            block_ids.append(int(block))
            block_data.append(0)

    nbtfile.tags.append(TAG_Byte_Array(name="Blocks", buffer=list_to_byte_array(block_ids)))
    nbtfile.tags.append(TAG_Byte_Array(name="Data", buffer=list_to_byte_array(block_data)))
    nbtfile.tags.append(TAG_List(name="Entities", type=TAG_Compound))
    nbtfile.tags.append(TAG_List(name="TileEntities", type=TAG_Compound))
    nbtfile.write_file(args.output)
