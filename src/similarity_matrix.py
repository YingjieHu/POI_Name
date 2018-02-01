
import codecs
import sys  

from gensim.models.word2vec import Word2Vec
from geopy.distance import vincenty
from matplotlib import cm as cm
from matplotlib.pyplot import savefig

import matplotlib.pyplot as plt
import numpy as np


reload(sys)  
sys.setdefaultencoding('utf8')



# This is the core function for plotting out similarity matrix
def plot_similarity_matrix(matrix_data, labels, plot_title):
    fig, ax = plt.subplots(figsize=(20,20))
    cmap = cm.get_cmap('RdYlGn')
    cax = ax.matshow(matrix_data, interpolation='nearest',cmap=cmap)
    #ax.grid(True)
    plt.title(plot_title)
    #plt.xticks(range(77), labels, rotation=90);
    plt.yticks(range(77), labels);
    fig.colorbar(cax, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, .75,.8,.85,.90,.95,1])
    plt.show()
    
    #fig.savefig('embeddingSimilarity.png',dpi=300)
    
    
    

# plotting similarity matrix using word2vec
def word2vec_similarity():
    # use word2vec to fill in the matrix values
    model = Word2Vec.load('../models/model_300.bin')

    labels = list()
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
            matrix_data[i,j] = model.similarity(labels[i], labels[j])

    plot_similarity_matrix(matrix_data=matrix_data,labels=labels, plot_title='POI Name Similarity (Neural Network Embedding)')  




# This function plot out similarity matrix based on geographic distance
def geo_distance_similarity():
   
    labels = list()
    coords = list()
    with codecs.open("../final_city_name_coords_US_only.csv","r","utf-8-sig") as fr:
            for line in fr:
                splitted = line.split(',')
                city_name = (splitted[0]+','+splitted[1]).replace(" ","|").strip().replace(u'\ufeff', '')
                city_name = city_name.decode("utf-8-sig").encode("utf-8")
                labels.append(city_name)
                coords.append((splitted[2]+','+splitted[3]).strip())
                 
    dim = len(labels)
     
    matrix_data = np.zeros((dim,dim))
     
    for i in range(dim):
        for j in range(dim):
            first_splitted = coords[i].split(",")
            first_coord = (float(first_splitted[0]),float(first_splitted[1]))
              
            second_splitted = coords[j].split(",")
            second_coord = (float(second_splitted[0]),float(second_splitted[1]))
              
            distance = vincenty(first_coord, second_coord).miles
              
            matrix_data[i,j] = distance / 1931.44912074 #math.log(10+distance) / math.log(10+1931.44912074)
             
    plot_similarity_matrix(matrix_data=matrix_data,labels=labels, plot_title='Distance Between Geographic Regions')  
    
    


#main function starts
if __name__ == "__main__":
    #geo_distance_similarity()
    word2vec_similarity()
    
    