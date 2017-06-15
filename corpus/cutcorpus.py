from math import floor

lines = []
lines_counter = 0
num_lines = sum(1 for line in open('big.txt'))
print("La cantidad de lineas es: ", num_lines)

lines_per_file = floor(num_lines / 10)
counter = 0

with open('big.txt') as big_file:
    for line in big_file:  # Go throught the whole big file
        lines.append(line)
        lines_counter += 1
        if lines_counter == lines_per_file:
            with open('toTest.txt', 'w') as small_file:
                # Write all lines on small file
                small_file.write('\n'.join(lines))
            counter = lines_counter - counter
            print("Se escribieron ", counter, "lineas")
            lines = []  # Reset variables

        if lines_counter == num_lines:
            with open('toTrain.txt', 'w') as small_file:
                # Write all lines on small file
                small_file.write('\n'.join(lines))
            counter = lines_counter - counter
            print("Se escribieron ", counter, "lineas")
            lines = []  # Reset variables
            lines_counter = 0
