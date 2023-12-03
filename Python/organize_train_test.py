import csv
import json

#######################
# USER SET PARAMETERS #
#################################################

# Testing or training set?
# NOTE: ONLY valid options are 'test' or 'train'
which_set = 'train'

# Relative path to OpenMIC folder
relpath = '../openmic-2018/'

#################################################

# Parse aggregated labels file as dictionary
def parse_csv_to_dict(file_path):
    result_dict = dict()
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)       
        for row in csv_reader:
            if len(row) >= 2:
                if row[0] in result_dict:
                    result_dict[row[0]].append(row[1])
                else:
                    result_dict[row[0]] = [row[1]]
    return result_dict

# Convert labels from string format to binary indicator
# One bit per instrument, 20 instruments total
# Value of '1' indicated instrument present, '0' otherwise
def label_string_to_bin(labels_string, class_map):
    labels = [0]*20
    for l in labels_string:
        if l in class_map:
            labels[class_map[l]] = 1
    return labels

# Construct file paths
csv_file = relpath + 'partitions/split01_' + which_set + '.csv'
label_file = relpath + 'openmic-2018-aggregated-labels.csv'
class_file = relpath + 'class-map.json'
audio_outfile = which_set + '_audio.txt'
label_outfile = which_set + '_labels.txt'

# Get dict of labels
label_pairs = parse_csv_to_dict(label_file)

# Read in JSON class map and convert to dict
with open(class_file, 'r') as file:
    class_map = json.load(file)

# Parse partition file for file names/paths
audio_file_names = []
folder_name = []
labels = []
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row:
            # Extract name of audio file
            audio_file_name = row[0]
            audio_file_names.append(audio_file_name)
            # Extract first three digits for folder path
            first_three_digits = audio_file_name[:3]
            folder_name.append(first_three_digits)
            # Extract corresponding labels
            if audio_file_name in label_pairs:
                labels.append(label_string_to_bin(label_pairs[audio_file_name], class_map))


# Save *.txt file with locations of all Testing and Training files
with open(audio_outfile, 'w') as f_audio:
    with open(label_outfile, 'w', newline='') as f_label:
        writer = csv.writer(f_label)
        for i in range(len(audio_file_names)):    
            f_audio.write('openmic-2018/audio/' + folder_name[i] + '/' + audio_file_names[i] + '.ogg\n')
            writer.writerow(labels[i])