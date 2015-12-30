#!/usr/bin/python

import mintapi
# A quick script to scape mint, figure out how much was spent the last day,
# then send that amount to the user in a text message.
# Written by Nick Strayer on Dec 23, 2015

#load in usernames and passwords.
mintPass      = open('mintPass.txt', 'r').readline().rstrip()
mintEmail     = open('mintEmail.txt', 'r').readline().rstrip()
mailPass      = open('mailPass.txt', 'r').readline().rstrip()
mailUsername  = open('mailUsername.txt', 'r').readline().rstrip()
phoneNumber   = open('phoneNumber.txt', 'r').readline().rstrip()

#log into mint
mint = mintapi.Mint(mintEmail, mintPass)

# Grab the the users transactions
transactions = mint.get_transactions()

#get the day and yesterday to find spending over the last day.
from datetime import date, timedelta
yesterday = date.today() - timedelta(days=1)
dayBefore = yesterday - timedelta(days=1)

# Ignore Chase Epay, transfer/credit card payment transactions, and rent payments.
typeMask = (transactions['description'] != "Chase Epay") & (transactions['description'] != "Bell Midtown Pmts") \
    & (transactions['category'] != "credit card payment") & (transactions['category'] != "transfer")

#First get rid of the transactions we don't want
totalSpending = transactions.loc[typeMask]

# Find what was spent yesterday.
timeMask = (totalSpending['date'] > dayBefore) & (totalSpending['date'] <= yesterday)

#Then filter to just yesterday
yesterdaysSpending = totalSpending.loc[timeMask]

#grab just the total of how much was spent.
spent = yesterdaysSpending.amount.sum()

monthDays = [31,28,31,30,31,30,31,31,30,31,30,31] #days in the month
#            j  f  m  a  m  j  j  a  s  o  n  d
monthlySpending = 1000 #budget for non-rent costs per month.
daysInMonth     = monthDays[yesterday.month-1] #grab how many days are in the month

#find how much has been spent this month so far.
beginingOfMonth = yesterday - timedelta(days= (yesterday.day - 1) )
monthMask       = (totalSpending['date'] > beginingOfMonth) & (totalSpending['date'] <= yesterday)
monthSpending   = totalSpending.loc[monthMask].amount.sum()

#Subtract this amount from my desired spending amount
budgetLeft = monthlySpending - monthSpending

#calculate how much on average I need to spend for the remaining days.
dailySpending = budgetLeft/(daysInMonth - yesterday.day)


# # Stuff to send message
import smtplib
import time
from time import gmtime, strftime, localtime


def sendText(amount) :
    '''
    Function takes the dollar amount spent and sends a text message to me with it.
    '''
    msg = ('You spent $' + str(amount) + ' yesterday.\n To meet savings goal you should spend less than $' + str(dailySpending) + ' for the rest of the month.')

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(mailUsername,mailPass)
    server.sendmail(mailUsername, phoneNumber, msg)
    server.quit()


#Send the text.
sendText(spent)
