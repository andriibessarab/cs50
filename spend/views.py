from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .models import User, Familie, Categorie, Transaction
from .functions import validate

from datetime import datetime

import json
import re

#Pages

def main(request):

    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')

    if request.user.is_authenticated:

        family = Familie.objects.filter(users=request.user)

        context = {
            'users': family[0].users.all(),
            'transactions': family[0].transactions.all()
        }

        return render(request, 'spend/authorized/main.html')

    else:

        return render(request, 'spend/unauthorized/unauthorized.html')       

def history(request):

    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    
    if request.user.is_authenticated:
        return render(request, 'spend/authorized/history.html')

    else:
        return HttpResponseRedirect('/')  

#Authentication

def register(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        userData = json.loads(request.POST['user'])
        errorsData = {}
        numOfFields = len(userData)
        numOfValidFields = 0
        for i in userData: 
            validationResults = validate(i, userData[i].replace(' ', ''))
            if validationResults[0]:
                errorsData[i] = True
                numOfValidFields += 1
            else:
                errorsData[i] = validationResults[1]
        if numOfFields != numOfValidFields:
            return JsonResponse({'status': False, 'errors': errorsData})
        User.objects.create_user(username = userData['username'], email = userData['email'],
            password = userData['password'], first_name = userData['fname'],
            last_name = userData['lname'])
        user = User.objects.filter(username=userData['username'])
        if request.user.is_authenticated:
            family = Familie.objects.filter(users=request.user)
            family[0].users.add(user[0])
        else:
            family = Familie()
            family.save()
            family.users.add(user[0])
        return JsonResponse({'status': True})

def logIn(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        userData = json.loads(request.POST['user'])
        for i in userData:
            if userData[i] == '':
                return JsonResponse({'status': False, 'error': 'Please fill out all the fields'})
        user = authenticate(username = userData['username'], password = userData['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'error': 'Incorrect username or password'})

def logOut(request):

    logout(request)
    return HttpResponseRedirect('/')

#Create/Add

def track(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        family = Familie.objects.filter(users=request.user)
        transactionData = json.loads(request.POST['transactionData'])

        #Check if all field filled out

        for i in transactionData:
            if not transactionData[i]:
                return JsonResponse({'status': False, 'error': 'Please fill out all the fields!'})

        #Check if type is valid

        if not transactionData['type'] == '+' and not transactionData['type'] == '-':
            return JsonResponse({'status': False, 'error': 'Incorrect type!'})

        #Check if amount is a positive number

        try:
            if float(transactionData['amount']) < 1:
                return JsonResponse({'status': False, 'error': 'Incorrect amount!'})
        except:
            return JsonResponse({'status': False, 'error': 'Amount is not a number!'})

        #Check if user is valid

        allFamilyMembers = [str(i) for i in list(family[0].users.all())]

        if transactionData['user'] not in allFamilyMembers:
            return JsonResponse({'status': False, 'error': 'Incorrect user!'})

        #Check if category is valid

        allCategories = [str(i) for i in list(family[0].categories.all())]

        if not transactionData['category'] in allCategories:
            return JsonResponse({'status': False, 'error': 'Incorrect category!'})
    

        #Record transaction

        newTransaction = Transaction(
            transactionType = transactionData['type'],
            user = User.objects.filter(username=transactionData['user'])[0],
            category = family[0].categories.filter(name = transactionData['category'])[0],
            amount = float(transactionData['amount'])
        )
        newTransaction.save()
        family[0].transactions.add(newTransaction)
    
        return JsonResponse({'status': True})

def addNewCategory(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        name = request.POST['name']

        family = Familie.objects.filter(users=request.user)

        allCategories = [str(i) for i in list(family[0].categories.all())]

        if name.replace(' ', '') == '':
            return JsonResponse({'status': False, 'error': 'Please choose a name of a category!'});
        elif name in allCategories:
            return JsonResponse({'status': False, 'error': 'You already have a category with this name!'});
        else:

            newCategory = Categorie(
            name = name
            )
            newCategory.save()

            family[0].categories.add(newCategory)

            return JsonResponse({'status':True})

#Information Requests

def requestInformation(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')
    else:
        information = {}
        family = Familie.objects.filter(users=request.user)
        currentMonth = datetime.today().strftime('%m')

        information['users'] = []
        information['categories'] = []
        information['transactions'] = []
        information['total'] = 0
        information['spent'] = 0
        information['remaining'] = 0
        information['totalLastMonth'] = 0
        information['spentLastMonth'] = 0
        information['remainingLastMonth'] = 0

        for i in family[0].users.all():
            information['users'].append(str(i))
        
        for i in family[0].categories.all():
            information['categories'].append(str(i))

        for i in family[0].transactions.all():

            transaction = {
                'type': i.transactionType,
                'category': str(i.category),
                'user': str(i.user),
                'amount': i.amount,
                'time': i.time.strftime('%Y/%m/%d %H:%M'),
            }

            information['transactions'].append(transaction);

            if i.transactionType == '+':
                if str(i.time)[5:7] == currentMonth:
                    information['total'] += i.amount
                    information['remaining'] += i.amount
                if str(i.time)[5:7] == str(int(currentMonth) - 1):
                    information['totalLastMonth'] += i.amount
                    information['remainingLastMonth'] += i.amount

            if i.transactionType == '-':
                if str(i.time)[5:7] == currentMonth:
                    information['spent'] += i.amount
                    information['remaining'] -= i.amount
                if str(i.time)[5:7] == str(int(currentMonth) - 1):
                    information['spentLastMonth'] += i.amount
                    information['remainingLastMonth'] += i.amount
        
        information['transactions'].reverse()

        return JsonResponse(information)

#Error Handling

def error(request, *args):

    return HttpResponseRedirect('/')