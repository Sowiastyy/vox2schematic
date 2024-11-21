from pyvox.parser import VoxParser
from pyvox.models import get_default_palette
from src.color_matcher import closest_minecraft_block

def handle_vox(args):
    model = VoxParser(args.filename).parse()
    palette = model.palette or get_default_palette()
    length, width, height = model.models[0].size

    blocks = [0] * (width * length * height)

    for z, x, y, c in model.models[0].voxels:
        color = palette[c - 1]
        if args.mode == 'single':
            block_id = args.blockid
        elif args.mode == 'terracotta_wool':
            block_id = closest_minecraft_block(color, terracotta_wool_only=True)
        else:  # all_blocks
            block_id = closest_minecraft_block(color)
        blocks[(y * length + z) * width + x] = block_id

    blocks_ext = [0 for _ in blocks]
    return width, length, height, blocks, blocks_ext
