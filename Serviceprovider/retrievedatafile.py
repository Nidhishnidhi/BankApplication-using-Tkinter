from Configuration import connectionsetupfile

def RetrieveDatabaseSize():
    count = 0
    try:
        status, value = connectionsetupfile.connection()
        
        databaseobj = value.database()
        data = databaseobj.child('BankAccount/PersonalData').get()
        
        for each_data in data:
            count += 1
        
        return count
    except:
        return count

def RetrieveUserData(Accountno):
    flag = 0
    status,value = connectionsetupfile.connection()
    userdata ={}
    
    databaseobj = value.database()
    
    data = databaseobj.child('BankAccount/PersonalData').get()
    for each_data in data:
        
        if(each_data.val()['AccountNumber'] == Accountno):
            userdata = each_data.val()
            
            flag = 1
            break
        
    if(flag == 1):
        return True,userdata
    
    else:
        return False,userdata
    
def RetrieveTransactionData(Accountno):
    flag = 0
    status,value = connectionsetupfile.connection()
    userdata = {}
    count = 0
    finaldata = {}
    
    databaseobj = value.database()
    
    data = databaseobj.child('BankAccount/Transaction_Data/'+Accountno+"/").get()
    for each_data in data:
    
        userdata[count] = each_data.val()
        count += 1
        flag = 1
        
    j = len(userdata)
    if(flag == 1):
        for i in range(5):
            finaldata[i] = userdata[j-1]
            j -= 1
            if(j == 0):
                break
        
        return True,finaldata
    
    else:
        
        return False,userdata
