

from gensim.models import KeyedVectors

import codecs,sys
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr

reload(sys)  
sys.setdefaultencoding('utf8')




# this function performs an experiment to test how cities are similar based on the embeddings learned from Google news
def correlation_google_news():
    
    filename = '/home/yingjie/Data/GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(filename, binary=True)
    # do a test
    result = model.most_similar(positive=['king','woman'], negative=['man'],topn=1)
    print(result)
    
    vocab_list = list(model.wv.vocab)
    
    distance_list = list()
    similarity_list = list()
        
    with codecs.open("../final_city_name_dist.csv","r","utf-8-sig") as fr:
        for line in fr:
            city_distance_split = line.split("|")
            
            # exclude the place names that contain multiple words
            if " " in city_distance_split[0]:
                continue
            
            if " " in city_distance_split[1]:
                continue
            
            first_city = city_distance_split[0].strip().replace(u'\ufeff', '')
            first_city = first_city.decode("utf-8-sig").encode("utf-8")
            first_city = first_city[:first_city.index(",")]
            first_city = first_city.strip()
            second_city = city_distance_split[1].strip().replace(u'\ufeff', '')
            second_city = second_city.decode("utf-8-sig").encode("utf-8")
            second_city = second_city[:second_city.index(",")]
            second_city = second_city.strip()
            
            if first_city in vocab_list and second_city in vocab_list:
                similarity_value = model.similarity(first_city, second_city)
                similarity_list.append(similarity_value)
                
                distance = float(city_distance_split[2])
                distance_list.append(distance)
            
    print pearsonr(distance_list,similarity_list)
    print spearmanr(distance_list,similarity_list)
    
    
if __name__ == "__main__":
    correlation_google_news()
