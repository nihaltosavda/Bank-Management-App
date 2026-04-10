import json
import random
import string
from pathlib import Path


class Bank:
       database = 'data.json'
       data = []

       try:
              if Path(database).exists():
                     with open(database) as fs:
                            data = json.loads(fs.read())
              else:
                     print("no such file exists")
       except Exception as err:
              print(f"an error occurred: {err}")

       @classmethod
       def __update(cls):
              with open(Bank.database, 'w') as fs:
                     fs.write(json.dumps(Bank.data))

       @classmethod
       def __accountgenerate(cls):
              alpha = random.choices(string.ascii_letters, k=3)
              num = random.choices(string.digits, k=3)
              spchar = random.choices("!@#$%^&*", k=1)
              id = alpha + num + spchar
              random.shuffle(id)
              return "".join(id)




       def createAccount(self):
              info = {
                     "name": input("enter your name: "),
                     "age": int(input("enter your age: ")),
                     "email": input("enter your email: "),
                     "pin": int(input("enter your pin: ")),
                     "account_number": Bank.__accountgenerate(),
                     "balance": 0,
              }

              if info["age"] < 18 or len(str(info["pin"])) != 4:
                     print("you are not eligible to create an account")
              else:
                     print("account created successfully")
                     for i in info:
                            print(f"{i}: {info[i]}")
                     print("please note down your account number for future reference")

                     
                     Bank.data.append(info)
                     Bank.__update()

       def depositMoney(self):
              accnumber = input("enter your account number: ")
              pin = int(input("enter your pin: "))

              userdata = [i for i in Bank.data if i["account_number"] == accnumber and i["pin"] == pin]

              if userdata == False:
                     print("invalid account number or pin")
              else:
                     amount = int(input("enter the amount you want to depposit: "))
                     if amount > 10000 or amount < 0:
                            print("you cannot deposit more than 10000 or less than 0 at a time")
                     else:
                            userdata[0]["balance"] += amount
                            Bank.__update()
                            print("money deposited successfully")


       def withdrawMoney(self):
              accnumber = input("enter your account number: ")
              pin = int(input("enter your pin: "))

              userdata = [i for i in Bank.data if i["account_number"] == accnumber and i["pin"] == pin]

              if userdata == False:
                     print("invalid account number or pin")
              else:
                     amount = int(input("enter the amount you want to withdraw: "))
                     if userdata[0]["balance"] < amount:
                            print("you have insufficient balance")
                     else:
                            userdata[0]["balance"] -= amount
                            Bank.__update()
                            print("money withdrawn successfully")


       def showDetails(self):
              accnumber = input("enter your account number: ")
              pin = int(input("enter your pin: "))

              userdata = [i for i in Bank.data if i["account_number"] == accnumber and i["pin"] == pin]
              print("your information is as follows: \n")
              for i in userdata[0]:
                     print(f"{i}: {userdata[0][i]}")

       def updateDetails(self):
              accnumber = input("enter your account number: ")
              pin = int(input("enter your pin: "))

              userdata = [i for i in Bank.data if i["account_number"] == accnumber and i["pin"] == pin]

              if userdata == False:
                     print("invalid account number or pin")
              else:
                     print("Fill the details for change or leave it empty")

                     newdata = {
                            "name": input("please tell new name or press enter: "),
                            "email": input("please tell new email or press enter: "),
                            "pin": int(input("please tell new pin or press enter: "))
                     }

                     if newdata["name"] == "":
                            newdata["name"] = userdata[0]["name"]
                     if newdata["email"] == "":
                            newdata["email"] = userdata[0]["email"]   
                     if newdata["pin"] == "":    
                            newdata["pin"] = userdata[0]["pin"]

                     newdata["age"] = userdata[0]["age"]
                     newdata["account_number"] = userdata[0]["account_number"]
                     newdata["balance"] = userdata[0]["balance"]

                     if type(newdata["pin"]) == str:
                            newdata["pin"] = int(newdata["pin"])

                     for i in newdata:
                            if newdata[i] == userdata[0][i]:
                                   continue
                            else:
                                   userdata[0][i] = newdata[i]
                     
                     Bank.__update()
                     print("details updated successfully")

       def deleteAccount(self):
              accnumber = input("enter your account number: ")
              pin = int(input("enter your pin: "))

              userdata = [i for i in Bank.data if i["account_number"] == accnumber and i["pin"] == pin]

              if userdata == False:
                     print("No suchh user exists")
              else:
                     check = input("are you sure you want to delete your account? (y/n): ")
                     if check == "n" or check == "N":
                            print("account deletion cancelled")
                     else:
                            index = Bank.data.index(userdata[0])
                            Bank.data.pop(index)
                            print("account deleted successfully")
                            Bank.__update()
       



user = Bank()
print("press 1 for creating account")
print("press 2 for depositing money in the account")
print("press 3 for withdrawing money from the account")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting the account")

check = int(input("tell your response: "))

if check == 1:
       user.createAccount()

if check == 2:
       user.depositMoney()

if check == 3:
       user.withdrawMoney()

if check == 4:
       user.showDetails()

if check == 5:
       user.updateDetails()

if check == 6:
       user.deleteAccount()