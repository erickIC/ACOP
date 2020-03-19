import random

## Files for ICTON 17
icton_input_file = "masks/mask-edfa1-padtec-icton17-normalizedv2.txt"
icton_output_file_1 = "masks/mask-edfa1-padtec-icton17-fold-1v2.txt"
icton_output_file_2 = "masks/mask-edfa1-padtec-icton17-fold-2v2.txt"
icton_output_file_3 = "masks/mask-edfa1-padtec-icton17-fold-3v2.txt"
icton_output_file_4 = "masks/mask-edfa1-padtec-icton17-fold-4v2.txt"
icton_output_file_5 = "masks/mask-edfa1-padtec-icton17-fold-5v2.txt"

## Files for New Models
others_input_file = "masks/mask-edfa1-padtec-new-models-normalizedv2.txt"
others_output_file_1 = "masks/mask-edfa1-padtec-new-models-fold-1v2.txt"
others_output_file_2 = "masks/mask-edfa1-padtec-new-models-fold-2v2.txt"
others_output_file_3 = "masks/mask-edfa1-padtec-new-models-fold-3v2.txt"
others_output_file_4 = "masks/mask-edfa1-padtec-new-models-fold-4v2.txt"
others_output_file_5 = "masks/mask-edfa1-padtec-new-models-fold-5v2.txt"

icton_output_files = [icton_output_file_1, icton_output_file_2, icton_output_file_3, icton_output_file_4, icton_output_file_5]
others_output_files = [others_output_file_1, others_output_file_2, others_output_file_3, others_output_file_4, others_output_file_5]

# Reading data
with open(icton_input_file, 'r') as f_icton_in, open(others_input_file, 'r') as f_others_in:
    icton_entries = f_icton_in.readlines()
    others_entries = f_others_in.readlines()

# Splitting data indexes into 5 random folds
total_size = len(others_entries)
indexes = list(range(total_size))
random.shuffle(indexes)

number_of_folds = 5
fold_size = total_size / number_of_folds

fold_1 = indexes[:int(fold_size)]
fold_2 = indexes[int(fold_size):int(fold_size*2)]
fold_3 = indexes[int(fold_size*2):int(fold_size*3)]
fold_4 = indexes[int(fold_size*3):int(fold_size*4)]
fold_5 = indexes[int(fold_size*4):]

folds = [fold_1, fold_2, fold_3, fold_4, fold_5]

# Writing output files
number_of_channels = 40
max_size = len(icton_entries)

for icton_output_file, others_output_file, fold in zip(icton_output_files, others_output_files, folds):
    with open(icton_output_file, 'w') as f_icton_out, open(others_output_file, 'w') as f_others_out:
        for index in fold:
            f_others_out.write(others_entries[index])

            # Mapping other model index to icton index
            start = int(index * number_of_channels)
            end = int(start + number_of_channels)
            if end == max_size:
                f_icton_out.writelines(icton_entries[start:])
                continue
            f_icton_out.writelines(icton_entries[start:end])