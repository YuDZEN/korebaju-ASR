import torchaudio
import pandas as pd
from datasets import Dataset, Audio

# 加载元数据
metadata = pd.read_csv('data/processed/metadata.csv', delimiter='|')

# 创建Hugging Face数据集
dataset = Dataset.from_pandas(metadata)

# 加载音频文件
def load_audio(batch):
    speech_array, sampling_rate = torchaudio.load(batch['path'])
    batch['speech'] = speech_array.squeeze().numpy()
    batch['sampling_rate'] = sampling_rate
    return batch

dataset = dataset.map(load_audio)

# 打印数据集信息
print(dataset)

# 将数据集保存到磁盘
dataset.save_to_disk('data/processed/whisper_dataset')
