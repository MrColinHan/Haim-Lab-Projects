'''
Changze Han
4.19.21

takes fasta as input
remove sequences that have either 'x' or '*'

'''

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.19.21 deep seq fd/"
fas_input_name = "part 3 ugly SRR5105314.fasta"
fas_output_name = "Cleaned_part 3 ugly SRR5105314.fasta"
# ========================================================================================================

input_list = list()
output_list = list()


def read_fasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def write_fas(x,y): # write the list x into y file
    output= open(y,"w+")
    for i in x:
        output.write(i)
    output.close


def main():
    read_fasta(working_dir+fas_input_name, input_list)
    print(f"len:{len(input_list)}")
    print(input_list[0])
    print(input_list[1])
    print(input_list[2])
    print(input_list[3])
    print('......')

    for i in range(len(input_list)):
        if input_list[i][0] == '>':
            if ('x' not in input_list[i+1]) and ('X' not in input_list[i+1]) and ('*' not in input_list[i+1]):
                output_list.append(input_list[i])
                output_list.append(input_list[i+1])

    print(f"len:{len(output_list)}")
    write_fas(output_list, working_dir+fas_output_name)



main()
