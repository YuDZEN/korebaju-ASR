# Corpus Directory Guideline

Here you put your raw data. The data for the trainning is in ```data_source``` and for the test in ```test_source```.

You should put your audio file and annotation (we only accept textgrid annotation) following the example in this directory. 

You MUST check the tier of annatation used for the trainnning. In the example, we used the 7th tier, if your annotation is on an other tier, please check the script ```local/KaldiTrainDataset``` and ```local/KaldiTestDataset``` and modify the line below according to your own case. 

``` word_tier = tg[7]  # Assuming the 8th tier is for words``` 


To be clear, if your annotation is on the 1st tier, you should write  ```word_tier = tg[0]``` because in Praat, the tier begins from 1 but here in the code, it begins from 0 (quite normal in most informatic tools)

You have nothing else to do because our scripts can automatically treat the raw data. 

You should put your the list of your vocabulary in the file list.txt as shown by the existing example.