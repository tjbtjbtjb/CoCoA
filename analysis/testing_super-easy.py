#!/usr/bin/env python
# coding: utf-8

# # Consolidated test notebook

# In[202]:


import sys
sys.path.insert(1, '..')
import cocoa.cocoa as cc


# In[203]:


help(cc)


# In[204]:


help(cc.get)


# In[205]:


cc.get(where='Spain',which='confirmed',what='Diff')


# In[209]:


cc.plot(where=['France','Italy'],which='confirmed',what='Cumul') # Caution, Cumul will become cumul (lower case)


# In[199]:


cc.listwhat()


# In[200]:


cc.listwhom()


# In[210]:


cc.listwhich()


# In[201]:


cc.setwhom('JHU')


# # Sandbox

# In[144]:


from importlib import reload


# In[196]:


reload(cc)


# In[198]:


cc.plot(where='France',which='deaths',what='Cumul')


# In[186]:


import cocoa.covid19 as coco


# In[194]:


reload(coco)


# In[195]:


mydb=coco.db('JHU')
mydb.getFields()


# In[150]:


help(cc)


# In[82]:


import pandas as pd
ts = pd.Series(z.cases.to_numpy(), index=z.date)
type(ts)


# In[84]:


ts1=pd.Series(z[z.country=="Spain"].cases.to_numpy(), index=z[z.country=="Spain"].date)
ts2=pd.Series(z[z.country=="Italy"].cases.to_numpy(), index=z[z.country=="Italy"].date)


# In[92]:


zz=pd.DataFrame({"country":z.country.unique(),"ts":[ts1,ts2]})
zz.head()


# In[98]:


from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot
from bokeh.io import show, output_notebook
output_notebook()


# In[99]:


fig=figure()


# In[110]:


fig.line(x='date',y='cases',source=z)
show(fig)


# # Other stuff. Oliv' branch

# In[ ]:




