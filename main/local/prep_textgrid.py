import os
import argparse
import shutil
import importlib
import subprocess
import sys
check_and_install('textgrid')
import textgrid
from textgrid import TextGrid, IntervalTier

def check_and_install(package):
    """检查并安装指定的包"""
    try:
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def convert_to_textgrid(alignment_file, words_file, output_file):
    """将对齐文件转换为 TextGrid 文件"""
    # 创建 TextGrid 对象
    textgrid = TextGrid()

    # 创建音素和单词的 IntervalTier 对象
    phone_tier = IntervalTier(name='phones')
    word_tier = IntervalTier(name='words')

    # 读取音素对齐信息
    with open(alignment_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            start_time = float(parts[0]) / 100.0  # 转换为秒
            end_time = float(parts[1]) / 100.0    # 转换为秒
            phone = parts[2]
            phone_tier.addInterval(start_time, end_time, phone)

    # 读取单词对齐信息
    if words_file:
        with open(words_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                start_time = float(parts[0]) / 100.0  # 转换为秒
                end_time = float(parts[1]) / 100.0    # 转换为秒
                word = parts[2]
                word_tier.addInterval(start_time, end_time, word)
    
    # 将 IntervalTier 添加到 TextGrid
    textgrid.appendTier(phone_tier)
    textgrid.appendTier(word_tier)

    # 保存 TextGrid 文件
    textgrid.save(output_file)
    print(f"TextGrid file saved to {output_file}")

def process_batch(alignments_dir, words_file, output_dir):
    """批量处理对齐文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(alignments_dir):
        if filename.endswith('.gz'):
            alignment_file = os.path.join(alignments_dir, filename)
            output_file = os.path.join(output_dir, filename.replace('.gz', '.TextGrid'))
            
            convert_to_textgrid(alignment_file, words_file, output_file)

# 设置路径
alignments_dir = 'decode/ali'  # 对齐文件的目录
words_file = 'decode/tmp/words.txt'  # 单词对齐信息文件路径
output_dir = 'decode/textgrid'  # 输出目录

# 批量处理对齐文件
process_batch(alignments_dir, words_file, output_dir)
