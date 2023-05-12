def get_all_records(cursor):
    get_all_records_query = '''SELECT * from sales_2;'''
    # Execute a command: this creates a new table
    cursor.execute(get_all_records_query)

    all_sales = cursor.fetchall()
    
    return all_sales