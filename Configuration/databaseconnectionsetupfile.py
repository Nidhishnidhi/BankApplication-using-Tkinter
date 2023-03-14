from firebase import firebase

def databaseconnection():
    
    try:
        objfirebase = firebase.FirebaseApplication("https://bankproject-614b4-default-rtdb.firebaseio.com")
        print("inside try")
        return objfirebase
    
    except:
        print("false")
        return "null"