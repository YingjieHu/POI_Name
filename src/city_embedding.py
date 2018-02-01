

import os, codecs
import sys

from gensim.models.word2vec import Word2Vec
from matplotlib import pyplot
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.decomposition import PCA


reload(sys)  
sys.setdefaultencoding('utf8')




def train_word2vec():
# Some test example data
# sentences = [['Knoxville','Music','Club'],
#             ['Knoxville','Vol','Shop'],
#             ['Knoxville','Tennessee','University'],
#             ['Knoxville','Dance','Club'],
#             ['Nashville','Music','Club'],
#             ['Nashville','BBQ','Restaurant'],
#             ['Nashville','Tennessee','State'],
#             ['Nashville','Dance','Club'],
#             ['DC','White','House'],
#             ['DC','Congress'],
#             ['DC','Capitol','Hill'],
#             ['DC','Maryland'],
#             ['DC','Noodle'],
#             ]
 
    class MySentences(object):
        def __init__(self, dirname):
            self.dirname = dirname
       
        def __iter__(self):
            for fname in os.listdir(self.dirname):
                for line in open(os.path.join(self.dirname, fname)):
                    yield line.split()
       
    sentences = MySentences('../city_poi_data')
    
    # train multiple word2vec models with changing dimensions
    for dim in range(50,500,50):
        model = Word2Vec(sentences, size=dim, window=12, min_count=1, workers=4, sg=1)
        print('The dimension is '+str(dim))
        # do 3 similarity tests
        print(model.most_similar(positive=['phoenix,az'],topn=5))
        print(model.most_similar(positive=['madison,wi'],topn=5))
        print(model.most_similar(positive=['toronto,on'],topn=5))
        model.save('../models/model_'+str(dim)+'.bin')




# load a trained word2vec model; and test similar cities
def identify_most_similar_cities():
    model = Word2Vec.load('../models/model_300.bin')
    result = model.most_similar(positive=['phoenix,az'], topn=20)
    print(result)
    result = model.most_similar(positive=['cleveland,oh'], topn=20)
    print(result)
    result = model.most_similar(positive=['charlotte,nc'], topn=20)
    print(result)
    result = model.most_similar(positive=['toronto,on'], topn=20)
    print(result)
    result = model.most_similar(positive=['edinburgh,edh'], topn=20)
    print(result)
    result = model.most_similar(positive=['stuttgart,bw'], topn=20)
    print(result)



# load the pre-trained word2vec model; then calculate correlation
def correlation_based_on_word2vec():
    for dim in range(50,500,50): 
        print('dim is '+str(dim))
        model = Word2Vec.load('../models/model_'+str(dim)+'.bin')
        #print(model.wv.vocab)
         
        distance_list = list()
        similarity_list = list()
        
        # get distance values between cities
        with codecs.open("../final_city_name_dist_US_only.csv","r","utf-8-sig") as fr:
            for line in fr:
                city_distance_split = line.split("|")
                distance = float(city_distance_split[2])
                distance_list.append(distance)
                  
                first_city = city_distance_split[0].replace(" ","|").strip().replace(u'\ufeff', '')
                first_city = first_city.decode("utf-8-sig").encode("utf-8")
                second_city = city_distance_split[1].replace(" ","|").strip().replace(u'\ufeff', '')
                second_city = second_city.decode("utf-8-sig").encode("utf-8")
                  
                similarity_value = model.similarity(first_city, second_city)
                similarity_list.append(similarity_value)
                  
        print pearsonr(distance_list,similarity_list)
        print spearmanr(distance_list,similarity_list)
        
        # we can plot out the result
        #pyplot.plot(distance_list,similarity_list)
        #pyplot.show()



def plot_word_vectors():
    
    # get a list of city names
    city_name_dict = dict()

    for fname in os.listdir('../city_poi_data'):
        for line in open(os.path.join('../city_poi_data', fname)):
            line = line.decode("utf-8-sig").encode("utf-8")
            splitted = line.split()
            city_name_dict[splitted[0].strip()] = 0


    city_list = city_name_dict.keys() #['DC', 'Knoxville','Nashville']
    model = Word2Vec.load('../models/model_300.bin')
    X = model[city_list]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
     
    pyplot.scatter(result[:,0], result[:,1])
    words = city_list #list(model.wv.vocab)
     
    for i, word in enumerate(words):
        word = word.replace("|"," ")
        pyplot.annotate(word, xy=(result[i,0], result[i,1]))
        
    pyplot.show()




#main function starts
if __name__ == "__main__":
    plot_word_vectors()

