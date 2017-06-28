from .forms import ImageUploadForm
from .models import Product, Review
from ..bestLogin.models import User
from django.conf import settings
from django.db.models import Count
import csv
import sys
from PIL import Image
import os
import glob
import fileinput

def deleteAllProducts():
    Product.objects.all().delete()
    newFile = open('testfile.csv', 'wb')
    newFile.close()
    aFile = open('newfile.csv', 'wb')
    aFile.close()
    return True

def CSVSTUFF():
    if not os.path.exists('testfile.csv'):
        print "Create New File"
        newFile = open('testfile.csv', 'wb')
        newFile.close()
    if not os.path.exists('newfile.csv'):
        print "Create New File"
        aFile = open('newfile.csv', 'wb')
        aFile.close()
    thing = readinImageList()
    something = thing
    print len(something)
    check = readAndAddNewCSV(thing[0], thing[1])
    if check[0]:
        print check[1]
        CheckForDuplicates()
        SendSecondCSVToFirst()
        addCSVtoDB(something)
    else:
        print check[1]

# LOOK THORUGH THE MEDIA FOLDER TO FIND ALL JPEGS (only read in new picture in one list and old in a different one)
def readinImageList():
    your_media_root = settings.MEDIA_ROOT
    image_list = []
    someLIST = []
    finalFormStr = ""
    your_media_root += "imageApp/images/products"
    print Product.pManager.all()
    for filename in glob.glob(your_media_root+'/*.jpg'):
        newStr = str(filename).split('\\')
        print newStr[len(newStr)-1]
        finalFormStr = "imageApp/images/products/" + newStr[len(newStr)-1]
        someLIST.append(finalFormStr)
        if not Product.pManager.filter(model_pic=finalFormStr):
            image_list.append(finalFormStr)
            print "DOESNT EXIST"
        else:
            #if Product.objects.filter(model_pic=finalFormStr)
            someLIST.append(finalFormStr)
            print "EXISTS!!"
    print "The length of the list is:",len(someLIST)/2
    print "The length of the list is:",len(image_list)
    return image_list, someLIST

# MAKE A CSV AND CHECK IF ITS NEEDS TO BE CREATED (CSV should only contain new images and they cannot exist in database)
def readAndAddNewCSV(list, list2):
    someNumber = Product.pManager.all().count()
    numberOfFiles = len(list) + len(list2)/2
    if someNumber <= numberOfFiles:
        with open('testfile.csv', 'a+') as f:
            count = 0
            someString = ""
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                count += 1
                if not line:
                    someString = "Empty Space At Line:", count
                    return False, someString
            for item in list:
                aString = "SomeName,SDR2S,SOMEDESCRIPTION,23.12,"+item+"\n"
                f.write(aString)
            someString = "All ", count, " Lines Work!!!"
        return True, someString
    else:
        Product.objects.all().delete()
        with open('testfile.csv', 'w+') as f:
            count = 0
            for i in range(0, len(list)):
                print i
                aString = "SomeName,SDR2S,SOMEDESCRIPTION,23.12,"+list[i]+"\n"
                f.write(aString)
                count += 1
            someString = "All ", count, " Lines Work!!!"
        return True, someString

def CheckForDuplicates():
     with open('testfile.csv','r+') as in_file, open('newfile.csv','w+') as out_file:
        seen = []
        reader = csv.reader(in_file, delimiter=',')
        for line in reader:
            print "LINE: ", line[4]
            if line[4] in seen:
                continue

            seen.append(line[4])
            if not line:
                print "STOP"
                return False
            out_file.write(line[0]+",")
            out_file.write(line[1]+",")
            out_file.write(line[2]+",")
            out_file.write(line[3]+",")
            out_file.write(line[4]+"\n")
        print seen

def SendSecondCSVToFirst():
    with open('newfile.csv','r+') as in_file, open('testfile.csv','w+') as out_file:
       reader = csv.reader(in_file, delimiter=',')
       for line in reader:
           print line
           out_file.write(line[0]+",")
           out_file.write(line[1]+",")
           out_file.write(line[2]+",")
           out_file.write(line[3]+",")
           out_file.write(line[4]+"\n")



# DELETE CSV AND DATABASE
def addCSVtoDB(list):
    #Product.objects.all().delete()
    with open('testfile.csv') as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            if not Product.pManager.filter(model_pic=row[4]):
                print "Create Product"
                Product.objects.create(name=row[0], code=row[1], description=row[2], price=row[3], model_pic=row[4])
            elif not Product.pManager.filter(name=row[0]) or not Product.pManager.filter(code=row[1]) or not Product.pManager.filter(description=row[2]) or not Product.pManager.filter(price=row[3]):
                print "Change Product"
                Product.pManager.filter(model_pic=row[4]).update(name=row[0], code=row[1], description=row[2], price=row[3], model_pic=row[4])
