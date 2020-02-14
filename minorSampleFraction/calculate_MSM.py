#!/usr/bin/env python3

import re
import sys

def combine_files(search_text):
    print("Searching for files:", search_text)
	combined_file = pd.DataFrame() # create empty data frame
    filenames = glob.glob(search_text) # first import any number of files
    if len(filenames) == 0: # if the file is blank, let people know
        print("no files")
        print("no file created")
        exit(2) # end the program (this will exit python) fail fast!
    else: 
        true_columns = sorted(['dbSNP.ID', 'allele', 'count' ]) # We know the true columns
        for file in filenames:
            test_file = pd.read_csv(file)
            column_list = sorted(list(test_file.columns.values))
            if len(column_list) == 3: # if there are three columns
                if true_columns == column_list: # if they match true headers
                    true_allele = sorted(['A', 'R'])
                    if true_allele == sorted(list(test_file.allele.unique())):
                        test_file['FileName'] = file # add the file name as a column
                        try:
                            # test if the count column really is numbers
                            test_file['count'] = test_file['count'].astype(float)
                            
                            combined_file = combined_file.append(test_file,ignore_index=True) 
                            print(file, "file added") # this may be impractical if there are hundreds of files
                        except ValueError:
                            print(file, "count column includes non-numbers")
                        
                    else:
                        print(file, "wrong allele list", test_file.allele.unique())
                        # Another source of error could be that the file was set up wrong.  
                        # This is only one way it could be wrong.  Another could be in SNP name and Count NAN
                else:
                    print(file, "columns do not match", column_list)
            else:
                print(file, "too many columns", column_list)
        #export to csv
        new_file_name = str(datetime.date.today()) + "combined_file.csv"
        combined_file.to_csv(new_file_name, index=False) # save the file before doing calculations
        print(new_file_name," file created")
    return(combined_file)

def label_informative(data_frame):
    # spread the columns (make the two alleles each their own column)
    stacked_file = data_frame.pivot_table(index=['dbSNP.ID', 'FileName'], columns='allele', values='count') 
    stacked_file = stacked_file.reset_index() # I don't like working with two columns as "index"
    stacked_file = stacked_file.fillna(0) # if either A or R had no values, we fill them with zero
    # caluclate the frequency of A allele, R is not needed as freq_A + freq_R = 1
    stacked_file['freq_A'] = stacked_file['A']/(stacked_file['R']+ stacked_file['A'])
    # we want those with low A and with low R.  Subtracting freq_A from 0.5 gets us low A
    # using the absolute value (abs) gives us both low R and low A
    stacked_file['abs_A'] = abs(stacked_file['freq_A'] - 0.5)
    # we want to label those with frequency (A or R) > 0.8 as informative
    stacked_file.loc[stacked_file.abs_A > 0.3, 'informative'] = 'True' 
    stacked_file.loc[stacked_file.abs_A <= 0.3, 'informative'] = 'False' 
    # there are some SNP's with very low counts, possibly due to read error
    # I chose to ignore those with counts less than 2% as uninformative
    stacked_file.loc[stacked_file.abs_A > 0.48, 'informative'] = 'False'
    new_file_name = str(datetime.date.today()) + "calculations_file.csv"
    stacked_file.to_csv(new_file_name, index = False) # save the file before doing calculations
    print(new_file_name," file created")
    # the exercise said to create a file with orig file name, SNP and informative-ness
    output_1 = stacked_file[['FileName','dbSNP.ID', 'informative' ]]
    output_1.to_csv('output_1.csv', index = False)
    return(stacked_file)

def find_MSF(data_frame):
    contam_data = data_frame.loc[data_frame['informative'] == 'True'].copy()
    contam_data['MSF'] = abs(contam_data['abs_A'] - 0.5)
    # uncertanty can be a measure of the error around the mean.
    # I am chosing standard deviation (std) and standard error (sem).
    minor_sample_fraction = contam_data.groupby(['FileName'], as_index = False).agg(
        {'MSF': ['mean', 'count','std', 'sem']})
    new_file_name = str(datetime.date.today()) + "MSF_output2.csv"
    minor_sample_fraction.to_csv(new_file_name, index = False) # save the file before doing calculations
    return(minor_sample_fraction)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("please provide search parameter: text and wild card (*)")
		exit(1)
	reg_expression = sys.argv[1]
	all_files = combine_files(reg_expression)
	labeled_SNP = label_informative(all_files)
	mean_MSF = find_MSF(labeled_SNP)
	
