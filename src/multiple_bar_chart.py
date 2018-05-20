
import numpy as np
import matplotlib.pyplot as plt

data = np.empty([7,10])

category_list = []
metro_list = []

i = -1
with open('../word_metro_cate_usage_refined.csv','r') as fr:
    for line in fr:
        splitted = line.split(',')
        if i== -1:
            for j in range(1,11):
                category_list.append(splitted[j].strip())
        else:
            metro_list.append(splitted[0])
            print(splitted[0])
            for j in range(1,11):
                data[i,j-1] = splitted[j]
            
        i += 1
            
       
    


#color_array =['aquamarine','#008080','#800080','#008000', '#000080','#CC6633','#99FF99','#9900CC','#3366FF','#CC3300']

color_array =['brown', 'indigo','green','coral','aquamarine','orange','darkblue','teal']
#'aquamarine','azure',

X = np.arange(10)
for i in range(7):
    plt.bar(X + 0.1*i, data[i], color = color_array[i], width = 0.1, label=metro_list[i])
    
# plt.bar(X + 0.00, data[0], color = 'b', width = 0.25)
# plt.bar(X + 0.25, data[1], color = 'g', width = 0.25)
# plt.bar(X + 0.50, data[2], color = 'r', width = 0.25)
axes = plt.gca()
axes.set_xlim([-0.5,10])
axes.set_ylim([0.0, 0.6])

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off


#plt.xlabel('POI Category')
plt.ylabel('Percentage of POI Names with Local Words')
plt.legend()
plt.show()