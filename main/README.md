## User Guide
We highly recommand you to use a Unix-like system (we used wsl-Ubuntu system) because it is much easier to use for a kaldi project than on any windows sysytem.

 To train your own model for korebaju langauge, you have to first install kaldi on your own PC. To install kaldi, please check the document in ```https://github.com/kaldi-asr/kaldi```

To train your own model, you only need to modifier ```corpus/data_source``` (where your put your audio file and annotation for the trainning of the model) and ```corpus/test_source``` (where your put your audio file and annotation for the test of the model) and ```corpus/list.txt``` (a list of all words that can occur in your corpus) by adding your own dataset (please refer the example already exsiting in these repertories). Please make sure that your annotation respect the the same rule as manifested by the example presenting in the ```corpus/data_source/COE_14```
if you want to change the annotation structure, it is of course possible, however you also need to change the coresponding python code in ```local```. To be able to change it correctly, you have better read the kaldi document in ```https://kaldi-asr.org/``` and understand how kaldi works (especially the data preparing)

After this, you need to check the language model. We used kenlm to produce a language model, we use a python script to create the corpus for the language model and the corpus based on in fact the ```corpus/list.txt``` by adding the word into the carrier phrase. You can of course make your own language model, however you should make your own corpus to train the language model. You can refer to the github project ```https://github.com/kpu/kenlm``` 

Before the last step, you should create 2 links by the following commands:
```
ln -s $KALDI_ROOT/egs/wsj/s5/steps steps
ln -s $KALDI_ROOT/egs/wsj/s5/utils utils
```

Now, you can run the main scripts ```../main/run.sh```, we choosed a classical HMM-GMM model for our project. you can also test other deep-learning method such as HMM-DNN but it needs a good GPU performance (generally hard to run on a normal PC). You need to change the run.sh in order to use other method (we recommand to read the example in kaldi project to understant how to change run.sh). 

please get into ../main and run the scrit "run.sh" by 
```
./run.sh
```
The trainning process will start, it can some minuits (depending on the size of your dataset). If everthing runs correctly, we can get the output file in ```../main/exp```.