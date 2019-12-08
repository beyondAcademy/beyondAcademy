##default import
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json, random, math

from graduateProject.models import BaseCode
from graduateProject.models import Document;

def algorithmView(request):
    try:
        documentQueryset = Document.objects.all()
        documentSelectedQueryset = Document.objects.filter(read_yn__exact='Y')
        category1PercentageDict = {1:0, 2:0, 3:0, 4:0, 5:0}
        category2PercentageDict = {1:0, 2:0, 3:0, 4:0, 5:0}
        category3PercentageDict = {1:0, 2:0, 3:0, 4:0, 5:0}

        for document in documentSelectedQueryset:
            if document.category1 == 1:
                category1PercentageDict[1] += 1
            elif document.category1 == 2:
                category1PercentageDict[2] += 1
            elif document.category1 == 3:
                category1PercentageDict[3] += 1
            elif document.category1 == 4:
                category1PercentageDict[4] += 1
            elif document.category1 == 5:
                category1PercentageDict[5] += 1

            if document.category2 == 1:
                category2PercentageDict[1] += 1
            elif document.category2 == 2:
                category2PercentageDict[2] += 1
            elif document.category2 == 3:
                category2PercentageDict[3] += 1
            elif document.category2 == 4:
                category2PercentageDict[4] += 1
            elif document.category2 == 5:
                category2PercentageDict[5] += 1

            if document.category3 == 1:
                category3PercentageDict[1] += 1
            elif document.category3 == 2:
                category3PercentageDict[2] += 1
            elif document.category3 == 3:
                category3PercentageDict[3] += 1
            elif document.category3 == 4:
                category3PercentageDict[4] += 1
            elif document.category3 == 5:
                category3PercentageDict[5] += 1

        if documentSelectedQueryset.count() == 0:
            listCount = 1
        else:
            listCount = documentSelectedQueryset.count()


        category1PercentageDict[1] = category1PercentageDict[1] / listCount * 100
        category1PercentageDict[2] = category1PercentageDict[2] / listCount * 100
        category1PercentageDict[3] = category1PercentageDict[3] / listCount * 100
        category1PercentageDict[4] = category1PercentageDict[4] / listCount * 100
        category1PercentageDict[5] = category1PercentageDict[5] / listCount * 100

        category2PercentageDict[1] = category2PercentageDict[1] / listCount * 100
        category2PercentageDict[2] = category2PercentageDict[2] / listCount * 100
        category2PercentageDict[3] = category2PercentageDict[3] / listCount * 100
        category2PercentageDict[4] = category2PercentageDict[4] / listCount * 100
        category2PercentageDict[5] = category2PercentageDict[5] / listCount * 100

        category3PercentageDict[1] = category3PercentageDict[1] / listCount * 100
        category3PercentageDict[2] = category3PercentageDict[2] / listCount * 100
        category3PercentageDict[3] = category3PercentageDict[3] / listCount * 100
        category3PercentageDict[4] = category3PercentageDict[4] / listCount * 100
        category3PercentageDict[5] = category3PercentageDict[5] / listCount * 100

        return render(request, 'graduateProject/algorithm/algorithm.html', {'documentQueryset':documentQueryset, 'category1PercentageDict':category1PercentageDict, 'category2PercentageDict':category2PercentageDict, 'category3PercentageDict':category3PercentageDict})
    except Exception as ex:
        print('error occured :', ex)

def algorithmSelectView(request):
    try:
        documentId = request.POST['documentId']
        document = Document.objects.get(id__exact=documentId)
        document.read_yn = 'Y'
        document.save()

        msg= documentId + "번 문서가 채택되었습니다."
        return HttpResponse(msg)
    except Exception as ex:
        print('error occured :', ex)

def algorithmResetView(request):
    try:
        documentQueryset = Document.objects.filter(read_yn__exact='Y')
        for document in documentQueryset:
            document.read_yn = 'N'
            document.save()

        msg = 'documet list가 리셋되었습니다.'
        return HttpResponse(msg)
    except Exception as ex:
        print('error occured :', ex)

def algorithmRecommend(request):
    try:
        documentSelectedQueryset = Document.objects.filter(read_yn__exact='Y')
        category1PercentageDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        category2PercentageDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        category3PercentageDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for document in documentSelectedQueryset:
            if document.category1 == 1:
                category1PercentageDict[1] += 1
            elif document.category1 == 2:
                category1PercentageDict[2] += 1
            elif document.category1 == 3:
                category1PercentageDict[3] += 1
            elif document.category1 == 4:
                category1PercentageDict[4] += 1
            elif document.category1 == 5:
                category1PercentageDict[5] += 1

            if document.category2 == 1:
                category2PercentageDict[1] += 1
            elif document.category2 == 2:
                category2PercentageDict[2] += 1
            elif document.category2 == 3:
                category2PercentageDict[3] += 1
            elif document.category2 == 4:
                category2PercentageDict[4] += 1
            elif document.category2 == 5:
                category2PercentageDict[5] += 1

            if document.category3 == 1:
                category3PercentageDict[1] += 1
            elif document.category3 == 2:
                category3PercentageDict[2] += 1
            elif document.category3 == 3:
                category3PercentageDict[3] += 1
            elif document.category3 == 4:
                category3PercentageDict[4] += 1
            elif document.category3 == 5:
                category3PercentageDict[5] += 1

        if documentSelectedQueryset.count() == 0:
            listCount = 1
        else:
            listCount = documentSelectedQueryset.count()

        category1PercentageDict[1] = math.ceil(category1PercentageDict[1] / listCount * 10)
        category1PercentageDict[2] = math.ceil(category1PercentageDict[2] / listCount * 10)
        category1PercentageDict[3] = math.ceil(category1PercentageDict[3] / listCount * 10)
        category1PercentageDict[4] = math.ceil(category1PercentageDict[4] / listCount * 10)
        category1PercentageDict[5] = math.ceil(category1PercentageDict[5] / listCount * 10)

        category2PercentageDict[1] = math.ceil(category2PercentageDict[1] / listCount * 10)
        category2PercentageDict[2] = math.ceil(category2PercentageDict[2] / listCount * 10)
        category2PercentageDict[3] = math.ceil(category2PercentageDict[3] / listCount * 10)
        category2PercentageDict[4] = math.ceil(category2PercentageDict[4] / listCount * 10)
        category2PercentageDict[5] = math.ceil(category2PercentageDict[5] / listCount * 10)

        category3PercentageDict[1] = math.ceil(category3PercentageDict[1] / listCount * 10)
        category3PercentageDict[2] = math.ceil(category3PercentageDict[2] / listCount * 10)
        category3PercentageDict[3] = math.ceil(category3PercentageDict[3] / listCount * 10)
        category3PercentageDict[4] = math.ceil(category3PercentageDict[4] / listCount * 10)
        category3PercentageDict[5] = math.ceil(category3PercentageDict[5] / listCount * 10)

        documentQuerySet = Document.objects.filter(read_yn__exact='N')
        querysetList = list(documentQuerySet)
        random.shuffle(querysetList)

        cat1_1 = []
        cat1_2 = []
        cat1_3 = []
        cat1_4 = []
        cat1_5 = []
        cat2_1 = []
        cat2_2 = []
        cat2_3 = []
        cat2_4 = []
        cat2_5 = []
        cat3_1 = []
        cat3_2 = []
        cat3_3 = []
        cat3_4 = []
        cat3_5 = []
        countList = {'cat1':category1PercentageDict, 'cat2':category2PercentageDict, 'cat3':category3PercentageDict}

        for document in querysetList:
            if (document.category1) == 1:
                if (len(cat1_1) < category1PercentageDict[1]):
                    cat1_1.append(document)
            if (document.category1) == 2:
                if (len(cat1_2) < category1PercentageDict[2]):
                    cat1_2.append(document)
            if (document.category1) == 3:
                if (len(cat1_3) < category1PercentageDict[3]):
                    cat1_3.append(document)
            if (document.category1) == 4:
                if (len(cat1_4) < category1PercentageDict[4]):
                    cat1_4.append(document)
            if (document.category1) == 5:
                if (len(cat1_5) < category1PercentageDict[5]):
                    cat1_5.append(document)
            if (document.category2) == 1:
                if (len(cat2_1) < category2PercentageDict[1]):
                    cat2_1.append(document)
            if (document.category2) == 2:
                if (len(cat2_2) < category2PercentageDict[2]):
                    cat2_2.append(document)
            if (document.category2) == 3:
                if (len(cat2_3) < category2PercentageDict[3]):
                    cat2_3.append(document)
            if (document.category2) == 4:
                if (len(cat2_4) < category2PercentageDict[4]):
                    cat2_4.append(document)
            if (document.category2) == 5:
                if (len(cat2_5) < category2PercentageDict[5]):
                    cat2_5.append(document)
            if (document.category3) == 1:
                if (len(cat3_1) < category3PercentageDict[1]):
                    cat3_1.append(document)
            if (document.category3) == 2:
                if (len(cat3_2) < category3PercentageDict[2]):
                    cat3_2.append(document)
            if (document.category3) == 3:
                if (len(cat3_3) < category3PercentageDict[3]):
                    cat3_3.append(document)
            if (document.category3) == 4:
                if (len(cat3_4) < category3PercentageDict[4]):
                    cat3_4.append(document)
            if (document.category3) == 5:
                if (len(cat3_5) < category3PercentageDict[5]):
                    cat3_5.append(document)


        cat1 = cat1_1 + cat1_2 + cat1_3 + cat1_4 + cat1_5
        cat2 = cat2_1 + cat2_2 + cat2_3 + cat2_4 + cat2_5
        cat3 = cat3_1 + cat3_2 + cat3_3 + cat3_4 + cat3_5

        cat1List = []
        for document in cat1:
            cat1Dict = {}
            cat1Dict['docId'] = document.id
            cat1Dict['category1'] = document.category1
            cat1Dict['category2'] = document.category2
            cat1Dict['category3'] = document.category3
            cat1List.append(cat1Dict)

        cat2List = []
        for document in cat2:
            cat2Dict = {}
            cat2Dict['docId'] = document.id
            cat2Dict['category1'] = document.category1
            cat2Dict['category2'] = document.category2
            cat2Dict['category3'] = document.category3
            cat2List.append(cat2Dict)

        cat3List = []
        for document in cat3:
            cat3Dict = {}
            cat3Dict['docId'] = document.id
            cat3Dict['category1'] = document.category1
            cat3Dict['category2'] = document.category2
            cat3Dict['category3'] = document.category3
            cat3List.append(cat3Dict)

        finalList = []
        finalDict = {}
        finalDict['cat1'] = cat1List
        finalDict['cat2'] = cat2List
        finalDict['cat3'] = cat3List
        finalList.append(finalDict)
        finalList.append(countList)

        return HttpResponse(json.dumps(finalList), content_type="application/json")
    except Exception as ex:
        print('error occured :', ex)