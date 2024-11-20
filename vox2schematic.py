from PIL import Image
from nbt.nbt import *
from io import BytesIO
from os import path
from argparse import ArgumentParser
from pyvox.parser import VoxParser
from pyvox.models import get_default_palette

formats = ['png', 'vox']

# prepend data with 4 bytes of data length and wrap it around BytesIO stream
# to be usable with NBT library in TAG_Byte_Array constructor as buffer parameter
def list_to_byte_array(blockdata):
	return BytesIO(len(blockdata).to_bytes(4, byteorder='big') + bytearray(blockdata))

def init_parser():
	parser = ArgumentParser(description='Converts various voxel formats to minecraft .schematic files')
	parser.add_argument('filename', help='File to convert')
	parser.add_argument('-o', '--output', help='Filename of the resulting file, defaults to filename.schematic')
	parser.add_argument('-f', '--format', help='Input file format, possible values are "png" for 2d PNG slice (requires dimensions to be specified with -d) and "vox". Redundant if file has a valid extension', choices=formats)
	parser.add_argument('-d', '--dimensions', help='Dimensions specified as "width length height" (You can just copy-paste it from MagicaVoxel)', nargs=3, type=int, metavar=('WIDTH', 'LENGTH', 'HEIGHT'))
	parser.add_argument('-b', '--blockid', help='Block id to use when converting to .schematic, defaults to 1 (stone)', type=int, default=1)
	return parser

def parse_args(parser):
	args = parser.parse_args()
	
	# deduce format from filename
	if args.format is None:
		extension = path.splitext(path.basename(args.filename))[1]
		if len(extension) > 0:
			# get rid of the dot in the extension
			extension = extension[1:]
			if extension in formats:
				args.format = extension
			else:
				parser.error('Wrong input file extension. Change your input file extension or specify format explicitly with -f')
		else:
			parser.error('Could not deduce format from filename because file extension is missing. Specify extension explicitly with -f')
			
	# force specifying dimensions for png format
	if args.format == 'png' and args.dimensions is None:
		parser.error('PNG format requires dimensions to be specified with -d')
		
	# deduce output filename from input filename
	if args.output is None:
		args.output = "{filename}.schematic".format(filename=path.splitext(path.basename(args.filename))[0])
	return args
	
def png_handler(args):
	model = Image.open(args.filename)
	sizex, sizey = model.size
	blocks = []
	for y in range(0, sizey):
		for x in range(0, sizex):
			rgb = model.getpixel((x, y))
			if rgb[3] != 0:
				blocks.append(args.blockid)
			else:
				blocks.append(0)

	blocks = list(reversed(blocks))
	blocks_ext = [0 for i in range(0, len(blocks))]
	width, length, height = args.dimensions
	return (width, length, height, blocks, blocks_ext)
MINECRAFT_BLOCKS = {
	(152, 94, 67)"172"
    (8, 10, 15): "251:15",
    (25, 27, 32): "252:15",
    (37, 23, 16): "159:15",
    (21, 21, 26): "35:15",
    (45, 47, 143): "251:11",
    (70, 73, 167): "252:11",
    (74, 60, 91): "159:11",
    (53, 57, 157): "35:11",
    (96, 60, 32): "251:12",
    (126, 85, 54): "252:12",
    (77, 51, 36): "159:12",
    (114, 72, 41): "35:12",
    (21, 119, 136): "251:9",
    (37, 148, 157): "252:9",
    (87, 91, 91): "159:9",
    (21, 138, 145): "35:9",
    (55, 58, 62): "251:7",
    (77, 81, 85): "252:7",
    (58, 42, 36): "159:7",
    (63, 68, 72): "35:7",
    (73, 91, 36): "251:13",
    (97, 119, 45): "252:13",
    (76, 83, 42): "159:13",
    (85, 110, 27): "35:13",
    (36, 137, 199): "251:3",
    (74, 181, 214): "252:3",
    (114, 109, 138): "159:3",
    (58, 175, 217): "35:3",
    (125, 125, 115): "251:7",
    (155, 155, 148): "252:7",
    (135, 107, 98): "159:7",
    (142, 142, 135): "35:7",
    (94, 169, 25): "251:5",
    (126, 189, 42): "252:5",
    (103, 118, 53): "159:5",
    (112, 185, 26): "35:5",
    (169, 48, 159): "251:2",
    (193, 84, 185): "252:2",
    (150, 88, 109): "159:2",
    (189, 69, 180): "35:2",
    (224, 97, 1): "251:1",
    (227, 132, 32): "252:1",
    (162, 84, 38): "159:1",
    (241, 118, 20): "35:1",
    (214, 101, 143): "251:6",
    (229, 154, 181): "252:6",
    (162, 78, 79): "159:6",
    (238, 141, 173): "35:6",
    (100, 32, 156): "251:10",
    (132, 56, 178): "252:10",
    (118, 70, 86): "159:10",
    (122, 42, 173): "35:10",
    (142, 33, 33): "251:14",
    (168, 54, 51): "252:14",
    (143, 61, 47): "159:14",
    (161, 39, 35): "35:14",
    (207, 213, 214): "251:0",
    (226, 228, 228): "252:0",
    (210, 178, 161): "159:0",
    (234, 236, 237): "35:0",
    (241, 175, 21): "251:4",
    (233, 199, 55): "252:4",
    (186, 133, 35): "159:4",
    (249, 198, 40): "35:4",
}

def closest_minecraft_block(color):
	"""Znajdź najbliższy kolor Minecraft dla danego koloru."""
	r, g, b = color[:3]  # Ignorujemy wartość alfa
	closest_block = None
	min_distance = float('inf')

	for mc_color, block_id in MINECRAFT_BLOCKS.items():
		mc_r, mc_g, mc_b = mc_color
		distance = (r - mc_r) ** 2 + (g - mc_g) ** 2 + (b - mc_b) ** 2
		if distance < min_distance:
			min_distance = distance
			closest_block = block_id

	return closest_block

def vox_handler(args):
	model = VoxParser(args.filename).parse()
	palette = model.palette or get_default_palette()
	length, width, height = model.models[0].size

	blocks = [0]*(width*length*height)
		
	for z, x, y, c in model.models[0].voxels:
		color = palette[c-1]
		block_id = closest_minecraft_block(color) or args.blockid
		blocks[(y*length + z)*width + x] = block_id
	
	blocks_ext = [0 for i in range(0, len(blocks))]
	return (width, length, height, blocks, blocks_ext)

def write_schematic(args, w, l, h, blocks, data):
    nbtfile = NBTFile()
    nbtfile.name = "Schematic"
    nbtfile.tags.append(TAG_Short(name="Width", value=w))
    nbtfile.tags.append(TAG_Short(name="Length", value=l))
    nbtfile.tags.append(TAG_Short(name="Height", value=h))
    nbtfile.tags.append(TAG_String(name="Materials", value="Alpha"))

    # Rozdzielanie "X:Y" na ID bloku i dane
    block_ids = []
    block_data = []
    for block in blocks:
        if isinstance(block, str) and ":" in block:
            id_part, data_part = block.split(":")
            block_ids.append(int(id_part))
            block_data.append(int(data_part))
        else:
            block_ids.append(int(block))  # Bez ":", traktujemy jako ID
            block_data.append(0)  # Domyślna wartość dla danych

    # Dodanie ID bloku i danych do pliku NBT
    nbtfile.tags.append(TAG_Byte_Array(name="Blocks", buffer=list_to_byte_array(block_ids)))
    nbtfile.tags.append(TAG_Byte_Array(name="Data", buffer=list_to_byte_array(block_data)))
    nbtfile.tags.append(TAG_List(name="Entities", type=TAG_Compound))
    nbtfile.tags.append(TAG_List(name="TileEntities", type=TAG_Compound))
    nbtfile.write_file(args.output)





handlers = {'png': png_handler, 'vox': vox_handler}

def main():
	parser = init_parser()
	args = parse_args(parser)
	
	w, l, h, blocks, data = handlers[args.format](args)
	write_schematic(args, w, l, h, blocks, data)

if __name__ == "__main__":
	main()
