import os
import re
import unicodedata
import prep_inter_lexicon
def load_phones(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        phones = file.read().splitlines()
    print("Loaded", len(phones), "phones from", file_path)
    return phones

def split_phonemes(line, phones):
    phonemes = []
    i = 0
    while i < len(line):
        match = None
        for phone in phones:
            if line[i:i+len(phone)] == phone:
                match = phone
                break
        if match:
            phonemes.append(match)
            i += len(match)
        else:
            if ord(line[i]) == 771:# 771 is the code for the tilde character, we must consider it as a nasal(we don't want to give a fuck about the small point like : or ', even ˀ)
                phonemes[len(phonemes)-1] = phonemes[len(phonemes)-1] + line[i]
            else:
                print(phonemes)
                print("Error: No match found for ", line[i] + " of " + line + " at position " + "of " +(str)(len(phonemes)) + " at position " + (str)(len(phonemes)))
            i += 1
    return ' '.join(phonemes)

prep_inter_lexicon.main()
phones = load_phones('../../main/data/lang/dict/nonsilence_phones.txt')
# input file2
with open('../../main/data/lang/dict/tmp.txt', 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()
processed_lines = [split_phonemes(line, phones) for line in lines]
# write the file
with open('../../main/data/lang/dict/lexicon_tmp.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(processed_lines))

# Step 1: Read lines from list.txt
with open('../../main/data/lang/dict/list.txt', 'r', encoding='utf-8') as file:
    list_lines = file.readlines()

# Step 2: Read lines from lexicon_tmp.txt
with open('../../main/data/lang/dict/lexicon_tmp.txt', 'r', encoding='utf-8') as file:
    lexicon_tmp_lines = file.readlines()

# Step 3: Combine and write to lexicon.txt
with open('../../main/data/lang/dict/lexicon.txt', 'w', encoding='utf-8') as file:
    for list_line, lexicon_tmp_line in zip(list_lines, lexicon_tmp_lines):
        # Step 4: Combine each line from list.txt with lexicon_tmp.txt
        combined_line = list_line.strip() + ' ' + lexicon_tmp_line
        # Step 5: Write to lexicon.txt
        file.write(combined_line)
os.remove('../../main/data/lang/dict/tmp.txt')
os.remove('../../main/data/lang/dict/lexicon_tmp.txt')
print("tmp.txt has been deleted.")
print("lexicon_tmp.txt has been deleted.")
print("Processing completed. The processed data has been saved to 'processed_lexicon.txt'.")
