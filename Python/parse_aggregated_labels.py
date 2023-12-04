import csv
from collections import Counter

# Parse aggregated labels file and pull out one-instrument files
def parse_labels(input_csv_path, output_txt_path):
    # Dictionary to store the occurrences of each sample_key
    sample_key_count = {}

    # Dictionary to store the corresponding instrument for each sample_key
    sample_key_instruments = {}

    # Read the CSV file and count occurrences of each sample_key
    with open(input_csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            if len(row) >= 2:  # Ensure the row has at least two entries
                sample_key = row[0]
                instrument = row[1]

                # Count occurrences of each sample_key
                if sample_key in sample_key_count:
                    sample_key_count[sample_key] += 1
                else:
                    sample_key_count[sample_key] = 1

                # Store the corresponding instrument for each sample_key
                sample_key_instruments[sample_key] = instrument

    # List to store sample_key values that occur only once
    one_occurrence_keys = [key for key, count in sample_key_count.items() if count == 1]

    # Write the list of sample_key and corresponding instrument to the output text file
    with open(output_txt_path, 'w') as txt_file:
        for key in one_occurrence_keys:
            txt_file.write(f"{key}, {sample_key_instruments[key]}\n")

# Count single-instrument audio samples, per instrument
def count_instruments(input_file, output_file):
    # Dictionary to store instrument counts
    instrument_counts = Counter()

    # Read input file and count occurrences, skipping the first line
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 2:
                sample_key, instrument = row
                instrument_counts[instrument] += 1

    # Sort instruments by count in descending order
    sorted_instruments = sorted(instrument_counts.items(), key=lambda x: x[1], reverse=True)

    # Write instrument counts to output file
    with open(output_file, 'w') as file:
        for instrument, count in sorted_instruments:
            file.write(f"{instrument}: {count}\n")

        # Write the total count of all instruments
        total_count = sum(instrument_counts.values())
        file.write(f"\nTotal Count of All Instruments: {total_count}\n")


if __name__ == "__main__":
    f_labels = '../openmic-2018/openmic-2018-aggregated-labels.csv'
    f_one_instrument = 'dataset-statistics/one-instrument.txt'
    f_one_instrument_counts = "dataset-statistics/one-instrument-counts.txt"

    parse_labels(f_labels, f_one_instrument)
    count_instruments(f_one_instrument, f_one_instrument_counts)