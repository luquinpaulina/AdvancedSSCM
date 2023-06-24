import pandas as pd

# Read the text file
file_path = 'C201.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Find the start and end indices of the customer section
start_index = lines.index('CUSTOMER\n') + 2

# Extract the customer data
customer_data = [line.split() for line in lines[start_index:]]

# Convert the customer data to a DataFrame
df = pd.DataFrame(customer_data, columns=['CUST NO.', 'XCOORD.', 'YCOORD.', 'DEMAND', 'READY TIME', 'DUE DATE', 'SERVICE TIME'])

# Convert numeric columns to appropriate data types
numeric_columns = ['CUST NO.', 'XCOORD.', 'YCOORD.', 'DEMAND', 'READY TIME', 'DUE DATE', 'SERVICE TIME']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

# Add depot (customer 0) to each set
customer_sets = []
for i in range(1, len(df), 10):  # Increment by 11 to include depot customer
    customer_set = df.iloc[i:i+10]
    customer_sets.append(customer_set)

# Print the customer sets
for i, customer_set in enumerate(customer_sets):
    print(f"Customer Set {i+1}:")
    print(customer_set)
    print()







