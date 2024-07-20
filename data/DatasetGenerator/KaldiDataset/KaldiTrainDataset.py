import os
import shutil
from glob import glob
# pip install textgrid if not installed
from textgrid import TextGrid
from KaldiDatasetFunctions import check_files_exist, move_files_to_directory, utt2spk_to_spk2utt
import time

start= time.time()
# make two variables to store the input and output directories
output_dir = "../../main/data/train"
input_dir = "../../data_source"
os.makedirs(output_dir, exist_ok=True) # create the output directory if it does not exist

# Not all of the files are equally important. For a simple setup where there is no "segmentation" information (i.e. each utterance corresponds to a single file), the only files you have to create yourself are "utt2spk", "text" and "wav.scp" and possibly "segments" and "reco2file_and_channel", and the rest will be created by standard scripts.
# path setting here, this is the files in data/train
wav_scp_path = os.path.join(output_dir, "wav.scp") # make a object to store the information for the moment (not stored in the file yet)
text_path = os.path.join(output_dir, "text") # idem
utt2spk_path = os.path.join(output_dir, "utt2spk") # idem
segments_path = os.path.join(output_dir, "segments") # idem


# 定义要检查的文件
files_to_check = ["wav.scp", "text", "utt2spk", "segments"]
existing_files = check_files_exist(files_to_check, output_dir)

# 如果存在任何文件，则处理
if existing_files:
    tmp_dir = os.path.join(output_dir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)  # 创建tmp目录，如果已存在则忽略
    move_files_to_directory(existing_files, output_dir, tmp_dir)


# Iterate over all files in input_dir and its subdirectories to process each wav file + corresponding TextGrid file
for root, dirs, files in os.walk(input_dir):
    wav_files = glob(os.path.join(root, '*.wav'))
    for wav_file in wav_files:
        base_name = os.path.splitext(os.path.basename(wav_file))[0][:-4]#删除了.wav后缀的文件名
        recording_id = base_name
        print("Processing " + base_name + ".wav")
        textgrid_file = os.path.join(root, base_name + '.TextGrid')
        print("the corresponding textgrid file should be: ", textgrid_file)
        speaker_id = base_name[0:-2]  # Adjust based on your naming convention
        print("speaker_id = " + speaker_id)

        if os.path.exists(textgrid_file):
            relative_wav_file = os.path.relpath(wav_file, output_dir)
            relative_wav_file = relative_wav_file.replace('\\', '/')  # Replace backslashes with forward slashes
            # Initialize content strings
            wav_scp_content = f"{recording_id} {relative_wav_file}\n" # <recording-id> <extended-filename>
            text_content = ""
            segments_content = ""
            utt2spk_content = ""

            # Load TextGrid file and extract word information
            tg = TextGrid.fromFile(textgrid_file)
            word_tier = tg[7]  # Assuming the 8th tier is for words
            utternance_number = 1
            for interval in word_tier:
                if interval.mark:  # Ensure the mark is not empty
                    start_time = interval.minTime
                    end_time = interval.maxTime
                    word = interval.mark
                    # utternance_id = base_name + str(utternance_number)
                    utternance_id = base_name + str(utternance_number).zfill(3)  # Convert to three digits
                    text_content += f"{utternance_id} {word}\n"
                    segments_content += f"{utternance_id} {recording_id} {start_time:.3f} {end_time:.3f}\n" # <utterance-id> <recording-id> <segment-begin> <segment-end>
                    utternance_number += 1
                    utt2spk_content += f"{utternance_id} {speaker_id}\n"

            # Append to files


            with open(wav_scp_path, 'a', encoding='utf-8') as f:
                f.write(wav_scp_content)

            with open(text_path, 'a', encoding='utf-8') as f:
                 f.write(text_content)

            with open(segments_path, 'a', encoding='utf-8') as f:
                f.write(segments_content)

            with open(utt2spk_path, 'a', encoding='utf-8') as f:
                f.write(utt2spk_content)
        else: print("no corresponding textgrid file found for " + base_name)
# Generate spk2utt file
utt2spk_to_spk2utt("../../main/data/train/utt2spk", "../../main/data/train/spk2utt")
print("Data preparation completed successfully!")

# 脚本执行完毕的时间戳
end = time.time()
print('cost %f second' % (end - start))