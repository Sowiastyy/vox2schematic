from argparse import ArgumentParser
from os import path, makedirs
from src.handlers.png_handler import handle_png
from src.handlers.vox_handler import handle_vox
from src.schematic_writer import write_schematic

# Obsługiwane formaty plików
SUPPORTED_FORMATS = ['png', 'vox']

def init_parser():
    parser = ArgumentParser(description='Converts various voxel formats to Minecraft .schematic files')
    parser.add_argument('filename', help='File to convert')
    parser.add_argument('-o', '--output', help='Filename of the resulting file, defaults to input filename with .schematic extension')
    parser.add_argument('-d', '--dimensions', help='Dimensions for PNG format: width length height', nargs=3, type=int, metavar=('WIDTH', 'LENGTH', 'HEIGHT'))
    parser.add_argument('-b', '--blockid', help='Block ID for single block mode', type=int, default=1)
    parser.add_argument('--mode', help='Conversion mode: single block, terracotta_wool, all_blocks', choices=['single', 'terracotta_wool', 'all'], default='all')
    return parser

def detect_format(filename):
    """Wykryj format pliku na podstawie rozszerzenia"""
    extension = path.splitext(filename)[1].lower().strip('.')
    if extension in SUPPORTED_FORMATS:
        return extension
    raise ValueError(f"Unsupported file format: .{extension}. Supported formats are: {', '.join(SUPPORTED_FORMATS)}")

def ensure_output_path(output_path):
    """Utwórz folder dla pliku wyjściowego, jeśli nie istnieje"""
    output_dir = path.dirname(output_path)
    if output_dir and not path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        makedirs(output_dir)

def main():
    parser = init_parser()
    args = parser.parse_args()

    # Wykryj format pliku
    file_format = detect_format(args.filename)

    # Domyślny plik wyjściowy, jeśli nie podano --output
    if not args.output:
        args.output = f"{path.splitext(args.filename)[0]}.schematic"

    # Upewnij się, że ścieżka wyjściowa istnieje
    ensure_output_path(args.output)

    # Obsługa plików na podstawie formatu
    if file_format == 'png':
        if not args.dimensions:
            raise ValueError("For PNG files, you must specify dimensions using --dimensions")
        w, l, h, blocks, data = handle_png(args)
    elif file_format == 'vox':
        w, l, h, blocks, data = handle_vox(args)
    else:
        raise ValueError(f"Unsupported format: {file_format}")

    # Zapis do pliku wyjściowego
    print(f"Saving schematic to: {args.output}")
    write_schematic(args, w, l, h, blocks, data)

if __name__ == "__main__":
    main()
