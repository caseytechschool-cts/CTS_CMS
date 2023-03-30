import csv


def save(download_path, table_heading, table_data, window):
    with open(download_path, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(table_heading)
        writer.writerows(table_data)
    window.write_event_value('-Thread-csv-download-', 'done')

