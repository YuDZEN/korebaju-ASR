import os
import pandas as pd
import torchaudio

# 读取Kaldi数据集的wav.scp和text文件
wav_scp_path = 'data/train/wav.scp'
text_path = 'data/train/text'

# 创建一个元数据DataFrame
data = []

# 读取wav.scp文件
with open(wav_scp_path, 'r') as f:
    wav_lines = f.readlines()

# 读取text文件
with open(text_path, 'r') as f:
    text_lines = f.readlines()

# 创建一个字典保存text文件中的内容
text_dict = {line.split()[0]: ' '.join(line.split()[1:]) for line in text_lines}

# 将wav.scp中的内容和对应的text内容存储到DataFrame中
for line in wav_lines:
    utt_id, wav_path = line.strip().split(maxsplit=1)
    if utt_id in text_dict:
        data.append([utt_id, wav_path, text_dict[utt_id]])

metadata = pd.DataFrame(data, columns=['id', 'path', 'label'])
metadata.to_csv('data/processed/metadata.csv', index=False, sep='|')
