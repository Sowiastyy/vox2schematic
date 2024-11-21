import os
from subprocess import run

# Folder testowy
TEST_FOLDER = "tests"

# Zakładamy, że istnieją dwa pliki VOX w folderze `tests`
vox_files = [
    os.path.join(TEST_FOLDER, "test1.vox"),
    os.path.join(TEST_FOLDER, "test2.vox")
]

# Ustawienia dla plików schematów
schematic_settings = [
    {"mode": "single", "blockid": 1},  # Single block mode (stone)
    {"mode": "single", "blockid": 4},  # Single block mode (cobblestone)
    {"mode": "terracotta_wool"},       # Terracotta and wool only
    {"mode": "all"},                   # All blocks
    {"mode": "single", "blockid": 57}, # Single block mode (diamond block)
]

# Tworzenie schematów dla każdego pliku VOX
for vox_file in vox_files:
    if not os.path.exists(vox_file):
        print(f"File not found: {vox_file}. Please ensure it exists in the '{TEST_FOLDER}' folder.")
        continue

    for i, settings in enumerate(schematic_settings, start=1):
        # Nazwa wyjściowego pliku .schematic
        schematic_filename = os.path.join(TEST_FOLDER, f"{os.path.splitext(os.path.basename(vox_file))[0]}_variant{i}.schematic")

        # Budowanie komendy dla vox2schematic
        command = [
            "python", "vox2schematic.py", vox_file,
            "--output", schematic_filename,
            "--mode", settings["mode"]
        ]

        if "blockid" in settings:
            command.extend(["--blockid", str(settings["blockid"])])

        # Uruchamianie konwersji
        print(f"Running: {' '.join(command)}")
        run(command)

print(f"Schematic files generated in the '{TEST_FOLDER}' folder.")
