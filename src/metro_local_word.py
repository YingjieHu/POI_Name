
import textmining
import os, codecs
import scipy
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# a function for rendering the color of word clouds; no need to change
def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "rgb(0, 0, 128)" #% random.randint(60, 100)


# this function shows the local words of each metropolitan area as word clouds
def visualize_local_words_by_metro(poi_data_dir):
    tdm = textmining.TermDocumentMatrix() # this is from the text mining package
    
    # a dict used to store the POI names in a metro
    metro_dict = dict()
    metro_dict['az'] = ""
    metro_dict['il'] = ""
    metro_dict['nc'] = ""
    metro_dict['nv'] = ""
    metro_dict['oh'] = ""
    metro_dict['pa'] = ""
    metro_dict['wi'] = ""
    
    # a dict used to filter out repeating POI names
    metro_poi_dict = dict()
    metro_poi_dict['az'] = dict()
    metro_poi_dict['il'] = dict()
    metro_poi_dict['nc'] = dict()
    metro_poi_dict['nv'] = dict()
    metro_poi_dict['oh'] = dict()
    metro_poi_dict['pa'] = dict()
    metro_poi_dict['wi'] = dict()
    
    
    for fname in os.listdir(poi_data_dir):
        if fname == 'city_list.csv':
            continue
        
        fr = codecs.open(os.path.join(poi_data_dir, fname),'r','utf-8')
        
        city_name = fname.replace('.txt','')
        city_name = city_name.replace(' ','|')
        #print(city_name)
        metro_name = city_name.split(',')[1]
        if metro_name == 'sc':  # There is one city in SC, but it is very close to NC
            metro_name = 'nc'
        
        #POI_doc = ""
        
        for line in fr:
            line = line.replace(city_name,'')
            line = line.strip()
            if metro_poi_dict[metro_name].has_key(line):
                #print(line)
                continue
            else:
                metro_dict[metro_name] += " "+line
                metro_poi_dict[metro_name][line] = 0
            #POI_doc += " " + line
            
        fr.close()
        #POI_doc = POI_doc.strip()
        
    metro_name_list = list()
    
    for metro in metro_dict:
        tdm.add_doc(metro_dict[metro].strip().replace(u'\ufeff', ''))
        metro_name_list.append(metro)
        
    vocab_list = [] # a list for storing the vocabulary
    matrix_rows = [] # matrix for storing the count values
    is_first = True
    
    metro_vector_dict = dict() # this is a dictionary; given a city name, we can know it index in the matrix 
    for i in range(len(metro_name_list)):
        metro_vector_dict[metro_name_list[i]] = i
    
    # put the vocabulary and count values into variables
    for row in tdm.rows(cutoff=1):
        if is_first:
            vocab_list = row
            is_first = False
        else:
            matrix_rows.append(list(row))
            
    # calculate tf-idf
    binary_matrix = scipy.sign(matrix_rows)
    np_array = np.array(binary_matrix)
    term_count_vect = np.sum(np_array,0) # sum the binary matrix along columns
    term_percentage_vect = np.log((7.0  / term_count_vect)) 

    np_matrix_row = np.array(matrix_rows)
    tfidf =  np_matrix_row * term_percentage_vect  #np.log(np_matrix_row) *
    
    metro_local_dict = dict()
    for i in range(7):
        metro_local_dict[metro_name_list[i]] = dict()
        
        a = tfidf[i]
        top_index = sorted(range(len(a)), key=lambda i: a[i])[-100:]
        top_index = np.flip(top_index,0)
        
        top_words = ''
        word_frequencies = dict()
        for index in top_index:
            top_words += ' '+vocab_list[index]+":"+str(a[index])
            word_frequencies[vocab_list[index]] = np.log2(a[index])
            metro_local_dict[metro_name_list[i]][vocab_list[index]] = 0
               
        #print(metro_name_list[i]+": "+top_words.strip())
     
        wordcloud = WordCloud(width=350, height=300, margin=8, prefer_horizontal=1, background_color='white',max_font_size=50).generate_from_frequencies(word_frequencies, max_font_size=None)
         
        plt.figure()
        plt.imshow(wordcloud.recolor(color_func=grey_color_func), interpolation='bilinear')
        plt.axis("off")
        plt.show()
    



# This function finds the local terms by metro; it is the same function as the last one;
# However, instead of outputing word clouds, this function returns the local terms
def find_local_words_by_metro(poi_data_dir):
    tdm = textmining.TermDocumentMatrix() # this is from the text mining package
    
    # a dict used to store the POI names in a metro
    metro_dict = dict()
    metro_dict['az'] = ""
    metro_dict['il'] = ""
    metro_dict['nc'] = ""
    metro_dict['nv'] = ""
    metro_dict['oh'] = ""
    metro_dict['pa'] = ""
    metro_dict['wi'] = ""
    
    # a dict used to filter out repeating POI names
    metro_poi_dict = dict()
    metro_poi_dict['az'] = dict()
    metro_poi_dict['il'] = dict()
    metro_poi_dict['nc'] = dict()
    metro_poi_dict['nv'] = dict()
    metro_poi_dict['oh'] = dict()
    metro_poi_dict['pa'] = dict()
    metro_poi_dict['wi'] = dict()
    
    
    for fname in os.listdir(poi_data_dir):
        if fname == 'city_list.csv':
            continue
        
        fr = codecs.open(os.path.join(poi_data_dir, fname),'r','utf-8')
        
        city_name = fname.replace('.txt','')
        city_name = city_name.replace(' ','|')
        #print(city_name)
        metro_name = city_name.split(',')[1]
        if metro_name == 'sc':
            metro_name = 'nc'
        
        #POI_doc = ""
        
        for line in fr:
            line = line.replace(city_name,'')
            line = line.strip()
            if metro_poi_dict[metro_name].has_key(line):
                #print(line)
                continue
            else:
                metro_dict[metro_name] += " "+line
                metro_poi_dict[metro_name][line] = 0
            #POI_doc += " " + line
            
        fr.close()
        #POI_doc = POI_doc.strip()
        
    metro_name_list = list()
    
    for metro in metro_dict:
        tdm.add_doc(metro_dict[metro].strip().replace(u'\ufeff', ''))
        metro_name_list.append(metro)
        
    vocab_list = [] # a list for storing the vocabulary
    matrix_rows = [] # matrix for storing the count values
    is_first = True
    
    metro_vector_dict = dict() # this is a dictionary; given a city name, we can know it index in the matrix 
    for i in range(len(metro_name_list)):
        metro_vector_dict[metro_name_list[i]] = i
        
    
    # put the vocabulary and count values into variables
    for row in tdm.rows(cutoff=1):
        if is_first:
            vocab_list = row
            is_first = False
        else:
            matrix_rows.append(list(row))
            
            
    # calculate tf-idf
    binary_matrix = scipy.sign(matrix_rows)
    np_array = np.array(binary_matrix)
    term_count_vect = np.sum(np_array,0) # sum the binary matrix along columns
    term_percentage_vect = np.log((7.0  / term_count_vect)) 

    np_matrix_row = np.array(matrix_rows)
    tfidf =  np_matrix_row * term_percentage_vect  #np.log(np_matrix_row) *
    
    metro_local_dict = dict()
    for i in range(7):
        metro_local_dict[metro_name_list[i]] = dict()
        
        a = tfidf[i]
        top_index = sorted(range(len(a)), key=lambda i: a[i])[-100:]
        top_index = np.flip(top_index,0)
        
        top_words = ''
        word_frequencies = dict()
        for index in top_index:
            top_words += ' '+vocab_list[index]+":"+str(a[index])
            word_frequencies[vocab_list[index]] = np.log2(a[index])
            metro_local_dict[metro_name_list[i]][vocab_list[index]] = 0
               
        #print(metro_name_list[i]+": "+top_words.strip())
    
    return metro_local_dict    
#         wordcloud = WordCloud(width=350, height=300, margin=8, prefer_horizontal=1, background_color='white',max_font_size=50).generate_from_frequencies(word_frequencies, max_font_size=None)
#         
#         plt.figure()
#         plt.imshow(wordcloud.recolor(color_func=grey_color_func), interpolation='bilinear')
#         plt.axis("off")
#         plt.show()




# this function is to calculate the percentages of local term usage in the names of POI
# This function does this calculation for one POI type per time; the final results are combined into "word_metro_cate_usage_refined.csv" file
def check_metro_local_word_usage(poi_data_dir, metro_local_dict):
    metro_poi_total_count_dict = dict()
    metro_poi_local_count_dict = dict()
    
    # init
    for metro in metro_local_dict:
        metro_poi_total_count_dict[metro] = 0
        metro_poi_local_count_dict[metro] = 0
     
    # go through files in the folder   
    for fname in os.listdir(poi_data_dir):
        if fname == 'city_list.csv':
            continue
        
        fr = codecs.open(os.path.join(poi_data_dir, fname),'r','utf-8')
        
        city_name = fname.replace('.txt','')
        city_name = city_name.replace(' ','|')
        #print(city_name)
        metro_name = city_name.split(',')[1]
        if metro_name == 'sc':
            metro_name = 'nc'
        
        #POI_doc = ""
        
        for line in fr:
            metro_poi_total_count_dict[metro_name] += 1
            
            line = line.replace(city_name,'').replace(u'\ufeff', '')
            line = line.strip()
            splitted_words = line.split(' ')
            for word in splitted_words:
                word = word.strip()
                if metro_local_dict[metro_name].has_key(word):
                    metro_poi_local_count_dict[metro_name] += 1
                    break
                    
        fr.close()
       
        
    for metro_name in metro_poi_total_count_dict:
        print(metro_name+": "+str(metro_poi_local_count_dict[metro_name] * 1.0 / metro_poi_total_count_dict[metro_name]))
    


# main function            
if __name__ == "__main__":
    
    # if you would like to show word clouds
    #visualize_local_words_by_metro('../city_poi_by_type/AllCategory')
    
    #if you would like to calculate word usage percentages, use the following code.
    metro_local_dict = find_local_words_by_metro('../city_poi_by_type/AllCategory')
    check_metro_local_word_usage('../city_poi_by_type/Shopping', metro_local_dict)
    