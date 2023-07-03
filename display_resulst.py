import matplotlib.pyplot as plt

# Read the contents of output.txt and output_weight.txt
with open("output.txt", "r") as file1, open("output_weight2.txt", "r") as file2:
    lines1 = file1.readlines()
    lines2 = file2.readlines()

instance_num = 0
total_distance1 = 0.0
total_distance2 = 0.0
active_arcs1 = []
active_arcs2 = []

# Determine the minimum number of lines between the two files
min_lines = min(len(lines1), len(lines2))

# Create lists to store the instance numbers and the comparison results
instance_nums = []
distances1 = []
distances2 = []
matches = []

for i in range(min_lines):
    line1 = lines1[i].strip()
    line2 = lines2[i].strip()

    if line1.startswith("Results for Instance"):
        # Skip the 0th instance
        if instance_num == 0:
            instance_num += 1
            continue

        instance_nums.append(instance_num)

        # Append the total distances to the respective lists
        distances1.append(total_distance1)
        distances2.append(total_distance2)

        # Check if the distances match and append the result to the matches list
        matches.append(total_distance1 == total_distance2)

        # Reset the variables for the next instance
        instance_num += 1
        total_distance1 = 0.0
        total_distance2 = 0.0
        active_arcs1.clear()
        active_arcs2.clear()

    elif line1.startswith("Sum of all totals:"):
        try:
            total_distance1 = float(line1.split(":")[1].strip())
            total_distance2 = float(line2.split(":")[1].strip())
        except (IndexError, ValueError):
            print("Invalid format in line:", line1)
            print("Skipping this instance.")
            continue

# Append the results for the last instance
instance_nums.append(instance_num)
distances1.append(total_distance1)
distances2.append(total_distance2)
matches.append(total_distance1 == total_distance2)

# Create the plot
fig, ax = plt.subplots()
ax.axis('off')

# Create the table
table_data = []
headers = ["Instance", "Total Distance for PD", "Total Distance for PL", "Match"]
for instance_num, distance1, distance2, match in zip(instance_nums, distances1, distances2, matches):
    table_data.append([instance_num, distance1, distance2, match])

table = ax.table(cellText=table_data, colLabels=headers, cellLoc="center", loc="center")

# Modify the table appearance
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

# Display the plot
plt.show()
