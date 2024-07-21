# This repertory contains the local data/script used for the project

## For the moment we don't have any local script, in fact we consider to intergrate our python script in DatasetGenerator into this repertory, but it will be the last job to do (since it is not so important to our model performance)

## 現在的重要問題是，每次訓練后我們需要去清理以前的目錄（data/train； data/test）這是不方便的，我們需要重新創一個文件夾比如早我們的local文件夾裏，或者另外創一個文件夾。

## 我目前的想法是，把我們data_generater的整合進我們的local文件夾，然後再在local文件夾做一個korebaju_data_prepare.sh,整合這幾個的功能，這樣每次運行run.sh就可以了。

## 然後就是每次刪除data/train; data/test; data/lang這些文件（先於生成的過程）。然後再重新生成這些文件夾。

## 目前這個聲學模型就算生成好了，之後要收集更多的數據，用同樣方法生成，此外就是要稍微注釋一部分的textgrid(因爲carrier phrase沒有包括在内)， 我們要看情況，很有可能我們必須訓練一個語言模型（這裏我們用n-gramm就可以，簡單，資源占用少）。但是目前我們要嘗試使用當前的聲學模型來完成任務，這是最簡便的，當然也最好看看怎麽在mfa使用我們的模型（最差重新訓練一個mfa模型）

## 最後就是我們還沒有test集，這個只能等到之後我們有更多數據再説