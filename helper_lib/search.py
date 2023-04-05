def search_devices(device_list, search_term):
    """
    This function searches for rows in the device_list where at least one column
    has a partial match with the search_term, and returns a list of those rows.
    """
    matching_rows = []
    for row in device_list:
        for index in range(1, len(row)):
            if isinstance(row[index], str) and search_term.lower() in row[index].lower():
                matching_rows.append(row)
                break
            elif isinstance(row[index], bool) and str(row[index]).lower() == search_term.lower():
                matching_rows.append(row)
                break
    return matching_rows
