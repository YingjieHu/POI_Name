# POI_Name_Analysis

* Author: Yingjie Hu
* Email: yjhu.geo@gmail.com



### Overall description 
This project provides the code for studying the names of Points of Interest (POI) and their changes with geographic distances. This GitHub repository is in companion with the published paper:

Hu, Y. & Janowicz, K. (2018): An empirical study on the names of points of interest and their changes with geographic distance, In: Proceedings of the 10th International Conference on Geographic Information Science (GIScience 2018), Aug. 29-31, Melbourne, Australia.

You can refer to this original paper for more details, and please feel free to re-use the code shared here for your own research projects. If you use the code, we would appreciate if you could cite our paper. Thank you!


### Dataset
The POI dataset used for this study is from Yelp, and can be downloaded here:  https://www.yelp.com/dataset . This study focuses on the seven metropolitan areas in the United States. The figure below provides a geographic visualization of the used POIs:
<p align="center">
<img align="center" src="https://github.com/YingjieHu/POI_Name/blob/master/fig/Figure2.png" width="600" />
</p>


### Repository organization
The "src" folder contains the source Python files for different functions. See the next section for detailed descriptions on these Python files.

The "city_poi_by_type" folder contains the POI names extracted from the original Yelp data (https://www.yelp.com/dataset). Within this folder, POI data are organized into different categories and then by cities or metropolitain areas. For example, there is a folder called "Automotive" which contains the POI names in different cities and each city is a separate file. There is also a folder called "Automotive_metro" which contains the POI names in different metros and each metro is a separate file. There are also two folders called "AllCategoy" and "AllCategory_metro" respectively, which contain the POIs in all categories. 

The "models" folder contains the trained word2vec model.


### Code function descriptions
This section provides descriptions for the source Python files. If you have questions on any of these files, please feel free to contact me at: yjhu.geo@gmail.com

"term_rank_frequency.py": Code in this file is to count the frequency of terms in POI names and output their ranks and frequencies. This file generates Figure 3(a) and Figure 3(b) in the GIScience paper for the exploratory analysis about Zipf's law. The code also outputs the top 10 most frequent terms in the POI names.

"metro_local_word.py": Code in this file identifies the local terms used in POI names for each metropolitan area, and then creates word clouds for each metropolitan area. Figure 4 in the paper is generated using this code. This file also provides the function for calculating the local term usage for each metropolitan area. Note that the related function will calculate the term usage for one POI type per action. Therefore, you need to execute the function 10 times, and manually combine the results. The current results are already combined in the file "word_metro_cate_usage_refined.csv".

"multiple_bar_chart.py": Code in this file creates the bar chart for the local term usage in different metropolitan areas. This is Figure 5 in the paper.

"distribution_divergence.py": Code in this file calculates the JSD among different metropolitan areas and finally calculate their average JSD.

"metro_countvector.py": Code in this file construct count-based vectors to represent each metropolitan area. This file also contains the functions that perform correlation analysis (Figure 6(a)) and generate similarity matrix (Figure 7(b)).

"metro_word2vec.py": Code in this file trains word2vec models using the library gensim (https://radimrehurek.com/gensim/models/word2vec.html). This file trains a word2vec model based on metropolitan areas and the POIs inside, and then correlates the collective similarity with distance. This code generates Figure 6(b) in the paper.

"geocoder.py": This file geo-locates the cities in the seven metropolitan areas in this POI dataset based on their names using the GeoNames API. The code opens a complete city list under the folder of "city_poi_by_type/AllCategory", and then geocodes each city in that file. Note: you will need to change the username from "demo" to your own GeoName API username.

"similarity_matrix.py": Code in this file generates the similarity matrices based on the geographic distances of the seven metropolitan areas and their POI name similarities based on word2vec. These generated figures are used in Figure 7 (a) and (c) in the published paper. These similarity matrices are also shown as below:
<p align="center">
<img align="center" src="https://github.com/YingjieHu/POI_Name/blob/master/fig/Similarity_metro.png" width="600" />
</p>

 
