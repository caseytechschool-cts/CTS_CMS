def search_devices(device_list, search_term):
    """
    This function searches for rows in the device_list where at least one column
    has a partial match with the search_term, and returns a list of those rows.
    """
    matching_rows = []
    for row in device_list:
        for column in row:
            if isinstance(column, str) and search_term.lower() in column.lower():
                matching_rows.append(row)
                break
            elif isinstance(column, bool) and str(column).lower() == search_term.lower():
                matching_rows.append(row)
                break
    return matching_rows
