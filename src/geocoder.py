
import codecs

from geopy.geocoders import GeoNames


def geocoding_cities():
    geolocator = GeoNames(username='yingjiehu')
    fw = codecs.open('../final_city_name_coords.csv','w','utf-8')
    with codecs.open('../final_city_name.csv','r','utf-8') as fr:
        for line in fr:
            this_city_name = line.strip()
            splitted = this_city_name.split(",")
            this_city_name_new = splitted[0].title()+", "+splitted[1].upper()
            location = geolocator.geocode(this_city_name_new)
            if location != None:
                #print(location.raw)
                #location = json.dumps(location.raw, encoding='utf-8')
                print(this_city_name +": "+ str(location.latitude) +", "+ str(location.longitude))
                fw.write(this_city_name+"|"+str(location.latitude)+"|"+str(location.longitude)+"\n")
            else:
                print(this_city_name+' not geocoded')
                fw.write(this_city_name+"||\n")
                            
    fw.close()


if __name__ == "__main__":
    geocoding_cities()
    