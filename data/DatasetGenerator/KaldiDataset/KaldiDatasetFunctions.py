import os
import shutil

# we make two functions to make our live easier
def check_files_exist(files, directory):
    existing_files = [f for f in files if os.path.exists(os.path.join(directory, f))]
    return existing_files

def move_files_to_directory(files, source_dir, target_dir):
    for file in files:
        shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))

def utt2spk_to_spk2utt(utt2spk_path, spk2utt_path):
    spk_to_utt = {}
    with open(utt2spk_path, 'r', encoding='utf-8') as f:
        for line in f:
            utt_id, spk_id = line.strip().split()
            if spk_id not in spk_to_utt:
                spk_to_utt[spk_id] = []
            spk_to_utt[spk_id].append(utt_id)

    with open(spk2utt_path, 'w', encoding='utf-8') as f:
        for spk_id, utt_ids in spk_to_utt.items():
            f.write(f"{spk_id} {' '.join(utt_ids)}\n")

    print("the file of spk2utt is successfully generated from the file of utt2spk")