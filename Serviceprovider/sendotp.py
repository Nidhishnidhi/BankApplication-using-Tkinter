import random
from tkinter import messagebox
import requests
import json

def sotp(a,phno):
    try:
        url = "https://www.fast2sms.com/dev/bulk"
        #generate the credentials
        mydata = {'sender_id':'FSTSMS',
                  'message':a,
                  'language':'english',
                  'route':'p',
                  'numbers':phno}
        
        #step3:validate the credentials
        headers = {'authorization':'ZLod1WikfVUYsxSqIm2vMFBrp7cwnT9j4gX5uDhPl6JRetK0AyyAE749QGd2wkVPITcBLe5aHqlxrpuz',
                   'Content-Type':"application/x-www-form-urlencoded",
                   'Cache-Control':'no-cache'}
        #send sms
        response = requests.request("post", url, data=mydata,headers=headers)
        return True
    
    except:
        return False
    
    
    
'''
def forgotpass():
            
    def sendotp():
        
        def val(otp_number):
            motp = otp_number
            uotp = userotp.get()
            
            if(int(motp) != int(uotp)):
                messagebox.showwarning('warning','Invalid OTP')
            
            else:
                messagebox.showinfo('Success','OTP Verified')
                messagebox.showinfo("success","Userid and password is sent to"+phno)
                
                
        phno = en1.get()
        

        status=0
        for row in range(n_row):
            dphone = sh.cell_value(row,2)
            
            if(dphone == phno):
                status=1
                
        if(status==1):
            otp_number = str(random.randint(1000, 9999))
            a="your otp number for forgot password"+otp_number
            sotp(a,phno)
            print(otp_number)
            
            def kill():
                messagebox.showwarning('warning','Session Expired')
                fframe.place_forget()
                lframe.place(x=400,y=50,height=600,width=500)
            
            #start timer
            w.after(30000,kill)
            
            #validate otp
            olabel = Label(fframe,text="Enter your otp")
            olabel.place(x=10,y=190)
            
            userotp = Entry(fframe)
            userotp.place(x=10,y=230)
            
            validate = Button(fframe,text="validate",command=lambda:val(otp_number))
            validate.place(x=10,y=280)
            
            m,n = sendup(phno)
            b = "your user id is "+m+" your password is"+n
            sotp(b,phno)
            
        else:
            messagebox.showwarning('sotp('otp is 345','8088254918')'''
