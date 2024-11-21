from src.minecraft_blocks import MINECRAFT_BLOCKS

def closest_minecraft_block(color, terracotta_wool_only=False):
    r, g, b = color[:3]
    closest_block = None
    min_distance = float('inf')

    for mc_color, block_id in MINECRAFT_BLOCKS.items():
        if terracotta_wool_only and not block_id.startswith(("159", "35", "251")):
            continue

        mc_r, mc_g, mc_b = mc_color
        distance = (r - mc_r) ** 2 + (g - mc_g) ** 2 + (b - mc_b) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_block = block_id

    return closest_block
