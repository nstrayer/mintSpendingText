# A quick script to scape mint, figure out how much was spent the last day,
# then send that amount to the user in a text message.
# Written by Nick Strayer on Dec 23, 2015

import mintapi

#load in usernames and passwords.
mintPass      = open('mintPass.txt', 'r').readline().rstrip()
mintEmail     = open('mintEmail.txt', 'r').readline().rstrip()
mailPass      = open('mailPass.txt', 'r').readline().rstrip()
mailUsername  = open('mailUsername.txt', 'r').readline().rstrip()
phoneNumber   = open('phoneNumber.txt', 'r').readline().rstrip()

#log into mint
mint     = mintapi.Mint(mintEmail, mintPass)

# Grab the the users transactions
transactions = mint.get_transactions()

#get the day and yesterday to find spending over the last day.
from datetime import date, timedelta
yesterday = date.today() - timedelta(days=1)
dayBefore = yesterday - timedelta(days=1)

# Find what was spent yesterday
mask = (transactions['date'] > dayBefore) & (transactions['date'] <= yesterday)
todaysSpending = transactions.loc[mask]
spent = todaysSpending.amount.sum()


monthDays = [31,28,31,30,31,30,31,31,30,31,30,31] #days in the month
#            j  f  m  a  m  j  j  a  s  o  n  d
monthlySpending = 1000 #budget for non-rent costs per month.
daysInMonth     = monthDays[yesterday.month-1] #grab how many days are in the month
dailySpending   = monthlySpending/daysInMonth #how much can I spend per day on average?


# # Stuff to send message
import smtplib
import time
from time import gmtime, strftime, localtime


def sendText(amount) :
    '''
    Function takes the dollar amount spent and sends a text message to me with it.
    '''
    msg = ('\nHey Nick,\n You spent $' + str(amount) + 'yesterday.\n To meet your savings goal you should have spent less than ' + str(dailySpending) + '.')

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(mailUsername,mailPass)
    server.sendmail(mailUsername, phoneNumber, msg)
    server.quit()


#Send the text.
sendText(spent)
