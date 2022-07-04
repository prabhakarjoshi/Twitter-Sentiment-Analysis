from var import options,optionlist
from myanalyser import trainAndAnalyse

print("\n############################################################################\nSentiment Analysis of tweets to understand major issues of a product/company\n############################################################################")
prodName=input("\n\nEnter the product to analyse the tweets:- ")
print("\n\noptions:-")
size=len(optionlist)
for i in range(size):
    print(i+1,":  ",optionlist[i])


myOption=int(input("\n\nSelect the category of the product:- "))

# print(optionlist[myOption-1])
mylist=options.get(optionlist[myOption-1])

print("training model....")

trainAndAnalyse(mylist,prodName)

print("\n---------------\n__++_ END _++__\n---------------")



