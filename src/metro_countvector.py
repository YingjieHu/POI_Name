
import os, codecs
import sys  

from geopy.distance import vincenty
from matplotlib import pyplot
from scipy import spatial
from scipy.stats.mstats_basic import linregress
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.decomposition import PCA
import textmining

import numpy as np
from similarity_matrix import plot_similarity_matrix


reload(sys)  
sys.setdefaultencoding('utf8')




# a function that learns metropolitan vectors by the count of POI name terms
def learn_vector_by_count(poi_data_dir):
    
    tdm = textmining.TermDocumentMatrix() # this is from the text mining package
    metro_name_list = list()
    
    for fname in os.listdir(poi_data_dir):
        fr = codecs.open(os.path.join(poi_data_dir, fname),'r','utf-8')
        metro_name = fname.replace('.txt','')
        metro_name_list.append(metro_name.replace(" ","|").strip())
        metro_name = metro_name.replace(' ','|')
        POI_doc = ''
        
        for line in fr:
            line = line.replace(metro_name,'')
            line = line.strip()
            POI_doc += " " + line
            
        fr.close()
        POI_doc = POI_doc.strip()
        tdm.add_doc(POI_doc)
        
        
    vocab_list = [] # a list for storing the vocabulary
    matrix_rows = [] # matrix for storing the count values
    is_first = True
    
    metro_name_dict = dict() # this is a dictionary; given a metro name, we can know it index in the matrix 
    for i in range(len(metro_name_list)):
        metro_name_dict[metro_name_list[i]] = i
        
    # put the vocabulary and count values into variables
    for row in tdm.rows(cutoff=1):
        if is_first:
            vocab_list = row
            is_first = False
        else:
            matrix_rows.append(list(row))
        
        
    return vocab_list, matrix_rows, metro_name_dict, metro_name_list

  
    
# This function performs correlation; dimension is an optional parameter that allows
# us to reduce the dimensionality of the vectors before correlation; put -1 if you would like to use the 
# original dimension
def count_based_correlation_metro(matrix_rows, metro_name_dict, dimension):
    matrix_rows_compressed = matrix_rows
    
    # if the matrix is to be compressed
    if dimension != -1:
        pca = PCA(n_components=dimension)
        matrix_rows_compressed = pca.fit_transform(matrix_rows)
    
    distance_list = list()
    similarity_list = list()
    
    city_coord_dict = dict()

    with codecs.open('../city_coords_AllCategories.csv','r', 'utf-8') as fr:
        for line in fr:
            splitted = line.strip().split("|")
            city_name = splitted[0].replace(" ","|").strip().replace(u'\ufeff', '')
            city_coord_dict[city_name] = splitted[1]+"|"+splitted[2]
            
    
    metro_dict = dict()
    metro_dict['azstate'] = ""
    metro_dict['ilstate'] = ""
    metro_dict['ncstate'] = ""
    metro_dict['nvstate'] = ""
    metro_dict['ohstate'] = ""
    metro_dict['pastate'] = ""
    metro_dict['wistate'] = ""
    
    
    city_list = list()
    with codecs.open("../city_poi_by_type/AllCategory/city_list.csv","r","utf-8-sig") as fr:
        for line in fr:
            line = line.replace(" ","|").strip().replace(u'\ufeff', '')
            city_list.append(line)
            metro_name = line.split(',')[1] + 'state'
            if metro_name == 'scstate':
                metro_name = 'ncstate'
            metro_dict[metro_name] += city_coord_dict[line]+ ','
        
            
    metro_coord_dict = dict()
    metro_list = list()
    for metro_name in metro_dict:
        metro_list.append(metro_name)
        metro_coord_array = metro_dict[metro_name][0: (len(metro_dict[metro_name])-1)].split(',')
        lat = 0.0
        lng = 0.0
        count = 0.0
        for this_metro_coord in metro_coord_array:
            count += 1.0
            coords = this_metro_coord.split("|")
            lat += float(coords[0])
            lng += float(coords[1])
            
        metro_coord_dict[metro_name] = (lat/count, lng/count)
            

    for i in range(len(metro_list)-1):
        for j in range(i+1,len(metro_list)):
            
            first_metro = metro_list[i]
            second_metro = metro_list[j]
            
            first_coord = metro_coord_dict[first_metro]
        
            second_coord = metro_coord_dict[second_metro]
        
            distance = vincenty(first_coord, second_coord).miles
            distance_list.append(distance)
            
            first_city_vector = matrix_rows_compressed[metro_name_dict[first_metro]]
            second_city_vector = matrix_rows_compressed[metro_name_dict[second_metro]]
              
            similarity_value = (1 - spatial.distance.cosine(first_city_vector, second_city_vector))
            similarity_list.append(similarity_value)
              
    print pearsonr(distance_list,similarity_list)
    print spearmanr(distance_list,similarity_list)
    
    np_distance_list = np.array(distance_list)
    np_similarity_list = softmax(np.array(similarity_list))
    x = np.log2(np_distance_list) #np_distance_list #
    y = np.log2(np_similarity_list) #np_similarity_list #
    slope, intercept, r_value, p_value, std_err = linregress(x,y)
    print("r-squared:", r_value**2)
    
    print("slope:", slope)
    print("intercept:", intercept)
    print("p-value:", p_value)

    
    pyplot.plot(x, y, 'o')#, label='Original data')
    pyplot.plot(x, intercept + slope*x, 'r')#, label='Fitted line')
    pyplot.xlabel('Log(Distance)')
    pyplot.ylabel('Log(Similarity)')
    pyplot.legend()
    pyplot.show()
         


def softmax(x):
    
    orig_shape = x.shape

    if len(x.shape) > 1:
        # Matrix
        ### YOUR CODE HERE
        x = np.exp(x - np.max(x, 1, keepdims= True))
        x /= np.sum(x, 1, keepdims = True)
        ### END YOUR CODE
    else:
        # Vector
        ### YOUR CODE HERE
        x = np.exp(x - np.max(x))
        x /= np.sum(x)
        ### END YOUR CODE

    assert x.shape == orig_shape
    return x



# This function plots out the similarity matrix using the count-based vector approach
def vector_count_similarity_matrix_metro(matrix_rows,metro_name_dict):

    labels = ['nv','az','wi','il','oh','nc','pa']
    labels_vec = ['nvstate','azstate','wistate','ilstate','ohstate','ncstate','pastate']
                                                    
    dim = len(labels)
      
    matrix_data = np.zeros((dim,dim))
      
    for i in range(dim):
        for j in range(dim):
            first_city_vector = matrix_rows[metro_name_dict[labels_vec[i]]]
            second_city_vector = matrix_rows[metro_name_dict[labels_vec[j]]]
            similarity_value = (1 - spatial.distance.cosine(first_city_vector, second_city_vector))
            matrix_data[i,j] = similarity_value
              
    plot_similarity_matrix(matrix_data=matrix_data,labels=labels, plot_title= 'POI Name Similarity (Count-Based)')  



#main function starts
if __name__ == "__main__":
    # this function constructs the vectors for the metropolitan areas
    vocab_list, matrix_rows, metro_name_dict, metro_name_list = learn_vector_by_count('../city_poi_by_type/AllCategory_metro')
    
    # This function performs correlation analysis
    count_based_correlation_metro(matrix_rows, metro_name_dict, -1)
    
    # this function construct the similarity matrix
    #vector_count_similarity_matrix_metro(matrix_rows,metro_name_dict)
    
    
