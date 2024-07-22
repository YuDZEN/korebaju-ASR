import os

input_file = '../../main/data/lang/dict/list.txt'  # 输入文件路径
output_file = '../../main/data/lang/dict/ngramcorpus.txt'  # 输出文件路径

# 读取输入文件内容
with open(input_file, 'r', encoding='utf-8') as file:
    list_lines = file.readlines()

# 处理每一行并写入输出文件
with open(output_file, 'w', encoding='utf-8') as file:
    for line in list_lines:
        # 去除每行首尾的空白字符（包括换行符）
        variable_word = line.strip()

        # 生成句子
        sentence_with_variable = f"cɨ̀kɨ́nà ìká-mè {variable_word} kòrèbàhɨ́ t͡ʃɨ́òpí\n"

        # 打印生成的句子（可选）
        print(sentence_with_variable)

        # 写入到输出文件
        file.write(sentence_with_variable)

input_file = output_file
output_file = '../../main/language_model/ngramcorpus.txt'

with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

unique_lines = list(set(lines))

with open(output_file, 'w', encoding='utf-8') as file:
    file.writelines(unique_lines)

os.remove(input_file)
print("Done!")

