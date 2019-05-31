input_file = "masks/mask-edfa1-padtec-icton17-normalized.txt"
output_file_1 = "masks/mask-edfa1-padtec-icton17-fold-1.txt"
output_file_2 = "masks/mask-edfa1-padtec-icton17-fold-2.txt"
output_file_3 = "masks/mask-edfa1-padtec-icton17-fold-3.txt"
output_file_4 = "masks/mask-edfa1-padtec-icton17-fold-4.txt"
output_file_5 = "masks/mask-edfa1-padtec-icton17-fold-5.txt"

output_files = [output_file_1, output_file_2, output_file_3, output_file_4, output_file_5]

# Reading data
with open(input_file, 'r') as f_in:
    entries = f_in.readlines()

# Splitting data into 5 folds
fold_size = (len(entries)) / 5
start = 0

for output_file in output_files:
    with open(output_file, 'w') as f_out:
        end = start + fold_size
        f_out.writelines(entries[start:end])
        start = end