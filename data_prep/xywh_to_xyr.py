import csv

# Paths to the input and output CSV files
input_csv_path = "../data_points/data_cords.csv"
output_csv_path = "../data_points/xyr_cords.csv"

# Read the input CSV file and write to the output CSV file
with open(input_csv_path, mode='r', newline='') as infile, open(output_csv_path, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    # Write the header for the output CSV
    writer.writerow(['sno', 'x', 'y', 'r'])
    
    # Process each row in the input CSV
    for sno, row in enumerate(reader, start=1):
        x = float(row['x'])
        y = float(row['y'])
        w = float(row['w'])
        h = float(row['h'])
        r = min(w, h) / 2
        writer.writerow([sno, x, y, r])

print(f"Data has been successfully written to {output_csv_path}")