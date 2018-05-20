
import os

from scipy.stats.mstats_basic import linregress
import textmining

import matplotlib.pyplot as plt
import numpy as np



tdm = textmining.TermDocumentMatrix()

input_direct = '../city_poi_by_type/AllCategory'

city_count = 0
for fname in os.listdir(input_direct):
    if fname == 'city_list.csv':
        continue
    
    city_count +=1
    
    city_name = fname.replace('.txt','')
    city_name = city_name.replace(' ','|')
    
    with open(input_direct+"/"+fname,'r') as fr:
        file_content = fr.read()
        file_content = file_content.replace(city_name,'')
        file_content = file_content.replace("  ",' ').strip()
        tdm.add_doc(file_content)
    
    
vocab_list = [] # a list for storing the vocabulary
matrix_rows = [] # matrix for storing the count values
is_first = True

# put the vocabulary and count values into variables
for row in tdm.rows(cutoff=1):
    if is_first:
        vocab_list = row
        is_first = False
    else:
        matrix_rows.append(list(row))
     
np_array = np.array(matrix_rows)
term_count_vect = np.sum(np_array,0) # sum the binary matrix along columns
term_percentage_vect = term_count_vect #(term_count_vect+1)/(float(city_count)+1)  # percentage of terms

term_count = len(term_percentage_vect)

a =  term_percentage_vect       
top_index = sorted(range(len(a)), key=lambda i: a[i])[-100:]
top_index = np.flip(top_index,0)
for i in range(10):
    print(vocab_list[top_index[i]])
  
   
sorted_term_freq_array = np.flip(np.sort(term_percentage_vect, kind='mergesort'),0)
x_index = range(1,term_count+1,1)

# first plot original values
x = x_index  
y = sorted_term_freq_array 
plt.scatter(x,y)
plt.xlabel('Rank of Words')
plt.ylabel('Frequency in POI Names')
plt.show()


# log-log plot here
x = np.log2(x_index)  #x_index #
y = np.log2(sorted_term_freq_array) 
plt.scatter(x,y)
slope, intercept, r_value, p_value, std_err = linregress(x,y)
print("p value ", p_value)
print("r-squared:", r_value**2)
plt.xlabel('Log(Rank of Words)')
plt.ylabel('Log(Frequency in POI Names)')
plt.show()

