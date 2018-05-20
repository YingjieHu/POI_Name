
import os, codecs
import sys

from gensim.models.word2vec import Word2Vec
from geopy.distance import vincenty
from matplotlib import pyplot
from scipy.stats.mstats_basic import linregress
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr

import numpy as np


reload(sys)  
sys.setdefaultencoding('utf8')


# train the word2vec model for POIs in metropolitan areas
def train_word2vec(categoryName):
 
    class MySentences(object):
        def __init__(self, dirname):
            self.dirname = dirname
       
        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for line in open(os.path.join(self.dirname, fname)):
                    yield line.split()
       
    sentences = MySentences('../city_poi_by_type/'+categoryName+'_metro')
    
    # train multiple word2vec models with changing dimensions
    for dim in range(300,301,50):
        model = Word2Vec(sentences, size=dim, window=12, min_count=1, workers=4, sg=1)
        print('The dimension is '+str(dim))
        
        # do 3 similarity tests
        print(model.most_similar(positive=['azstate'],topn=5))
        print(model.most_similar(positive=['ohstate'],topn=5))
        #print(model.most_similar(positive=['toronto,on'],topn=5))
        
        model.save('../models/model_'+str(dim)+'_'+categoryName+'_metro.bin')

      
        
# load the pre-trained word2vec model; then calculate Pearson and Spearman correlations
def correlation_based_on_word2vec_metro_scale(categoryName):
    for dim in range(300,301,50): 
        print('dim is '+str(dim))
        model = Word2Vec.load('../models/model_'+str(dim)+'_'+categoryName+'_metro.bin')
        #print(model.wv.vocab)

        # load city coords
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
            
                
        distance_list = list()
        similarity_list = list()
        
        for i in range(len(metro_list)-1):
            for j in range(i+1,len(metro_list)):
                first_metro = metro_list[i]
                second_metro = metro_list[j]
                
                first_coord = metro_coord_dict[first_metro]
            
                second_coord = metro_coord_dict[second_metro]
            
                distance = vincenty(first_coord, second_coord).kilometers
                distance_list.append(distance)
                
                similarity_value = model.similarity(first_metro, second_metro)
                similarity_list.append(similarity_value)
                  
        print pearsonr(distance_list,similarity_list)
        print spearmanr(distance_list,similarity_list)
        
        np_distance_list = np.array(distance_list)
        np_similarity_list = np.array(similarity_list)
        x = np.log2(np_distance_list) #np_distance_list #
        y = np.log2(np_similarity_list) #np_similarity_list #
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        print("r-squared:", r_value**2)
        
        print("slope:", slope)
        print("intercept:", intercept)
        print("p-value:", p_value)

        # we can plot out the result
        #pyplot.scatter(x,y)
        pyplot.plot(x, y, 'o')#, label='Original data')
        pyplot.plot(x, intercept + slope*x, 'r')#, label='Fitted line')
        pyplot.xlabel('Log(Distance)')
        pyplot.ylabel('Log(Similarity)')
        pyplot.legend()
        pyplot.show()
        




#main function starts
if __name__ == "__main__":

    # use the command below to train word2vec
    #train_word2vec("AllCategory")
 
    # calculate the correlation between word2vec based similarity and distance
    correlation_based_on_word2vec_metro_scale("AllCategory")


