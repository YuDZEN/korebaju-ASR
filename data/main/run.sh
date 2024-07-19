#!/usr/bin/env bash

# 這段代碼的意義是調用本地的shell腳本，這個腳本的作用是下載數據集
train_cmd="utils/run.pl"
decode_cmd="utils/run.pl"

train=data/train
test=data/test
echo "Data preparation done."
rm -rf exp mfcc # Clean up previous run,可能還要加入其他的
echo "Clean up done."
# Feature extraction
for x in train test; do
 steps/make_mfcc.sh --nj 1 data/$x exp/make_mfcc/$x mfcc
 steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
 utils/fix_data_dir.sh data/$x
done
echo "Feature extraction done."
# Mono training
steps/train_mono.sh --nj 1 --cmd "$train_cmd" \
  --totgauss 400 \
  data/train data/lang exp/mono0a
echo "Mono training done."
# Graph compilation這個是為了生成解碼圖，這個圖是用來解碼的
utils/mkgraph.sh data/lang_test_tg exp/mono0a exp/mono0a/graph_tgpr

echo "Mono training done."


# now we need to train a 3-phone model
echo "Triphone training start."



# Decoding，這是一個測試集，我們暫時沒有，先不用管
#steps/decode.sh --nj 1 --cmd "$decode_cmd" \
#    exp/mono0a/graph_tgpr data/test exp/mono0a/decode_test_yesno
#
#for x in exp/*/decode*; do [ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh; done
