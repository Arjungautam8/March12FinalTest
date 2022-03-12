#!/usr/bin/env python
# coding: utf-8

# In[16]:


import re
import pandas as pd


# In[17]:


first_names = {}
last_names = {}


# In[18]:


def addFirstName(record):
    if pd.isna(record.firstname):
        return
    elif record.firstname in first_names:
        first_names.get(record.firstname).append(record.rownum)
    else:
        first_names[record.firstname] = [record.rownum]


# In[19]:


def addLastName(record):
    if pd.isna(record.lastname):
        return
    elif record.lastname in last_names:
        last_names.get(record.lastname).append(record.rownum)
    else:
        last_names[record.lastname] = [record.rownum]


# In[20]:


def addNamesToDatabase(record):
    addFirstName(record)
    addLastName(record)


# In[ ]:





# In[21]:


def removeEmailDomain(email):
    return email.split("@")[0]


# In[22]:


def getNameFromEmail(email):
        
    if "." in email:
        emailSplitted = email.lower().split(".")
        for key in first_names:
            if key in email:
                return key
        return emailSplitted[0]
    return ""


# In[23]:


def getLastNameFromEmail(email):
    if "." in email:
        emailSplitted = email.lower().split(".")
        for key in last_names:
            if key in email:
                return key
        return emailSplitted[1]
    return ""


# In[24]:


def getPatternCode(record,email):
    firstname = record.firstname
    lastname = record.lastname
    if (pd.isna(record.firstname)):
        firstname = getNameFromEmail(email)
    if (pd.isna(record.lastname)):
        lastname = getLastNameFromEmail(email)
    message = ""

    if email.lower() == firstname.lower():
        message = "<11>"
        return message
    elif email.lower() == lastname.lower():
        message = "<22>"
        return message
    elif "." in email:
        emailSplitted = email.lower().split(".")
        if firstname[:1] == emailSplitted[0][:1] and emailSplitted[0] != firstname.lower():
            message = "<1>"
        if emailSplitted[0].lower() == firstname.lower():
            message = message + "<11>"
        if emailSplitted[1].lower() == lastname.lower():
            message = message + ".<22>"
        elif " " in lastname or "-" in lastname:
            if " " in lastname:
                lastnamesplitted = lastname.lower().split(" ")
            else:
                lastnamesplitted = lastname.lower().split("-")

            if lastnamesplitted[0] in email:
                message = message + ".<20>"
            if lastnamesplitted[1] in email:
                message = message + ".<21>"
        return message
    elif "-" in email:
        emailSplitted = email.lower().split("-")
        if firstname[:1] == emailSplitted[0][:1] and emailSplitted[0] != firstname.lower():
            message = "<1>"
        if emailSplitted[0].lower() == firstname.lower():
            message = message + "<11>"
        if emailSplitted[1].lower() == lastname.lower():
            message = message + "-<22>"
        elif " " in lastname or "-" in lastname:
            if " " in lastname:
                lastnamesplitted = lastname.lower().split(" ")
            else:
                lastnamesplitted = lastname.lower().split("-")
            if lastnamesplitted[0] in email:
                message = message + "-<20>"
            if lastnamesplitted[1] in email:
                message = message + "-<21>"
        return message
 
    elif "_" in email:
        if firstname.lower()[:3] == email[:3].lower():
            message = message + "<11-f3l>"
        emailSplitted = email.lower().split("_")

        if emailSplitted[1] == record.lastname.lower():
            message = message + "<22>"
    elif firstname.lower()[:2] == email[:2] and email.lower() != firstname.lower():
        message = message + "<11-f21>"
        if lastname.lower() == email[2:].lower():
            message = message + "<22>"
    elif " " in lastname or "-" in lastname:
        if " " in lastname:
            lastnamesplitted = lastname.lower().split(" ")
        else:
            lastnamesplitted = lastname.lower().split("-")        
        if lastnamesplitted[0] in email:
            message = message + "<20>"
        if lastnamesplitted[1] in email:
            message = message + "<21>"
    elif firstname.lower()[:1] == email[:1] and firstname.lower() != email.lower() and not re.match(r"[.,-]",email):
        message = "<1>"
        if email[1:].lower() == lastname.lower():
            message = message + "<22>"        
        if email[1:].lower() == firstname.lower():
            message = message + "<11>"
    return message


# In[26]:


def main():

    # Read the csv file
    data = pd.read_csv('intelligentGuessingDataSet.csv')
    total_element = data.index.stop
    for i in range(0, total_element):
        addNamesToDatabase(data.iloc[i])
    result = []
    for i in range(0, total_element):
        message = getPatternCode(data.iloc[i], removeEmailDomain(data.iloc[i].email))
        result.append(message)
    new_dataframe = data.copy(deep = True)
    for i in range(0, total_element):
        new_dataframe.loc[i, "Email Pattern"] = result[i]
    
    new_dataframe.to_csv('problemSet1_submission.csv')

if __name__ == "__main__":
    main()


# In[ ]:




