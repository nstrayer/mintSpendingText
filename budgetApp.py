
# coding: utf-8

# In[1]:

import mintapi
mintPass = open('mintPassword.txt', 'r').readline().rstrip()
mailPass = open('emailPassword.txt', 'r').readline().rstrip()

mint = mintapi.Mint("nick.strayer@gmail.com", mintPass)


# In[2]:

transactions = mint.get_transactions()


# In[3]:


from datetime import date, timedelta 
#get the day and yesterday to find spending over the last day. 
yesterday = date.today() - timedelta(days=1)
dayBefore = yesterday - timedelta(days=1)


# In[4]:

mask = (transactions['date'] > dayBefore) & (transactions['date'] <= yesterday)
todaysSpending = transactions.loc[mask]
spent = todaysSpending.amount.sum()


# In[5]:

monthDays = [31,28,31,30,31,30,31,31,30,31,30,31] #days in the month
#            j  f  m  a  m  j  j  a  s  o  n  d
monthlySpending = 1000 #budget for non-rent costs per month. 
daysInMonth     = monthDays[yesterday.month-1] #grab how many days are in the month
dailySpending   = monthlySpending/daysInMonth #how much can I spend per day on average?


# # Stuff to send message

# In[6]:

import smtplib
import time
from time import gmtime, strftime, localtime

# Credentials 
username = 'nickSpendingApp'
password =  mailPass
fromaddr = 'nickSpendingApp'
toaddrs  = '7346450110@txt.att.net'


# In[7]:

def sendText(amount) :
    '''
    Function takes the dollar amount spent and sends a text message to me with it. 
    '''
    msg = ('\nYo\n You spent $ ' + str(amount) + ' yesterday.\n To meet your savings goal you should have spent less than ' + str(dailySpending) + '.')

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


# In[8]:

sendText(spent)

