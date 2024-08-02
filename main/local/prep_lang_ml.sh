#!/bin/bash

rm -rf lang_ml
mkdir lang_ml


python3 local/n_gram_corpus_preparation.py || { echo "Python script n_gram_corpus_preparation.py failed"; exit 1; }

if [ ! -f lang_ml/ngramcorpus.txt ]; then
    echo "File lang_ml/ngramcorpus.txt not found!"
    exit 1
fi

./local/kenlm/build/bin/lmplz --verbose_header --discount_fallback -o 3 < lang_ml/ngramcorpus.txt > lang_ml/model.arpa || { echo "lmplz failed"; exit 1; }
$KALDI_ROOT/src/lmbin/arpa2fst --disambig-symbol=#0 --read-symbol-table=data/lang/words.txt lang_ml/model.arpa lang_ml/G.fst || { echo "arpa2fst failed"; exit 1; }
cp lang_ml/G.fst data/lang/G.fst
