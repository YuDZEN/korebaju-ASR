#!/bin/bash
# Set up Kaldi environment
. ./path.sh
# Check if Kaldi path is set correctly
if [ ! -d "$KALDI_ROOT" ]; then
  echo "Please set the KALDI_ROOT variable to the root of your Kaldi installation."
  exit 1
fi

# prepare dataset and lexicon
./local/prep_tranning_corpus.sh
python3 main/local/prep_lexicon.py
find ./data/lang -type f -exec dos2unix {} \;


# Define directories
train_dir=./data/train
test_dir=./data/test
lang_dir=./data/lang
dict_dir=./data/lang/dict
exp_dir=./exp/
# Create export directory if it does not exist
if [ ! -d "$exp_dir" ]; then
  mkdir -p $exp_dir
fi

# Ensure necessary directories exist
for dir in $train_dir $test_dir $lang_dir $dict_dir; do
  if [ ! -d "$dir" ]; then
    echo "Directory $dir does not exist!"
    exit 1
  fi
done




# Step 1: Prepare language data and features
echo "Preparing language data and features..."
utils/prepare_lang.sh $dict_dir "<UNK>" $lang_dir/local/lang $lang_dir || exit 1
# Step 2: Extract features for train and test data  
echo "Extracting features for train and test data..."
steps/make_mfcc.sh --nj 4 --cmd "run.pl" $train_dir || exit 1
# 暫時還沒有test,之後要加上，解除注釋
# steps/make_mfcc.sh --nj 4 --cmd "run.pl" $test_dir || exit 1
steps/compute_cmvn_stats.sh $train_dir || exit 1
# 暫時還沒有test,之後要加上，解除注釋
# steps/compute_cmvn_stats.sh $test_dir || exit 1

# Step 3: Monophone training
echo "Training monophone model..."
steps/train_mono.sh --nj 1 --cmd "run.pl" $train_dir $lang_dir $exp_dir/mono || exit 1

# Step 4: Align monophone model
echo "Aligning monophone model..."
steps/align_si.sh --nj 1 --cmd "run.pl" $train_dir $lang_dir $exp_dir/mono $exp_dir/mono_ali || exit 1

# Step 5: Triphone training
echo "Training triphone model..."
steps/train_deltas.sh --cmd "run.pl" 2000 10000 $train_dir $lang_dir $exp_dir/mono_ali $exp_dir/tri1 || exit 1

# Step 6: Align triphone model
echo "Aligning triphone model..."
steps/align_si.sh --nj 1 --cmd "run.pl" $train_dir $lang_dir $exp_dir/tri1 $exp_dir/tri1_ali || exit 1

# Step 7: Prepare n-gram language model and generate graph
./local/prep_lang_ml.sh
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1

# Step 7: Decode test data
# echo "Decoding test data..."
# utils/mkgraph.sh $lang_dir $exp_dir/tri1 $exp_dir/tri1/graph || exit 1
# steps/decode.sh --nj 4 --cmd "run.pl" $exp_dir/tri1/graph $test_dir $exp_dir/tri1/decode_test || exit 1

# Step 8: Get the results
# echo "Getting results..."
# grep WER $exp_dir/tri1/decode_test/wer_* | utils/best_wer.sh

echo "All steps completed successfully!"
