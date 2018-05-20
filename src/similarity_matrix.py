
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
    plt.xticks(range(7), labels, rotation=90);
    plt.yticks(range(7), labels);
    fig.colorbar(cax, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, .75,.8,.85,.90,.95,1])
    plt.show()
    
    #fig.savefig('embeddingSimilarity.png',dpi=300)
    
    

# calculate the collective similarity of POI names using word2vec
def word2vec_similarity_metro():
    # use word2vec to fill in the matrix values
    model = Word2Vec.load('../models/model_300_AllCategory_metro.bin')

    labels = ['nv','az','wi','il','oh','nc','pa']
    labels_vec = ['nvstate','azstate','wistate','ilstate','ohstate','ncstate','pastate']
                 
    dim = len(labels)
     
    matrix_data = np.zeros((dim,dim))
     
    for i in range(dim):
        for j in range(dim):
            matrix_data[i,j] = model.similarity(labels_vec[i], labels_vec[j])

    plot_similarity_matrix(matrix_data=matrix_data,labels=labels, plot_title='POI Name Similarity (word2vec)')  



   
# calculate the distance between metropolitan areas
def geo_distance_similarity_metro():

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
            if metro_name == 'scstate':  # note: there is one city in South Carolina in the data, which is very close to ther other NC cities. Thus, we consider it as NC.
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
            
        metro_coord_dict[metro_name] = str(lat/count)+','+ str(lng/count)

   
    labels = ['nv','az','wi','il','oh','nc','pa']
    coords = list()
    for i in range(7):
        coords.append(metro_coord_dict[labels[i]+'state'])
#     with codecs.open("../final_city_name_coords_US_only.csv","r","utf-8-sig") as fr:
#             for line in fr:
#                 splitted = line.split(',')
#                 city_name = (splitted[0]+','+splitted[1]).replace(" ","|").strip().replace(u'\ufeff', '')
#                 city_name = city_name.decode("utf-8-sig").encode("utf-8")
#                 labels.append(city_name)
#                 coords.append((splitted[2]+','+splitted[3]).strip())
             
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
    geo_distance_similarity_metro()
    #word2vec_similarity_metro()
    