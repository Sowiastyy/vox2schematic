from PIL import Image

def handle_png(args):
    model = Image.open(args.filename)
    sizex, sizey = model.size
    blocks = []

    for y in range(sizey):
        for x in range(sizex):
            rgb = model.getpixel((x, y))
            if rgb[3] != 0:
                blocks.append(args.blockid)
            else:
                blocks.append(0)

    blocks = list(reversed(blocks))
    blocks_ext = [0 for _ in blocks]
    width, length, height = args.dimensions
    return width, length, height, blocks, blocks_ext
