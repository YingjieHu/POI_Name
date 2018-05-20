
import codecs
from geopy.geocoders import GeoNames

# This function geocodes the city names using the GeoNames API
def geocoding_cities():
    geolocator = GeoNames(username='demo')
    # output file
    fw = codecs.open('../city_coords_AllCategories.csv','w','utf-8')
    #read from the city list
    with codecs.open('../city_poi_by_type/AllCategory/city_list.csv','r','utf-8') as fr:
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
    