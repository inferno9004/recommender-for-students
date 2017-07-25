
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pymysql
import math
#from sqlalchemy import create_engine
get_ipython().magic(u'matplotlib inline')


# In[2]:

import pymysql.cursors


# In[3]:

# connection = pymysql.connect(host= 54.191.229.32:22,
#                              user= 'ubuntu',
#                              password='capstone',
#                              db='db',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


# In[ ]:




# In[4]:

# q1 = '''

# Select userId, bankId, difficulty, sum(correct) as correct, 
# sum(incorrect) as incorrect, sum(blank) as blank, 
# sum(correct)*difficulty as score
# from(
# select a.userId, q.bankID, a.correct, a.incorrect, a.blank, q.difficulty 
# from isee_answers_2016.answers a
# 	, isee_webapp.questionSections qs
#     , isee_webapp.questions q
# where a.questionSectionId = qs.questionSectionId
# and qs.questionId = q.questionId
# and bankId <> 0) x
# group by bankId, userId
# ;

# '''


# In[5]:

# q2 = '''

# select d.userId,d.bankId, sum(d.total_score)as final_score from (select  c.userId, c.bankId, c.difficulty, 
# c.total_correct,c.total_incorrect,c.total_blank, 
# (c.total_correct*c.difficulty)/(c.total_correct+c.total_incorrect+c.total_blank) as total_score 
# from (select b.userId, b.bankId, b.difficulty,  
# sum(b.correct) as total_correct ,sum(b.incorrect) as total_incorrect 
# ,sum(b.blank)as total_blank 
# from (select a.userId, q.bankID, a.correct,  a.incorrect, a.blank, q.difficulty  
# from  isee_answers_2016.answers a inner join isee_webapp.questionSections qs 
# on a.questionSectionId = qs.questionSectionId 
# inner join isee_webapp.questions q 
# on qs.questionId = q.questionId where q.bankId <> 0)b group by 1,2,3) c)d
# group by 1,2


# '''


# In[6]:

# q3 = '''

# select b.userId, b.bankId, b.difficulty,b.total_correct,b.total_incorrect,b.total_blank, (b.total_correct + b.total_incorrect + b.total_blank) as total_qns_attempted from
# (select a.userId,a.bankID,a.difficulty,sum(a.correct) as total_correct,sum(a.incorrect) as total_incorrect,sum(a.blank) as total_blank from
# (select a.userId, q.bankID, a.correct,  a.incorrect, a.blank, q.difficulty  
# from  isee_answers_2016.answers a inner join isee_webapp.questionSections qs 
# on a.questionSectionId = qs.questionSectionId 
# inner join isee_webapp.questions q 
# on qs.questionId = q.questionId where q.bankId <> 0) a
# group by 1,2,3) b


# '''


# In[7]:

# #safe the result in a dataframe
# e_1 = create_engine('mysql+pymysql://root:Welcome_9@localhost:3306/isee_webapp')
# e_2 = create_engine('mysql+pymysql://root:Welcome_9@localhost:3306/isee_answers_2016')
# answer_df = pd.read_sql_query(q3, e_2)


# In[2]:

answer_df=pd.read_csv('data.csv')


# In[3]:

answer_df=answer_df.drop('Unnamed: 0', axis = 1)


# In[4]:

answer_df['score'] = answer_df["total_correct"]/answer_df["total_qns_attempted"] + ((answer_df["total_qns_attempted"].astype(int)//10)*0.05).round(2)


# In[5]:

answer_df["bank_diff"] = answer_df["bankId"].astype(str) + "_" + answer_df["difficulty"].astype(str)


# In[6]:

score_matrix = pd.pivot_table(answer_df
               ,values ='score'
               ,columns=['bank_diff']
               ,index = ['userId']
                )


# In[7]:

score_matrix.shape


# In[8]:

score_matrix.fillna(score_matrix.mean(), inplace=True)


# In[9]:

type(score_matrix)


# In[11]:

from scipy import spatial

dataSetI = score_matrix.ix[16657,:].tolist()
dataSetII = score_matrix.ix[16657,:].tolist()
result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
print result


# In[14]:

user_matrix = pd.DataFrame(index=score_matrix.index.tolist()[:101],columns=score_matrix.index.tolist())


# In[17]:

#user_matrix.set_value(8195,8195,1)


# In[18]:

#user_matrix


# In[11]:

from sklearn.metrics.pairwise import cosine_similarity


# In[21]:

#score_matrix.index.tolist()


# In[22]:

#score_dict = score_matrix.transpose().to_dict()


# In[23]:

#score_dict[8195]['104_1']


# In[24]:

#score_matrix.ix[16657,:].tolist()


# In[12]:

cosine_similarity(score_matrix.ix[16657,:].tolist(),score_matrix.ix[16657,:].tolist())[0][0]


# In[13]:

import itertools


# In[14]:

user_pairs = list(itertools.combinations(score_matrix.index.tolist(), 2))


# In[21]:

# x = {(i[0],i[1]: cosine_similarity(score_matrix.ix[16657,:].tolist(),score_matrix.ix[16657,:].tolist())[0][0]) for i in user_pairs}


# In[29]:

user_pairs[0]


# In[15]:

get_ipython().run_cell_magic(u'timeit', u'', u"for i in user_matrix.index.tolist():\n    for j in user_matrix.columns.tolist():\n        user_matrix.set_value(i,j,spatial.distance.cosine(score_matrix.ix[i,:].tolist(), score_matrix.ix[j,:].tolist()))\n        \nuser_matrix.to_csv('user.csv')")


# In[16]:

user_matrix


# In[47]:

# for i in user_pairs:
#     cosine_similarity(score_matrix.ix[i[0],:],)


# In[26]:

user_matrix.to_csv('cosine.csv')


# In[ ]:




# In[ ]:




# In[ ]:




# In[248]:

def selector(userid,n):
    
    user_test = answer_df[(answer_df['userId'] == userid)]
    top_df = user_test.sort_values('score', ascending=False).head(n/3)[['bankId','difficulty']]
    bottom_df = user_test.sort_values('score', ascending=False).tail(n/3)[['bankId','difficulty']]
    bottom_df['difficulty'] = bottom_df['difficulty'].apply(lambda x: x-1 if ((x == 2) |(x==3)) else x)
    top_df['difficulty'] = top_df['difficulty'].apply(lambda x: x+1 if ((x == 1) |(x==2)) else x)
    
    x = top_df.index.tolist()
    x.extend(bottom_df.index.tolist())
    user_test.drop(x, inplace = True)
    
    middle_df = user_test[["bankId","difficulty"]].sample(n = n -(n/3)-(n/3))
    
    return pd.concat([top_df,middle_df,bottom_df], axis=0)
    


# In[251]:

selector(11953,4)


# In[170]:

user_test = answer_df[(answer_df['userId'] == 10254)]


# In[177]:

top_df = user_test.sort_values('score', ascending=False).head(13)[['bankId','difficulty']]


# In[176]:

bottom_df = user_test.sort_values('score', ascending=False).tail(13)[['bankId','difficulty']]


# In[194]:

bottom_df['difficulty'] = bottom_df['difficulty'].apply(lambda x: x-1 if ((x == 2) |(x==3)) else x)


# In[195]:

top_df['difficulty'] = top_df['difficulty'].apply(lambda x: x+1 if ((x == 1) |(x==2)) else x)


# In[224]:

x = top_df.index.tolist()


# In[226]:

x.extend(bottom_df.index.tolist())


# In[229]:

user_test.drop(x, inplace = True)


# In[232]:

middle_df = user_test[["bankId","difficulty"]].sample(n = 13)


# In[233]:

middle_df


# In[238]:

pd.concat([top_df,middle_df,bottom_df], axis=0).shape


# In[9]:

q = '''
select a.answerId,a.userId,a.correct,a.incorrect,a.blank,a.duration, q.sectionId, s.sectionType from ssat_answers_2016.answers a 
join ssat_webapp.questionSections q 
on a.questionSectionId = q.questionSectionId 
left join ssat_webapp.sections s 
on s.sectionId = q.sectionId;

'''


# In[10]:

crosstab = pd.pivot_table(answer_df
               ,values ='final_score'
               ,columns=['bankId']
               ,index = ['userId']
                )


# In[11]:

crosstab.isnull().sum().sum()


# In[12]:

crosstab.to_csv('crosstab.csv')


# In[13]:

new_crosstab = pd.read_csv('crosstab.csv')


# In[14]:

new_crosstab.fillna(new_crosstab.mean(), inplace=True)


# In[15]:

new_crosstab.set_index(keys = 'userId', inplace=True)


# In[ ]:




# In[146]:

from sklearn.cluster import KMeans
cluster = KMeans(n_clusters = 70).fit(new_crosstab)


# In[153]:

centroids_df = pd.DataFrame(cluster.cluster_centers_)


# In[154]:

centroids_df.shape


# In[162]:

new_crosstab["cluster_label"] = pd.Series(cluster.labels_)


# In[169]:

del new_crosstab['cluster_label']


# In[173]:

new_crosstab.reset_index(inplace=True)


# In[177]:

new_crosstab['cluster_label'] = pd.Series(cluster.labels_)


# In[184]:

centroids_df

