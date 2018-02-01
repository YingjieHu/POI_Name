

import os, codecs
import sys  

from scipy import spatial
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfTransformer
import textmining

import numpy as np
from similarity_matrix import plot_similarity_matrix


reload(sys)  
sys.setdefaultencoding('utf8')




# a function that learns city vectors by the count of POI name words
def learn_vector_by_count():
    
    tdm = textmining.TermDocumentMatrix() # this is from the text mining package
    city_name_list = list()
    
    for fname in os.listdir('../city_poi_data'):
        fr = codecs.open(os.path.join('../city_poi_data', fname),'r','utf-8')
        city_name = fname.replace('.txt','')
        city_name_list.append(city_name.replace(" ","|").strip())
        city_name = city_name.replace(' ','|')
        POI_doc = ''
        
        for line in fr:
            line = line.replace(city_name,'')
            line = line.strip()
            POI_doc += " " + line
            
        fr.close()
        POI_doc = POI_doc.strip()
        tdm.add_doc(POI_doc)
        
        
    vocab_list = [] # a list for storing the vocabulary
    matrix_rows = [] # matrix for storing the count values
    is_first = True
    
    city_name_dict = dict() # this is a dictionary; given a city name, we can know it index in the matrix 
    for i in range(len(city_name_list)):
        city_name_dict[city_name_list[i]] = i
        
    
    # put the vocabulary and count values into variables
    for row in tdm.rows(cutoff=1):
        if is_first:
            vocab_list = row
            is_first = False
        else:
            matrix_rows.append(list(row))
        
        
    return vocab_list, matrix_rows, city_name_dict, city_name_list



# given a city name, a city name list, and their learned vector representations, find top 5 similar cities
def get_similar_city(city_name, city_name_list, vector_matrix):
    
    # step 1: identify the index of the study city
    city_index = -1
    for i in range(len(city_name_list)):
        if city_name_list[i] == city_name:
            city_index = i
            break
    
    # step 2: calculate the similarity value of this city with regard to other cities
    similarity_list = list()
    target_city_vector = vector_matrix[city_index]
    for i in range(len(city_name_list)):
        this_city_vector = vector_matrix[i]
        similarity_value = (1-spatial.distance.cosine(target_city_vector, this_city_vector))
        similarity_list.append(similarity_value)
    
    # step 3: find and identify the top 6 cities (including itself) that have the highest similarity  
    a = similarity_list
    top_index = sorted(range(len(a)), key=lambda i: a[i])[-6:]
    top_city = ''
    for index in top_index:
        top_city += ' '+city_name_list[index]+":"+str(a[index])
         
    print(top_city)
         
         

        
# this function reduce the dimension of the count-based vector to 300; then perform correlation
def pca_count_correlation(matrix_rows, city_name_dict):
    pca = PCA(n_components=300)
    matrix_rows_compressed = pca.fit_transform(matrix_rows)
    
    distance_list = list()
    similarity_list = list()
         
    with codecs.open("../final_city_name_dist_US_only.csv","r","utf-8-sig") as fr:
        for line in fr:
            city_distance_split = line.split("|")
            distance = float(city_distance_split[2])
            distance_list.append(distance)
             
            first_city = city_distance_split[0].replace(" ","|").strip().replace(u'\ufeff', '')
            first_city = first_city.decode("utf-8-sig").encode("utf-8")
            second_city = city_distance_split[1].replace(" ","|").strip().replace(u'\ufeff', '')
            second_city = second_city.decode("utf-8-sig").encode("utf-8")
             
            first_city_vector = matrix_rows_compressed[city_name_dict[first_city]]
            second_city_vector = matrix_rows_compressed[city_name_dict[second_city]]
             
            similarity_value = (1 - spatial.distance.cosine(first_city_vector, second_city_vector))
            similarity_list.append(similarity_value)
             
    print pearsonr(distance_list,similarity_list)
    print spearmanr(distance_list,similarity_list)
    


# this function plots the similarity matrix with count-based vectors
def vector_count_similarity_matrix(matrix_rows,city_name_dict):
    labels = list()
    #coords = list()
    with codecs.open("../final_city_name_coords_US_only.csv","r","utf-8-sig") as fr:
            for line in fr:
                splitted = line.split(',')
                city_name = (splitted[0]+','+splitted[1]).replace(" ","|").strip().replace(u'\ufeff', '')
                city_name = city_name.decode("utf-8-sig").encode("utf-8")
                labels.append(city_name)
                             
    dim = len(labels)
      
    matrix_data = np.zeros((dim,dim))
      
    for i in range(dim):
        for j in range(dim):
            first_city_vector = matrix_rows[city_name_dict[labels[i]]]
            second_city_vector = matrix_rows[city_name_dict[labels[j]]]
            similarity_value = (1 - spatial.distance.cosine(first_city_vector, second_city_vector))
            matrix_data[i,j] = similarity_value
              
    plot_similarity_matrix(matrix_data=matrix_data,labels=labels, plot_title= 'POI Name Similarity (Count-Based Vector)')  



# this function finds the top 20 words used in a city's POI names by tf-idf
def find_city_top_words_by_tfidf(matrix_rows, city_name_list):
    
    transformer = TfidfTransformer(smooth_idf=False)
    matrix_rows = transformer.fit_transform(matrix_rows).toarray() 
      
    fw = codecs.open('../city_frequent_words_tfidf.csv','w','utf8')
    
    city_size = len(city_name_list)
    for i in range(city_size):
#         print i
#         print(city_name_list[i])
#         print(city_name_dict[city_name_list[i]])  
        a = matrix_rows[i]
        top_index = sorted(range(len(a)), key=lambda i: a[i])[-20:]
           
        top_words = ''
        for index in top_index:
            top_words += ' '+vocab_list[index]+":"+str(a[index])
               
        print(top_words.strip())
           
        fw.write(city_name_list[i]+"|"+top_words+"\n")
       
    fw.close()



#main function starts
if __name__ == "__main__":
    vocab_list, matrix_rows, city_name_dict, city_name_list = learn_vector_by_count()
    get_similar_city('phoenix,az', city_name_list, matrix_rows)
    
    # get_similar_city('cleveland,oh', city_name_list, matrix_rows)
    # get_similar_city('charlotte,nc', city_name_list, matrix_rows)
    # get_similar_city('toronto,on', city_name_list, matrix_rows)
    # get_similar_city('edinburgh,edh', city_name_list, matrix_rows)
    # get_similar_city('stuttgart,bw', city_name_list, matrix_rows)
    
    
    
