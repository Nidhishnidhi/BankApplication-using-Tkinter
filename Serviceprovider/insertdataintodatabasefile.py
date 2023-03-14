from Configuration import databaseconnectionsetupfile

def insertdetail(userdata):
    objfirebase = databaseconnectionsetupfile.databaseconnection()

    objfirebase.post('BankAccount/PersonalData',userdata)
    
    return True
 
   
def inserteachuserdata(accountno,transactiondata):

    objfirebase = databaseconnectionsetupfile.databaseconnection()
    
    try:
        objfirebase.post('BankAccount/Transaction_Data/'+accountno+'/',transactiondata)
        return True
    
    except:
        return False
