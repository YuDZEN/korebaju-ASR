#!/bin/bash
echo "Cleanup is beginning."
# 删除 data/lang/local 文件夹及其内容
rm -rf data/lang/local/*
# 删除 data/lang/phone 文件夹及其内容
rm -rf data/lang/phone/*
# 删除 data/lang/dict/lexiconp.txt 文件
rm -f data/lang/dict/lexiconp.txt
# 删除 data/lang/L.fst 文件
rm -f data/lang/L.fst
rm -f data/lang/G.fst
rm -f data/lang/L_disambig.fst
rm -f data/lang/oov.int
rm -f data/lang/oov.txt
rm -rf data/lang/phones
rm -f data/lang/words.txt
rm -f data/lang/topo
rm -rf data/test/log
rm -rf exp/
# 刪除 data/train 目錄下的大部分文件
rm -rf data/train/utt2dur
rm -rf data/train/utt2num_frames
rm -rf data/train/frame_shift
rm -rf data/train/feats.scp
rm -rf data/train/cmvn.scp
rm -rf data/train/split1
rm -rf data/train/log
rm -rf data/train/data
rm -rf data/train/.backup
rm -rf data/train/conf
echo "Cleanup complete."

# 在這裏要調用 KaldiTrainDataset.py以及KaldiTestDataset.py
echo "Preparing Train data and Test data..."
python3 local/KaldiTrainDataset.py
python3 local/KaldiTestDataset.py

# utt2spk 文件在 data/train/utt2spk，來生成 spk2utt 文件
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
# 生成新的 utt2spk 文件
utils/spk2utt_to_utt2spk.pl data/train/spk2utt > data/train/utt2spk.new
# 替换原来的 utt2spk 文件
mv data/train/utt2spk.new data/train/utt2spk
# 验证数据目录
utils/validate_data_dir.sh data/train

echo "Train data and Test data completed."