# Suspicious Article Detector (SAD!)
#### By: Taylor Murphy, Neil Locketz

## Problem: 
Fake news is a problem that is endemic in the current political climate. Being able to detect fictitious news will help keep the public properly informed so that they can make decisions based on facts. These fake articles often use the same rhetorical structures, so theoretically they should be easily identifiable using modern machine learning techniques, such as neural networks.

## Data:
https://github.com/GeorgeMcIntire/fake_real_news_dataset
https://opendatascience.com/blog/how-to-build-a-fake-news-classification-model/ 

https://www.kaggle.com/mrisdal/fake-news/version/1
http://compsocial.github.io/CREDBANK-data/
http://www.opensources.co/ -> https://github.com/BigMcLargeHuge/opensources/blob/master/sources/sources.csv 
http://resources.mpi-inf.mpg.de/impact/web_credibility_analysis/README 

## Methods:
Current plan is to use a unidirectional LSTM on embeddings from Word2Vec
https://www.researchgate.net/publication/319306895_3HAN_A_Deep_Neural_Network_for_Fake_News_Detection
We are also going to compare results of a network run with just article text as input, and the results of a network which was run with article content as well as meta information about the webpage it was found on. Currently, most of these “fake news detectors” only do their classification based on the text of the article. We hypothesize that these results could be improved if we leverage the “sketchy website affect”.
Evaluation:
We are going to separate the datasets into development, test, and train sets. Evaluation will be performed on the development set while training. The final results will be collected using the test set. We are going to measure success using a confusion matrix, and F-score.

