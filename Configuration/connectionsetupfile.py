from firebase import firebase
import pyrebase

def connection():
    try:
       
        firebaseConfig = {
          'apiKey': "AIzaSyCfrb3TdrtrpBwwved9ery0eJ6w_Me8gmc",
          'authDomain': "bankproject-614b4.firebaseapp.com",
          'databaseURL': "https://bankproject-614b4-default-rtdb.firebaseio.com",
          'projectId': "bankproject-614b4",
          'storageBucket': "bankproject-614b4.appspot.com",
          'messagingSenderId': "257297997522",
          'appId': "1:257297997522:web:9beaa43b8fa06a3daad70b",
          'measurementId': "G-QY9H465WC6"
        }
        
        
        firebase = pyrebase.initialize_app(firebaseConfig)
        
        return True,firebase
    
    except:

        return False,"null"