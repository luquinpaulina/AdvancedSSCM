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

for i in range(min_lines):
    line1 = lines1[i].strip()
    line2 = lines2[i].strip()

    if line1.startswith("Results for Instance"):
        # Print the instance number and total distance
        print(f"Instance {instance_num}")
        print(f"Total Distance (output.txt): {total_distance1}")
        print(f"Total Distance (output_weight.txt): {total_distance2}")

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

# Check for differences in the last instance
print(f"Instance {instance_num}")
print(f"Total Distance for Distance Minimization Model: {total_distance1}")
print(f"Total Distance for Weight-Load Minimization Model: {total_distance2}")
