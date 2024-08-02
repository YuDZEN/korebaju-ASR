# This file contains functions that are used in the KaldiTrainDataset.py and KaldiTestDataset.py


import os
import shutil
import importlib
import subprocess
import sys

def check_and_install(package):
    try:
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# we make two functions to make our live easier
def check_files_exist(files, directory):
    existing_files = [f for f in files if os.path.exists(os.path.join(directory, f))]
    return existing_files

def move_files_to_directory(files, source_dir, target_dir):
    for file in files:
        shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))


def remove_duplicate_lines(input_file, output_file):
    # we use a set because a set can only store unique elements!
    unique_lines = set()

    # 读取文件并将每一行加入集合
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            unique_lines.add(line)

    # 将集合中的行写回到输出文件中
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in unique_lines:
            file.write(line)