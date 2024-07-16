import unicodedata

# 需要保留的组合字符名称
keep_combining_names = [
    'COMBINING TILDE',  # 鼻音符号
    'COMBINING DOUBLE INVERTED BREVE',  # 喉塞音符号
    'MODIFIER LETTER SMALL H',  # ʰ
    'MODIFIER LETTER SMALL REVERSED GLOTTAL STOP',  # ˀ
    'COMBINING DIAERESIS'  # ̈（用于ɨ̂等）
]

def remove_unwanted_characters(text):
    normalized_text = unicodedata.normalize('NFD', text)  # 将文本规范化为 NFD 形式
    stripped_text = ''.join(c for c in normalized_text if not unicodedata.combining(c) or unicodedata.name(c) in keep_combining_names)  # 去除组合字符

    # 删除冒号和连字符
    stripped_text = stripped_text.replace(':', '').replace('-', '')

    return stripped_text

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin:
        examples = fin.readlines()

    transformed_examples = []

    for example in examples:
        parts = example.strip().split()
        transformed_parts = []

        for part in parts:
            normalized_part = remove_unwanted_characters(part)
            transformed_parts.append(normalized_part)

        transformed_example = " ".join(transformed_parts)
        transformed_examples.append(transformed_example)

    with open(output_file, 'w', encoding='utf-8') as fout:
        for transformed_example in transformed_examples:
            fout.write(transformed_example + '\n')

    print(f"Processed {len(transformed_examples)} examples. Output saved to {output_file}")
def main():
    input_file = '../../main/data/lang/dict/list.txt'  # 输入文件路径
    output_file = '../../main/data/lang/dict/tmp.txt'  # 输出文件路径
    process_file(input_file, output_file)
