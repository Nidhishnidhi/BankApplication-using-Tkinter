from tkinter import *
from Configuration import connectionsetupfile,databaseconnectionsetupfile
from Serviceprovider import retrievedatafile,insertdataintodatabasefile,sendotp
from tkinter import messagebox
import random
from datetime import datetime
from PIL import Image, ImageTk
from fpdf import FPDF
newaccountnumber = " "
generated_otp = 0

'''************************************************************************Ministatement Function******************************************************'''
def ministatementfunction():
    status,userdata = retrievedatafile.RetrieveTransactionData(AccountNumberEntry.get())
    
    if(status):
        pdf = FPDF()
     
        pdf.add_page()
       
        pdf.set_font("Arial", size = 10)
        pdf.cell(200,10,txt = str(userdata[0]['AccountNumber']), align ="C")
        
        for i in range(len(userdata)):
            pdf.cell(200, 40, txt = "Transaction"+str(i+1)+": ",ln = i+1 ,align = 'L')
            pdf.cell(200, 10, txt = str(userdata[i]['Message']),ln = i+1 ,align = 'C',)
    
        # save the pdf with name .pdf
        
        pdf.output(AccountNumberEntry.get()+".pdf") 


def uploadtotransactiondata(message):
    print("inside uploadtransactiondata")
    transactiondata = {'AccountNumber':AccountNumberEntry.get(),
                'Message':message}
    
    status = insertdataintodatabasefile.inserteachuserdata(AccountNumberEntry.get(), transactiondata)

    if(status):
        print("Transaction data is uploaded")

    else:
        print("Transaction data not uploaded")




'''**************************************************************************TransferAmount Function**********************************************'''
def transferamountfunction():
    ActionFrame.place_forget()
    TransferAmountFrame.place(x=400,y = 50,height = 750,width = 800)
    
def transferamount():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    newstatus,newuserdata = retrievedatafile.RetrieveUserData(transferaccountnoentry.get())
    
    if(AccountNumberEntry.get() != transferaccountnoentry.get()):
        if(newstatus):
            connectionstatus, value = connectionsetupfile.connection()
            database_obj = value.database()
            udata = database_obj.child('BankAccount/PersonalData').get()
    
            if int(userdata['Balance']) >= 1000 and int(transferamountentry.get()) <= int(userdata['Balance']) - 1000:
                flag = 0
                for each_data in udata:
                    db_Accountno = each_data.val()['AccountNumber']
                    if(db_Accountno == transferaccountnoentry.get()):
                        if(int(userdata['Balance']) > int(transferamountentry.get())):
                            database_obj.child("Account/PersonalData").child(each_data.key()).update({'Balance':int(newuserdata['Balance']) + int(transferamountentry.get())})
                            flag = 1
                        
                if(flag == 1):
                    for each_data in udata:
                        db_Accountno = each_data.val()['AccountNumber']
                        if(db_Accountno == AccountNumberEntry.get()):
                            database_obj.child("BankAccount/PersonalData").child(each_data.key()).update({'Balance':int(userdata['Balance']) - int(transferamountentry.get())})
                            messagebox.showinfo("Success","Amount Transfered Successfully")
                            message = "From Acc No: "+str(AccountNumberEntry.get())+" "+str(transferamountentry.get())+" is transfered to Acc No:"+str(transferaccountnoentry.get())+" "+str(datetime.now())
                            uploadtotransactiondata(message)
                            TransferAmountFrame.place_forget()
                            ActionFrame.place(x=400,y=50,height = 750,width = 800)
            else:
                messagebox.showerror("Error","Insuffient balance")
                TransferAmountFrame.place_forget()
                ActionFrame.place(x=400,y=50,height = 750,width = 800)
            
            
        else:
            messagebox.showerror("Error","Account Doesn't Exist")
    
    else:
        messagebox.showerror("Error","Can't transfer Amount to same account")
                

'''**************************************************************************ChangePIN function************************************************'''
def changepinfunction():
    ActionFrame.place_forget()
    ChangePinFrame.place(x= 400, y = 50 ,height = 750,width = 800)
    
def validatePIN():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    
    if(int(userdata['Password']) == int(oldpinentry.get())):
        if(int(newpinentry.get()) == int(confirmpinentry.get())):
            if(int(newpinentry.get()) != int(oldpinentry.get())):
                connectionstatus, value = connectionsetupfile.connection()
                database_obj = value.database()
                udata = database_obj.child('BankAccount/PersonalData').get()
    
                flag = 0
                for each_data in udata:
                    db_Accountno = each_data.val()['AccountNumber']
                    if(db_Accountno == AccountNumberEntry.get()):
                       
                        database_obj.child("BankAccount/PersonalData").child(each_data.key()).update({'Password':int(confirmpinentry.get()) })
                        messagebox.showinfo("success","Pin Changed Successfully")
                        ChangePinFrame.place_forget()
                        ActionFrame.place(x=400,y=50,height = 750,width = 800)
            else:
                messagebox.showerror("Error","New pin cannot be old pin")
        else:
            messagebox.showerror("Error","Confirm Password doesnt match New Password")
    else:
        messagebox.showerror("Error","Wrong PIN")
            



'''*************************************************************************Deposit Function***************************************************'''
def depositfunction():
    ActionFrame.place_forget()
    DepositFrame.place(x=400,y=50,height = 750,width = 800)

def addamount():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    available_balance = int(userdata['Balance'])
    
    
    updatedbalance = int(rupeeentry.get())
    status, value = connectionsetupfile.connection()
    database_obj = value.database()
    udata = database_obj.child('BankAccount/PersonalData').get()

    flag = 0
    for each_data in udata:
        db_Accountno = each_data.val()['AccountNumber']
        if(db_Accountno == AccountNumberEntry.get()):
           
            database_obj.child("BankAccount/PersonalData").child(each_data.key()).update({'Balance':updatedbalance + available_balance })
            messagebox.showinfo("success","Deposit successful")
            message = "Amount "+str(updatedbalance)+" is deposited at "+str(datetime.now())
            uploadtotransactiondata(message)
            DepositFrame.place_forget()
            ActionFrame.place(x=400,y=50,height = 750,width = 800)
        
    

'''************************************************************************Show balance********************************************************'''
def showbalance():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    
    messagebox.showinfo("Balance","Available balance:"+str(userdata['Balance']))

'''*************************************************************************Withdraw function***************************************************'''
def withdrawfunction():
    ActionFrame.place_forget()
    WithdrawFrame.place(x=400,y = 50,height =750,width = 800)
    
def deductamount():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    amount = int(AmountEntry.get())
        
    balance = int(userdata['Balance'])
    if(balance >= (amount+500)):
        balance -= amount
        
        status, value = connectionsetupfile.connection()
        database_obj = value.database()
        udata = database_obj.child('BankAccount/PersonalData').get()

        for each_data in udata:
            db_Accountno = each_data.val()['AccountNumber']
            if(db_Accountno == AccountNumberEntry.get()):
                
                database_obj.child("BankAccount/PersonalData").child(each_data.key()).update({'Balance': balance})
                messagebox.showinfo("Withdraw","Amount withdrawn:"+str(amount))
                message = "Amount "+str(amount)+" is debited at "+str(datetime.now())
                uploadtotransactiondata(message)
                WithdrawFrame.place_forget()
                ActionFrame.place(x=400,y=50,height = 750,width = 800)
                
    else:
        messagebox.showwarning("warning","Insufficient Balance")
    
'''************************************************************************After Login******************************************************'''
def afterlogin():
    NewUserFrame.place_forget()
    ActionFrame.place(x=400,y=50,height = 750,width = 800)



'''***********************************************************************Validate OTP******************************************************'''
def validateotp():
    global generated_otp
    
    if(str(generated_otp) == OTPEntry.get()):
        Login['state'] = NORMAL
        
    else:
        messagebox.showerror("Error","Invalid OTP")
    
   
'''***********************************************************************Resend OTP***********************************************************'''
def resendOTP():
    global generated_otp
    generated_otp = random.randint(1000,9999)
    print(generated_otp)
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    otpstatus = sendotp.sotp(generated_otp,userdata['Phone'])
    ResendOTP['state'] = DISABLED
   
'''**********************************************************************Send OTP*************************************************************'''
def send_otp():
    global generated_otp
    generated_otp = random.randint(1000,9999)
    print(generated_otp)
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    otpstatus = sendotp.sotp(generated_otp,userdata['Phone'])
    if(otpstatus):
        messagebox.showinfo("success","OTP sent successfully")
        OTPEntry.place(x=20,y=290,width =200)
        SendOTP['state'] = DISABLED
        AuthenticatePin['state'] = DISABLED
        ResendOTP['state'] = NORMAL
        ValidateOTP['state'] = NORMAL
        
    ResendOTP.configure(command = resendOTP)

'''***********************************************************************Upload Data****************************************************'''
def uploaddata():
    tempkey = random.randint(1000,9999)
    UserData = {'AccountNumber':newaccountnumber,
                'Name':NameEntry.get(),
                'Phone':PhoneEntry.get(),
                'Balance':InitialAmountEntry.get(),
                'Password':tempkey}
    
    
    otpstatus = sendotp.sotp(tempkey, PhoneEntry.get())
    
    if(otpstatus):
        messagebox.showinfo("Success","Temporary Pin is sent to your Phone number "+str(PhoneEntry.get()))
    
    status = insertdataintodatabasefile.insertdetail(UserData)

    if(status):
        messagebox.showinfo("Success","Account Created Successfully")
        NewUserFrame.place_forget()
        MainFrame.place(x=400,y=50,height = 750,width = 800)
        
    else:
        messagebox.showerror("Error","Account not created")

'''**********************************************************************New User Function****************************************************'''
def NewUser():
    global newaccountnumber
    NewUserFrame.place(x=400,y=50,height = 750,width = 800)
    
    count = retrievedatafile.RetrieveDatabaseSize()
    #count = 0
    
    newaccountnumber = "Nidhi"+str(int(10000)+count)
    
    GeneratedAccountNumber.configure(text = newaccountnumber)
    
'''**********************************************************************Authenticate Password***********************************************'''
def AuthenticatePassword():
    status,userdata = retrievedatafile.RetrieveUserData(AccountNumberEntry.get())
    print(PinEntry.get())

    if(status):
        if(int(userdata['Password']) == int(PinEntry.get())):
            SendOTP['state'] = NORMAL
        
        else:
            messagebox.showerror("Error","InvalidPin")
    else:
        messagebox.showwarning("warning","account doesnt exist")
    

'''*******************************************************************WINDOW************************************************************'''
w = Tk()
w.geometry('1250x1250')
w.state("zoomed")
w.resizable(0, 0)
w.configure(background= "#000000" )
w.title("Bank Application")

'''*********************************************************************Main frame************************************************************'''
MainFrame = Frame(w,bg = "#A0A0A0",relief = SUNKEN)
MainFrame.place(x=400,y=50,height = 750,width = 800)

AccountNumber = Label(MainFrame,text="AccountNumber:",bg = "#A0A0A0",fg = "#000000",font=('fira-code', 15))
AccountNumber.place(x=20,y=70)

AccountNumberEntry = Entry(MainFrame)
AccountNumberEntry.place(x=20,y=110,width = 200)

Pin = Label(MainFrame,text = "Enter your PIN:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
Pin.place(x=20,y=160)

PinEntry = Entry(MainFrame)
PinEntry.place(x=20,y=200,width = 200)

AuthenticatePin = Button(MainFrame,text = "Authenticate",bg = "#A0A0A0",fg = "black",command = AuthenticatePassword)
AuthenticatePin.place(x=250,y =200)

OTP = Label(MainFrame,text = "Enter OTP:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
OTP.place(x=20,y=250)

OTPEntry = Entry(MainFrame)

SendOTP = Button(MainFrame,text = "Send OTP",bg = "dark green",fg = "Black",command = send_otp)
SendOTP.place(x = 30,y = 320)
SendOTP['state'] = DISABLED

ResendOTP = Button(MainFrame,text = "Resend",bg = "dark green",fg = "black")
ResendOTP.place(x=100,y=320)
ResendOTP['state'] = DISABLED

ValidateOTP = Button(MainFrame,text = "Validate",bg= "dark green",fg = "black",command = validateotp)
ValidateOTP.place(x = 70,y = 360)
ValidateOTP['state'] = DISABLED

Login = Button(MainFrame,text = "LOGIN",bg ="dark green",fg = "black",command = afterlogin)
Login.place(x = 100,y = 450)
Login['state'] = DISABLED

NewUser = Button(MainFrame,text = "New User?",bg = "#A0A0A0",fg = "black",command = NewUser)
NewUser.place(x = 100,y = 490)

'''***********************************************************************New User*************************************************************************'''

NewUserFrame = Frame(w,bg = "#A0A0A0",relief= SUNKEN)

NewUserAccountNumber = Label(NewUserFrame,text="Account Number:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
NewUserAccountNumber.place(x = 20,y=70)

GeneratedAccountNumber = Label(NewUserFrame,bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
GeneratedAccountNumber.place(x=200,y=70)

Name = Label(NewUserFrame,text = "Enter your name:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
Name.place(x = 20, y = 110)

NameEntry = Entry(NewUserFrame)
NameEntry.place(x = 20,y = 150,width = 200)

Phone = Label(NewUserFrame,text = "Enter Phone Number:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',15))
Phone.place(x = 20,y = 200)

PhoneEntry = Entry(NewUserFrame)
PhoneEntry.place(x=20,y=240,width = 200)

InitialAmount = Label(NewUserFrame,text = "Enter Initial Amount",bg="#A0A0A0",fg = "#000000",font=('fira-code',15))
InitialAmount.place(x=20,y=290)

InitialAmountEntry = Entry(NewUserFrame)
#InitialAmountEntry.insert(0,' ₹ ')
InitialAmountEntry.place(x=20,y=330,width = 200)

SignUp = Button(NewUserFrame,text = "Sign Up",bg = "dark green",fg = "black",command = uploaddata)
SignUp.place(x=200,y = 500)
#SignUp['state'] = DISABLED

'''************************************************************************Action Frame****************************************************'''
ActionFrame = Frame(w,bg = '#A0A0A0',relief = SUNKEN)

wallpaper = Label(ActionFrame)
image = Image.open("D:\\Downloads\\Screenshot 2022-06-17 132307.png")
resize_img = image.resize((800,750))
img = ImageTk.PhotoImage(resize_img)
wallpaper.configure(image = img)
wallpaper.pack()

withdraw = Button(ActionFrame,text="Withdraw",bg = "#660000",fg = "White",font = ('fira-code',15),command = withdrawfunction)
withdraw.place(x = 180,y = 200,height = 50,width = 150)

deposit = Button(ActionFrame,text = "Deposit",bg = "#660000",fg = "white",font = ('fira-code',15),command = depositfunction)
deposit.place(x = 480,y = 270,height = 50,width = 150)

ministatement = Button(ActionFrame,text = "Mini-Statement",bg = "#660000",fg = "white",font = ('fira-code',15),command = ministatementfunction)
ministatement.place(x = 180,y = 340, height = 50,width = 150)

balance = Button(ActionFrame,text = "Balance",bg = "#660000",fg ="white",font=('fira-code',15),command = showbalance)
balance.place(x = 480,y = 410,height = 50,width = 150)

changepin = Button(ActionFrame,text = "Change Pin",bg = "#660000",fg = "white",font = ('fira-code',15),command = changepinfunction)
changepin.place(x = 180,y = 480,height = 50,width = 150)

transfer = Button(ActionFrame,text = "Transfer Amount",bg ="#660000",fg ="white",font = ('fira-code',15),command = transferamountfunction)
transfer.place(x = 480,y = 550, height = 50,width = 150)

'''***************************************************************************Withdraw Frame*****************************************************'''
WithdrawFrame = Frame(w,bg="#A0A0A0",relief = SUNKEN)

WithdrawLabel = Label(WithdrawFrame,text = "WITHDRAW",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',35))
WithdrawLabel.place(x=280,y=20)

AmountLabel = Label(WithdrawFrame,text = "Enter the amount to be withdrawn:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',20))
AmountLabel.place(x = 200,y = 250)

rupee = Label(WithdrawFrame,text = " ₹ ",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',20))
rupee.place(x=280,y=380)

AmountEntry = Entry(WithdrawFrame,bg = "#A0A0A0",font = ('fira-code',20))
AmountEntry.place(x = 320,y = 380,height = 30,width = 100)

depositsubmit = Button(WithdrawFrame,text = "WITHDRAW",bg = "dark green",fg = "black",command = deductamount)
depositsubmit.place(x=330,y = 480,width = 100)


'''*************************************************************************Deposit Frame***********************************************************'''
DepositFrame = Frame(w,bg = "#A0A0A0",relief = SUNKEN)

DepositLabel = Label(DepositFrame,text="DEPOSIT",bg = "#A0A0A0", fg = "#000000",font = ('fira-code',35))
DepositLabel.place(x=280,y=50)

label1 = Label(DepositFrame,text = "Enter the Deposit Amount:",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',25))
label1.place(x = 200,y = 250)

rupeelabel = Label(DepositFrame,text = " ₹ ",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',20))
rupeelabel.place(x=280,y=380)

rupeeentry = Entry(DepositFrame,bg = "#A0A0A0",font=('fira-code',20))
rupeeentry.place(x=320,y=380,height = 30,width = 100)

depositsubmit = Button(DepositFrame,text = "DEPOSIT",bg = "dark green",fg = "black",command = addamount)
depositsubmit.place(x=330,y = 480)




'''************************************************************************Mini-Statement Frame************************************************************'''






'''************************************************************************Change PIN Frame*****************************************************************'''
ChangePinFrame = Frame(w,bg = "#A0A0A0",relief = SUNKEN)

ChangePinLabel = Label(ChangePinFrame,text = "Change PIN",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',40))
ChangePinLabel.place(x=250,y=50)

oldpinlabel = Label(ChangePinFrame,text = "Enter old pin",bg = "#A0A0A0",fg = "#000000",font=('fira-code',25))
oldpinlabel.place(x=280,y=200)

oldpinentry = Entry(ChangePinFrame,bg = "#A0A0A0",font = ('fira-code',20))
oldpinentry.place(x=280,y=250,height = 30,width = 200)

newpinlabel = Label(ChangePinFrame,text = "Enter new pin",bg="#A0A0A0",fg = "#000000",font = ('fira-code',25))
newpinlabel.place(x = 280,y = 300)

newpinentry = Entry(ChangePinFrame,bg = "#A0A0A0",font = ('fira-code',20))
newpinentry.place(x = 280,y = 350,height = 30,width = 200)

confirmpinlabel = Label(ChangePinFrame,text = "Confirm pin",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',25))
confirmpinlabel.place(x=280,y=400)

confirmpinentry = Entry(ChangePinFrame,bg = "#A0A0A0",font = ('fira-code',20))
confirmpinentry.place(x = 280,y = 450,height = 30,width = 200)

changepinbutton = Button(ChangePinFrame,text = "Change PIN",bg ="dark green",fg = "black",command = validatePIN)
changepinbutton.place(x = 360,y = 600)




'''***********************************************************************Transfer Amount Frame************************************************************'''
TransferAmountFrame = Frame(w,bg = "#A0A0A0",relief = SUNKEN)

transferlabel = Label(TransferAmountFrame,text = "Transfer Amount",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',40))
transferlabel.place(x = 250,y = 50)

transferaccountnolabel = Label(TransferAmountFrame,text = "Enter Transfer Account Number",bg = "#A0A0A0",fg = "#000000",font = ('fira-code',25))
transferaccountnolabel.place(x = 200,y = 200)

transferaccountnoentry = Entry(TransferAmountFrame,bg = "#A0A0A0",font = ('fira-code',20))
transferaccountnoentry.place(x = 300,y=250,height = 30,width = 200)

transferamountlabel = Label(TransferAmountFrame,text = "Enter Amount to be transfered",bg = "#A0A0A0",fg = "#000000",font = ("fira-code",25))
transferamountlabel.place(x = 200,y = 300)

transferamountentry = Entry(TransferAmountFrame,bg = '#A0A0A0',font = ('font-code',20))
transferamountentry.place(x=300,y=350,height = 30,width = 200)

transferamountbutton = Button(TransferAmountFrame,text = "Transfer",bg ="dark green",fg = 'black',command = transferamount)
transferamountbutton.place(x = 360,y = 500)
















w.mainloop()