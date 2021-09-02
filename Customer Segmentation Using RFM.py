#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


pd.set_option("display.max_columns" , None)
pd.set_option("display.float_format" , lambda x : "%.4f" % x)
pd.set_option("display.width" , 200)


# In[3]:


from warnings import filterwarnings
filterwarnings("ignore")


# In[4]:


path= "/Users/gokhanersoz/Desktop/VBO_Dataset/online_retail_II.xlsx"


# In[5]:


online_retail = pd.read_excel(path ,sheet_name = "Year 2010-2011")


# # Mission 1:
# 
# ### Understanding and Preparing Data
# 
# ### 1. Read the 2010-2011 data in the OnlineRetail II excel. Make a copy of the dataframe you created. 

# In[6]:


df = online_retail.copy()
df.head()


# In[7]:


df.ndim


# ### 2. Examine the descriptive statistics of the dataset.

# In[8]:


def check_dataframe(dataframe, head = 5 , tail = 5):
    
    print(" head ".upper().center(50,"#"),end="\n\n")
    print(dataframe.head(head),end="\n\n")
    
    print(" tail ".upper().center(50,"#"),end="\n\n")
    print(dataframe.tail(tail),end="\n\n")
     
    print(" ndim ".upper().center(50,"#"),end="\n\n")
    print(f"{dataframe.ndim} Dimension",end="\n\n")
          
    print(" dtypes ".upper().center(50,"#"),end="\n\n")
    print(dataframe.dtypes,end="\n\n")
          
    print(" ınfo ".upper().center(50,"#"),end="\n\n")
    print(dataframe.info(),end="\n\n")
          
    print(" na ".upper().center(50,"#"),end="\n\n")
    print(dataframe.isnull().sum(),end="\n\n")
          
    print(" describe ".upper().center(50,"#"),end="\n\n")
    print(dataframe.describe([0.01,0.99]).T)


# In[9]:


check_dataframe(df)


# ### 3. Are there any missing observations in the dataset? If yes, how many missing observations in each variable?

# In[10]:


na = df.isnull().sum()
na = pd.DataFrame(na[na>0], columns = ["NA Values"]).T
na_names = na.columns
na


# In[11]:


plt.figure(figsize = (10,7))
data = df.isnull()[na_names]

sns.heatmap(data = data , cmap = "viridis",yticklabels=False)
plt.ylabel("Na Values")
plt.show()


# ### 4. Remove the missing observations from the data set. Use the 'inplace=True' parameter for removal.

# In[12]:


df.describe([0.01, 0.99]).T


# In[13]:


df.dropna(inplace = True)
df.isnull().sum()


# In[14]:


df.describe([0.01, 0.99]).T


# ### 5. How many unique items are there?

# In[15]:


for col in df.columns :
    print(f"For {col.upper()} Nunique Values : {df[col].nunique()}",end = "\n\n")


# In[16]:


# Target Values

items = "StockCode"
print(f"For {items.upper()} Nunique Values : {df[items].nunique()}")


# ### 6. How many of each product are there?

# In[17]:


target = df[items].value_counts()
target = pd.DataFrame(target).reset_index()
target.columns = ["StockCode", "Values"]
target.head(10)


# ### 7. Sort the 5 most ordered products from most to least.

# In[18]:


five_values = df.groupby(["StockCode"])[["Quantity"]].sum().sort_values(by = "Quantity" , ascending = False)
five_values.head()


# In[19]:


target.sort_values(by ="Values" , ascending = False).head()


# ### 8. The 'C' in the invoices shows the canceled transactions. Remove the canceled transactions from the data set.

# In[20]:


print(f"DataFrame Shape : {df.shape}")


# In[21]:


df["Invoice"].str.contains("C", na = None).head(3)


# In[22]:


df["Invoice"].str.contains("C" , na = False).head(3)


# In[23]:


# The reason we set na = False would normally return None if na = None. 
# We fill them with False instead, which we convert to True with "~" and catch them.

df = df[~df["Invoice"].str.contains("C", na = False )]
print(f"DataFrame Shape : {df.shape}")


# ### 9. Create a variable named 'Total Price' that represents the total earnings per invoice.

# In[24]:


df.head()


# In[25]:


df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()


# ## Mission 2:
# 
# ## Calculation of RFM metrics
# 
# ▪ Make the definitions of Recency, Frequency and Monetary.
# 
# ▪ Customer specific Recency, Frequency and Monetary metrics with groupby, agg and lambda
# calculate.
# 
# ▪ Assign your calculated metrics to a variable named rfm.
# 
# ▪ Change the names of the metrics you created to recency, frequency and monetary.
# 
# Note 1: For the recency value, accept today's date as (2011, 12, 11).
# 
# Note 2: After creating the rfm dataframe, filter the dataset to "monetary>0".

# In[26]:


df["InvoiceDate"].max()


# In[27]:


# We looked at a max value and added 2 days on top of it....

import datetime
today_date = datetime.datetime(2011,12,11)
today_date


# In[28]:


rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda InvoiceDate : (today_date - InvoiceDate.max()).days,
                                    "Invoice" : lambda Invoice : Invoice.nunique(),
                                    "TotalPrice" : lambda TotalPrice : TotalPrice.sum()})


# In[29]:


rfm.head()


# In[30]:


# Control 

values = 12346.0000

print("Invoice : " , df[df["Customer ID"] == values]["Invoice"].nunique(),end = "\n\n")

print("InvoiceDate : " , (today_date - df[df["Customer ID"] == values]["InvoiceDate"].max()).days,end="\n\n")

print("TotalPrice : " , df[df["Customer ID"] == values]["TotalPrice"].sum(),end = "\n\n")


# In[31]:


rfm.columns = ["Recency", "Frequence", "Monetary"]
rfm.head()


# In[32]:


#We caught the min value of the monetary value as 0 here, we need to fix it...
rfm.describe().T


# In[33]:


rfm = rfm[rfm["Monetary"] > 0]
rfm.describe().T


# ## Mission 3:
# ### Generating and converting RFM scores to a single variable
# 
# ▪ Convert Recency, Frequency and Monetary metrics to scores between 1-5 with the help of qcut.
# 
# ▪ Record these scores as recency_score, frequency_score and monetary_score.
# 
# ▪ Express recency_score and frequency_score as a single variable and save as RFM_SCORE.
# 
# CAUTION! We do not include monetary_score.

# In[34]:


# If we pay attention to the frequency here, the same values appear in different quarters 
#and this will cause a problem, so we will use rank(method = "first")

values = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
rfm.describe(values).T


# In[35]:


# For the Recency value, the scoring should be in reverse, the lowest value being the highest
# [(0.999, 13.8] < (13.8, 33.0] < (33.0, 72.0] < (72.0, 180.0] < (180.0, 374.0]] ranges

rfm["Recency_Score"] = pd.qcut(rfm.Recency, 5, labels = [5,4,3,2,1])


# In[36]:


pd.DataFrame(rfm.Frequence.rank(method="first").describe(values)).T


# In[37]:


# We will use the rank method for the frequency value as it captures the same values in different quarters

# Note: We don't need to take it backwards here, anyway, the biggest area gets the highest score...

# [(0.999, 868.4] < (868.4, 1735.8] < (1735.8, 2603.2] < (2603.2, 3470.6] < (3470.6, 4338.0]] ranges

rfm["Frequence_Score"] = pd.qcut(rfm.Frequence.rank(method="first"), 5 , labels = [1,2,3,4,5])


# In[38]:


# The one with the highest Monetary value has the highest score...

#[(3.749, 250.194] < (250.194, 490.096] < (490.096, 942.276] <(942.276, 2058.426] <(2058.426, 280206.02]] ranges

rfm["Monetary_Score"] = pd.qcut(rfm.Monetary, 5 , labels = [1,2,3,4,5])


# In[39]:


rfm.head()


# In[40]:


rfm["RFM_SCORE"] = rfm["Recency_Score"].astype(str) + rfm["Frequence_Score"].astype(str)
rfm.head()


# In[41]:


# Champions

rfm[rfm["RFM_SCORE"] == "55"]["RFM_SCORE"].count()


# In[42]:


# Hiberneating

rfm[rfm["RFM_SCORE"] == "11"]["RFM_SCORE"].count()


# ## Mission 4:
# 
# ### Defining RFM scores as segments
# 
# ▪ Make segment definitions so that the generated RFM scores can be explained more clearly.
# 
# ▪ Convert the scores into segments with the help of the seg_map below.

# In[43]:


seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


# In[44]:


# Here, when the regex is False, it does not detect [1-2][1-2] values, only 33,41,51 values.
# We make it detect all of them by making Regex True
rfm["Segment"] = rfm["RFM_SCORE"].replace(seg_map , regex = True)
rfm.head()


# In[45]:


plt.figure(figsize = (15,5))
i = 1
for col in ["Recency","Frequence","Monetary"]:
    plt.subplot(1,3,i)
    sns.distplot(rfm[col])
    i+=1
    
plt.tight_layout()
plt.show()


# In[46]:


plt.figure(figsize = (15,5))
i = 1
for col in ["Recency","Frequence","Monetary"]:
    plt.subplot(1,3,i)
    sns.distplot(np.log1p(rfm[col]))
    i+=1
    
plt.tight_layout()
plt.show()


# In[47]:


plt.figure(figsize = (15,10))

sns.scatterplot(x = rfm["Recency"], y = rfm["Frequence"] , hue=rfm["Segment"])

size = 15
plt.xlabel("Recency" , fontsize = size)
plt.ylabel("Frequence", fontsize = size)
plt.title("Frequence ~ Recency" ,fontsize = size)
plt.show()


# ### Mission 5:
# 
# ### Time for action!
# 
# ▪ Select the 3 segments you find important. These three segments;
# 
#      - Both in terms of action decisions,
# 
#      - Interpret both in terms of the structure of the segments (mean RFM values).
# 
# ▪ Select the customer IDs of the "Loyal Customers" class and get the excel output.

# In[48]:


segment_names = rfm["Segment"].unique().tolist()
for name in segment_names:
    print(f" For { name } Describe ".upper().center(50,"#"),end = "\n\n")
    
    print(pd.DataFrame(data = rfm[rfm["Segment"] == name].describe().T), end = "\n\n")


# In[49]:


segment = rfm["Segment"].value_counts()
segment = pd.DataFrame(segment).sort_values(by = "Segment" , ascending = False)
segment


# In[50]:


rfm[["Segment","Frequence","Recency","Monetary"]].groupby("Segment").agg(["mean","count"])


# ### Champions Class
# 
# * This class is the class that brings the most returns. He sees that he is logged in frequently according to his recency value. His Frequence value is higher than the others, which makes this class Champions. By creating more opportunities for them, we can increase their monetary value even more...
# 
# ### Loyal Customers
# 
# * We can organize special campaigns to attract this class to the champions class and increase their returns to us more.
# 
# ### Can't Loose
# 
# * These customers are more when we compare their frequencies with loyal customers, but the difference between them is very high, they are close to each other in terms of return, it may be a plus for us to be in contact with them so that they can visit more often in order not to keep them away. Campaigns can be organized according to what they are more interested in...

# ### Select the customer IDs of the "Loyal Customers" class and get the excel output.

# In[51]:


loyal_customers = pd.DataFrame()
loyal_customers["Loyal_Customers_ID"] = rfm[rfm["Segment"] == "loyal_customers"].index
loyal_customers.to_excel("loyal_customers_id.xlsx")


# In[52]:


print("Loyal Customers Shape : {}".format(loyal_customers.shape))


# In[53]:


loyal_customers.head()


# In[ ]:




