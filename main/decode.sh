#!/bin/bash

set -e

# define directories
data_dir="decode/data"
output_dir="decode/tmp"
ali_output_dir="decode/ali"
textgrid_output_dir="decode/textgrid"
nj=1  # the number of parallel jobs, set to 1 for simplicity, you can change it according to your CPU cores and memory
cmd="run.pl"

mkdir $output_dir
mkdir $ali_output_dir
mkdir $textgrid_output_dir

# 创建必要的目录
mkdir -p $output_dir
find decode/ -type f -name "*.wav" | awk -F'/' '{print $NF}' | sed 's/.wav//' | awk '{print $1" decode/"$1".wav"}' > decode/wav.scp

# 检查必要的文件是否存在
if [ ! -f $data_dir/wav.scp ]; then
  echo "Error: $data_dir/wav.scp not found."
  exit 1
fi

# 创建 utt2spk 和 spk2utt 文件
awk '{print $1" "$1}' $data_dir/wav.scp > $data_dir/utt2spk
utils/utt2spk_to_spk2utt.pl < $data_dir/utt2spk > $data_dir/spk2utt

# 提取MFCC特征
steps/make_mfcc.sh --nj $nj --cmd "$cmd" $data_dir $data_dir $data_dir/mfcc
steps/compute_cmvn_stats.sh $data_dir $data_dir $data_dir/mfcc

# 解码
steps/decode.sh --nj $nj --cmd "$cmd" exp/tri1/graph $data_dir $output_dir
echo "Decoding finished. Results are in $output_dir"
steps/align_fmllr.sh --nj 4 --cmd "$cmd" decode data/lang exp/tri1 $ali_output_dir

echo "Converting result to TextGrid format..."
python3 local/prep_textgrid.py || exit 1

echo "TextGrid files are successfully generated in decode/textgrid"
