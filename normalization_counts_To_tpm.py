

################################# normalization ##########################################
##                  script accepts a matrix of m rows and n columns,                    ##
##                          first row is the sample next                                ##
##                          first colum is the gene name / id                           ##
##                  normalizes genes by TPM for each column individually                ##
##########################################################################################





import csv  # to avoid pandas install dependency
import argparse


parser = argparse.ArgumentParser(description='Normalization script,  performs TPM normalization on raw count data obtained from htseq, considers first row as header, and first column as gene names')
parser.add_argument('-i',  type=str,
                    help='name of input file, in tsv format')
parser.add_argument('-o', dest='infile',
                    const=sum, default='normalized_output.tsv', dest = 'outfile'
                    help='output file, normalized values,  in tsv format')

args = parser.parse_args()
#print(args.accumulate(args.integers))

with open('%s' %(args.infile),'r') as in_raw, open('%s' %(args.outfile),'w') as out_raw :

    infile = csv.reader(in_raw, delimiter = '\t')
    outfile = csv.writer(out_raw, delimiter = '\t')


    # most robust normalization technique is TPM  transcripts per million.
    # simple division

    header_dict = {}

    dict_of_row_lists = {}


    # first find total transctipts per column...

    # load data
    headList = []
    rowcount = 0
    for row in infile:
        elmnt_number = 0
        row_list = []
        
        if rowcount == 0:
            for element in row:
                if elmnt_number > 0:   # ignore label
                    header_dict[elmnt_number] = 0
                    headList.append(element)
            
                elmnt_number+=1
            outfile.writerow(headList)
        else:
            for element in row:
                if elmnt_number > 0:   # ignore label
                    row_list.append(element)
                elmnt_number+=1

                
            dict_of_row_lists[row[0]]= row_list
            

        rowcount +=1


    #   accumulate the values
    for key, values in dict_of_row_lists.items():
        count = 1
        for element in values:
            header_dict[count] += int(element)
            count +=1

    #   normalize

    for key, values in dict_of_row_lists.items():
        count = 1    # to skip the initial empty space
        for element in values:
            #print element 
            element = float(element) / (float(header_dict[count])/1000000.0)  # transcripts per million
            values[count-1] = element
            #print 'later', element
            count +=1 


    #   write to file

    for key, values in dict_of_row_lists.items():

        row_list = [key]
        for element in values:
            row_list.append(element)
        outfile.writerow(row_list)
    
    print rowcount
        
