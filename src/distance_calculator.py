
import codecs

from geopy.distance import vincenty


def calculate_distance_between_regions():
    city_list = list()
    
    with codecs.open('../final_city_name_coords_US_only.csv','r', 'utf-8') as fr:
        for line in fr:
            city_list.append(line.strip())
            
    fw = codecs.open('../final_city_name_dist_US_only.csv','w', 'utf-8')
    
    city_count = len(city_list)
    for i in range(city_count-1):
        for j in range(i+1, city_count):
            first_splitted = city_list[i].split("|")
            first_coord = (float(first_splitted[1]),float(first_splitted[2]))
            
            second_splitted = city_list[j].split("|")
            second_coord = (float(second_splitted[1]),float(second_splitted[2]))
            
            distance = vincenty(first_coord, second_coord).miles
            
            fw.write(first_splitted[0]+'|'+second_splitted[0]+"|"+str(distance)+"\n")
            
    fw.close()


if __name__ == "__main__":
    calculate_distance_between_regions()
    