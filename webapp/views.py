import json
import time

import firebase_admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from firebase_admin import credentials, firestore, storage

json_key = {
    "type": "service_account",
    "project_id": "edhunt",
    "private_key_id": "f9d4ffc352178ab32ef126ded89eabedb85f414a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCkjjKUJAmyODBW\n/t/wGxh/plsJNZnIqzR+t0mit1hne6DXcgB4DKS8s7XKe3p8HS/V/XmSliafSAeB\nacVit5P43WRlPc2bDzmxd4b0bsS7CZkDYc8PcSWQbmhkGvUdJYfSFoW6H+dmRqGC\nc3v3CoZTtAqF+2zQ9egzlhEizpM2XymUdABpvvAwYM9kDI6mVKI5Tc7u3PgsXPJQ\nrouyGpE9joWysWI9KQoFpJRyL6jXH81SpNuTptAxWRWismYwwmQXHo0fYs3zzUSB\nmCWJgMTE7Cus4QZl4kXIb41bwIo/5EUEonbFqHdLohWebSauqE5gQOLJEaIpLzxY\no3Tb+H37AgMBAAECggEADgHGn2KD6sYqozUVxb/gsXjtFdcYrIKaONEMNQwLO9/D\nnKMpFA7rdN6NMluZXPg1Cq+FSit6xSMh9GuW8CS1NUFPGukMV88Pd6I3fBXzrAIQ\nor+QGv3kFyu2uhKrW5xGt+TP5Dxz+3o2pD6FRk2Aip5wKOBybkUIS1/SPJa95CpJ\nh1DD+5HV1+09blUTIJY/LhqSoIRxc/DA4XwyRTDywDi4VmFOpyt7aw9gLkY53iWg\nhzROaiH7J/cq423JY2fLCyGwMgzQQVIcIcd8FQWVuzifwE7LHxC4pxC2c7d66u/P\niefRq/0oIjVWHnblSnGiGpGKaZhM5MVZvrZlYms+vQKBgQDYkZxUJJGPtNn9hxWW\nXFsZTS17zxrdOLBrw2GNrjGH12uaGNcje9uuKYLObSuVlTeEJbC5ll5HVkAOyZmO\noLPVXHhMa2Z56Wxa/YoHORkQNV+1lhcZnmm/eEeMA2rtwA6h/vo+F+WgD6USyPrO\nSNFNwCWWEiz4E+bsjAt17NcM1QKBgQDChDeX4ST1wJClmTUJ4WtI+xkQPAvmBcSs\nFFR17qcp4bKlhYoSraek8EOs7v4mGe/fZ+J1oKiAUprJ7IvruQda5jY4FnF4/8i3\n9Y9UU624+aGSebQhVIua55+7kmOULI5HOzHjpwvHLcleiDZa0H4oA1xxKw4ggA7y\nqV3HgcSHjwKBgAwI+4EJjzVHPZ4DNcXnWACt80sgFUQZ9GPotbEj7wi3hflITBxi\ns7CYCfbixjtH0Y/8cDfADXk1Z9XqiigM8jF3NBA7H7TCrgzYbiU8nRHzhWAX+Syp\nSwMi8gbr4bNYqveBrfJpbY9ZjzjeBmIUVd1WQkB2vh0DLiATIEfrY4AJAoGALb2P\noRxlZ5CvsvEzAq7KXrAFNccY+S80D078iXrkPjn/m2KqlDfXqzaAg4LzqpwAxyUT\noJt15C8IjSEdygGJlDt8VnYYmt5zIacR3D+NI2k4MEyEKi5KYdPDwQTse6R6lI97\n7M+UOnMu3hbjyTkr4Vbg/w+j08qpOTDQh6ChSUsCgYB7PoZIRM+qq427GUnD80qB\nVr+4yNCkHoKygkFjnKchQibIaCKVMjDda5rErT5rexEVT6SRHm8UhSyZ/R8U1XIV\nvD5hii7CiEyj0jbPtC+F3e2zkDSd9bV/ok6N2HcnPm3aaQxCt6zVzqL8BIgU/zJ4\nqUXzeDwq/ooY7uNDpA+ZKg==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ebkth@edhunt.iam.gserviceaccount.com",
    "client_id": "114363773335303361188",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ebkth%40edhunt.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(json_key)
firebase_admin.initialize_app(cred, {'storageBucket': 'edhunt.appspot.com'})
bucket = storage.bucket()


def show_dashboard(request):
    fs = firestore.client()
    courses_doc = fs.collection("courses").get()
    courses = []
    cats = []
    for i in courses_doc:
        cats.append(i.id)
        datas = fs.collection("courses").document(i.id).collection(i.id).get()
        for j in datas:
            d = j.to_dict()
            d['cat'] = i.id
            d['id'] = j.id
            courses.append(d)
    return render(request, 'index.html', {"course_list": courses})


def delete_course(request):
    data = request.POST
    cat_id = data['id']
    cat = data['cat']
    db = firestore.client()
    db.collection('courses').document(cat).collection(cat).document(cat_id).delete()
    courses_doc = db.collection("courses").get()
    courses = []
    cats = []
    for i in courses_doc:
        cats.append(i.id)
        datas = db.collection("courses").document(i.id).collection(i.id).get()
        for j in datas:
            d = j.to_dict()
            d['cat'] = i.id
            courses.append(d)
    return render(request, 'index.html', {"course_list": courses})


def add_course(request):
    if request.method == "POST":
        data = request.POST
        cat = data['cat']
        files = request.FILES.getlist('image')
        if len(files) == 1:
            ima = files[0]
            blob = bucket.blob(ima.name + str(time.time_ns()) + ".pdf")
            blob.upload_from_file(ima.file)
            blob.make_public()
            url = blob.public_url
            db = firestore.client()
            d = db.collection('courses').document(cat).collection(cat).document()
            d.set({
                "id": d.id,
                "url": url,
                "name": data['name']
            })
            return HttpResponseRedirect('dashboard')
        else:
            print("no fields")
            return HttpResponseRedirect('dashboard')
    else:
        db = firestore.client()
        courses_doc = db.collection("courses").get()
        cats = []
        for i in courses_doc:
            cats.append(i.id)
        return render(request, 'course_add.html', {
            'category': cats
        })


def show_category(request):
    fs = firestore.client()
    cat_doc = fs.collection("indian_category").get()
    category = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        category.append(d)
    return render(request, 'category.html', {"cat": category})


def add_category(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data and 'coach' in data and 'distance' in data and 'indian' in data:
            db = firestore.client()
            d = db.collection('indian_category').document()
            d.set({
                "id": d.id,
                "isCoaching": str(data['coach']).lower() == "true",
                "isDistance": str(data['distance']).lower() == "true",
                "isIndian": str(data['indian']).lower() == "true",
                "name": data['name']
            })
            return HttpResponseRedirect('category')
        else:
            print("no fields")
            return HttpResponseRedirect('category')
    else:
        return render(request, 'category-add.html')


def edit_category(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data and 'coach' in data and 'id' in data and 'distance' in data and 'indian' in data:
            db = firestore.client()
            db.collection('indian_category').document(data['id']).update({
                "id": data['id'],
                "isCoaching": str(data['coach']).lower() == "true",
                "isDistance": str(data['distance']).lower() == "true",
                "isIndian": str(data['indian']).lower() == "true",
                "name": data['name']
            })
            return HttpResponseRedirect('category')
        else:
            return HttpResponseRedirect('category')
    else:
        cat_id = request.GET.get('id', "")
        db = firestore.client()
        details = db.collection('indian_category').document(cat_id).get()
        cat = details.to_dict()
    return render(request, 'category-edit.html', {"cat": cat, "cat_id": cat_id})


def delete_category(request):
    data = request.POST
    cat_id = data['id']
    db = firestore.client()
    db.collection('indian_category').document(cat_id).delete()
    cat_doc = db.collection("indian_category").get()
    category = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        category.append(d)
    return render(request, 'category.html', {"cat": category})


def show_service(request):
    fs = firestore.client()
    ser_coll = fs.collection('indian_college').get()
    dist = fs.collection('district').get()
    services = []
    for i in ser_coll:
        di_name = ""
        d = i.to_dict()
        for j in dist:
            if j.id == d['district_id']:
                di_name = j.to_dict()['name']

        d['district'] = di_name
        services.append(d)
    return render(request, 'services.html', {"services": services})


def add_service(request):
    data = request.POST
    if request.method == "POST":
        print("1st if")
        data_dict = dict(data)
        for key, value in data_dict.items():
            if len(value) == 1 and value[0] == "[]":
                print("2st if")
                data_dict[key] = []
            elif key == "urls":
                data_dict[key] = json.loads(value[0])
            else:
                data_dict[key] = value[0]
        photos = request.FILES.getlist('image')
        # pdf = request.FILES.getlist('pdf_url')
        data = data_dict
        print(data)
        if 'about' in data and 'category_id' in data and "district_id" in data and "grade_id" in data and "isAutonomous" in data and "isCoaching" in data and "isDistance" in data and "isIndian" in data and "name" in data and "number" in data and 'university' in data:
            print("3st if")
            url_list = []
            pdf_url = ""
            for i in photos:
                print("4st if")
                blob = bucket.blob(i.name)
                blob.upload_from_file(i.file)
                blob.make_public()
                url_list.append(blob.public_url)
            # if len(pdf) == 1:
            #     blob = bucket.blob(pdf[0].name)
            #     blob.upload_from_file(pdf[0].file)
            #     blob.make_public()
            #     pdf_url = blob.public_url
            db = firestore.client()
            d = db.collection('indian_college').document()
            d.set({
                "about": data['about'],
                "category_id": data['category_id'],

                "image": url_list,
                "district_id": data['district_id'],
                "grade_id": data['grade_id'],
                "isAutonomous": str(data['isAutonomous']).lower() == "true",
                "isCoaching": str(data['isCoaching']).lower() == "true",
                "isDistance": str(data['isDistance']).lower() == "true",
                "isIndian": str(data['isIndian']).lower() == "true",
                "university": data['university'],
                "name": data['name'],
                "number": data['number'],

                "id": d.id,
                "urls": data['urls']
            })
            return HttpResponseRedirect('service')
        else:
            return HttpResponseRedirect('service')
    fs = firestore.client()
    cat_doc = fs.collection("indian_category").get()
    category = []
    cities = []
    grade = []
    for i in cat_doc:
        category.append(i.to_dict())
    city_doc = fs.collection('district').get()
    for i in city_doc:
        dt = i.to_dict()
        dt['id'] = i.id
        cities.append(dt)
    grade_doc = fs.collection('grade').get()
    for i in grade_doc:
        grade.append(i.to_dict())
    return render(request, 'service-add.html', {
        'category': category,
        'city': cities,
        'grade': grade,
    })


def edit_service(request):
    data = request.POST
    if request.method == "POST":
        data_dict = dict(data)
        for key, value in data_dict.items():
            if len(value) == 1 and value[0] == "[]":
                data_dict[key] = []
            elif key == "description":
                data_dict[key] = json.loads(value[0])
            elif key == "old_url":
                result = json.loads(value[0])
                result_list = [str(item) for item in result]
                data_dict[key] = result_list
            elif key == "urls":
                data_dict[key] = json.loads(value[0])
            else:
                data_dict[key] = value[0]
        photos = request.FILES.getlist('image')
        pdf = request.FILES.getlist('pdf_url')
        data = data_dict
        if 'about' in data and 'category_id' in data and "district_id" in data and "grade_id" in data and "isAutonomous" in data and "isCoaching" in data and "isDistance" in data and "isIndian" in data and "name" in data and "number" in data and 'university' in data and 'id' in data and 'old_url' in data:
            url_list = []
            for i in data['old_url']:
                if type(i) is str:
                    url_list.append(i)
            pdf_url = ""
            db = firestore.client()
            for i in photos:
                blob = bucket.blob(i.name)
                blob.upload_from_file(i.file)
                blob.make_public()
                url_list.append(blob.public_url)
            if len(pdf) == 1:
                blob = bucket.blob(pdf[0].name)
                blob.upload_from_file(pdf[0].file)
                blob.make_public()
                pdf_url = blob.public_url
                db.collection('indian_college').document(data['id']).update({
                    "pdf_url": pdf_url,
                })

            db.collection('indian_college').document(data['id']).update({
                "about": data['about'],
                "category_id": data['category_id'],
                "image": url_list,
                "district_id": data['district_id'],
                "grade_id": data['grade_id'],
                "isAutonomous": str(data['isAutonomous']).lower() == "true",
                "isCoaching": str(data['isCoaching']).lower() == "true",
                "isDistance": str(data['isDistance']).lower() == "true",
                "isIndian": str(data['isIndian']).lower() == "true",
                "university": data['university'],
                "name": data['name'],
                "number": data['number'],
                "id": data['id'],
                "urls": data['urls']
            })
            return HttpResponseRedirect('service')
        else:
            return ""
    else:
        clg_id = request.GET.get('id', "")
        db = firestore.client()
        service = db.collection('indian_college').document(clg_id).get()
        cat_doc = db.collection("indian_category").get()
        category = []
        cities = []
        grade = []
        for i in cat_doc:
            category.append(i.to_dict())
        city_doc = db.collection('district').get()
        for i in city_doc:
            dt = i.to_dict()
            dt['id'] = i.id
            cities.append(dt)
        grade_doc = db.collection('grade').get()
        for i in grade_doc:
            grade.append(i.to_dict())
        ser = service.to_dict()
        return render(request, 'service-edit.html', {
            'category': category,
            'city': cities,
            'grade': grade,
            'service': ser,
            'service_id': clg_id,
        })


# def delete_service(request):
#     data = request.POST
#     print(data)
#     if request.method == "POST":
#         if 'id' in data and 'service_name' in data:
#             db = firestore.client()
#             db.collection('services').document(data['service_name']).set({"d": "d"})
#             db.collection('services').document(data['service_name']).collection(data['service_name']).document(
#                 data['id']).delete()
#             return HttpResponseRedirect('service')
#         else:
#             return ""
def delete_service(request):
    data = request.POST
    cat_id = data['id']
    db = firestore.client()
    db.collection('indian_college').document(cat_id).delete()
    return HttpResponseRedirect('service')


def show_banner(request):
    fs = firestore.client()
    ban_doc = fs.collection("banner").get()
    ban = []
    for i in ban_doc:
        d = i.to_dict()
        ban.append(d)
    return render(request, 'banner.html', {"ban": ban})


def add_banner(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES.getlist('image')
        if len(files) == 1:
            ima = files[0]
            blob = bucket.blob(ima.name + str(time.time_ns()) + ".png")
            blob.upload_from_file(ima.file)
            blob.make_public()
            url = blob.public_url
            db = firestore.client()
            d = db.collection('banner').document()
            d.set({
                "id": d.id,
                "url": url
            })
            return HttpResponseRedirect('banner')
        else:
            print("no fields")
            return HttpResponseRedirect('banner')
    else:
        return render(request, 'banner-add.html')


def edit_banner(request):
    if request.method == "POST":
        data = request.POST
        if 'id' in data and 'old_url' in data:
            ima = request.FILES.getlist('image')
            if len(ima) == 1:
                blob = bucket.blob(ima[0].name + str(time.time_ns()) + ".png")
                blob.upload_from_file(ima[0].file)
                blob.make_public()
                url = blob.public_url
            else:
                url = data['old_url']
            db = firestore.client()
            db.collection('banner').document(data['id']).update({
                "url": url,
                "id": data['id']
            })
            return HttpResponseRedirect('banner')
        else:
            return HttpResponseRedirect('banner')
    else:
        ban_id = request.GET.get('id', "")
        db = firestore.client()
        details = db.collection('banners').document(ban_id).get()
        cat = details.to_dict()
    return render(request, 'banner-edit.html', {"ban": cat, "ban_id": ban_id})


def delete_banner(request):
    data = request.POST
    cat_id = data['id']
    db = firestore.client()
    db.collection('banner').document(cat_id).delete()
    cat_doc = db.collection("banner").get()
    category = []
    for i in cat_doc:
        d = i.to_dict()
        category.append(d)
    return render(request, 'banner.html', {"cat": category})


def show_district(request):
    fs = firestore.client()
    cat_doc = fs.collection("district").get()
    city = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        city.append(d)
    return render(request, 'district.html', {"city": city})


def add_district(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data:
            db = firestore.client()
            db.collection('district').document().set({
                "name": data['name']
            })
            return HttpResponseRedirect('district')
        else:
            print("no fields")
            return HttpResponseRedirect('district')
    else:
        return render(request, 'district-add.html')


def edit_district(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data and 'id' in data:
            db = firestore.client()
            db.collection('district').document(data['id']).update({

                "name": data['name']
            })
            return HttpResponseRedirect('district')
        else:
            return HttpResponseRedirect('district')
    else:
        city_id = request.GET.get('id', "")
        db = firestore.client()
        details = db.collection('district').document(city_id).get()
        cat = details.to_dict()
    return render(request, 'district-edit.html', {"city": cat, "city_id": city_id})


def edit_user(request):
    if request.method == "POST":
        data = request.POST
        if 'coins' in data and 'id' in data:
            db = firestore.client()
            db.collection('users').document(data['id']).update({

                "coins": data['coins']
            })
            return HttpResponseRedirect('users')
        else:
            return HttpResponseRedirect('users')
    else:
        city_id = request.GET.get('id', "")
        db = firestore.client()
        details = db.collection('users').document(city_id).get()
        cat = details.to_dict()
    return render(request, 'user_edit.html', {"user": cat, "user_id": city_id})


def delete_district(request):
    data = request.POST
    cat_id = data['id']
    db = firestore.client()
    db.collection('district').document(cat_id).delete()
    cat_doc = db.collection("district").get()
    category = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        category.append(d)
    return render(request, 'district.html', {"cat": category})


def show_grade(request):
    fs = firestore.client()
    cat_doc = fs.collection("grade").get()
    city = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        city.append(d)
    return render(request, 'grade.html', {"city": city})


def add_grade(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data:
            db = firestore.client()
            d = db.collection('grade').document()
            d.set({
                "name": data['name'],
                "id": d.id,
            })
            return HttpResponseRedirect('grade')
        else:
            print("no fields")
            return HttpResponseRedirect('grade')
    else:
        return render(request, 'grade-add.html')


def edit_grade(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data and 'id' in data:
            db = firestore.client()
            db.collection('grade').document(data['id']).update({

                "name": data['name']
            })
            return HttpResponseRedirect('grade')
        else:
            return HttpResponseRedirect('grade')
    else:
        city_id = request.GET.get('id', "")
        db = firestore.client()
        details = db.collection('grade').document(city_id).get()
        cat = details.to_dict()
    return render(request, 'grade-edit.html', {"city": cat, "city_id": city_id})


def delete_grade(request):
    data = request.POST
    cat_id = data['id']
    db = firestore.client()
    db.collection('grade').document(cat_id).delete()
    cat_doc = db.collection("grade").get()
    category = []
    for i in cat_doc:
        d = i.to_dict()
        d['id'] = i.id
        category.append(d)
    return render(request, 'grade.html', {"cat": category})


def show_user(request):
    fs = firestore.client()
    users_doc = fs.collection("users").get()
    users = []
    for i in users_doc:
        users.append(i.to_dict())
    return render(request, 'users.html', {"user_list": users})


def register_business(request):
    fs = firestore.client()
    bus_doc = fs.collection("business").get()
    busin = []
    for i in bus_doc:
        busin.append(i.to_dict())
    return render(request, 'business.html', {"bus": busin})


def scholarship(request):
    fs = firestore.client()
    sco_doc = fs.collection("scolar").get()
    scolar = []
    for i in sco_doc:
        scolar.append(i.to_dict())
    return render(request, 'scholarship.html', {"sc": scolar})


def withdrawl_request(request):
    fs = firestore.client()
    sco_doc = fs.collection("withdraw").get()
    scolar = []
    for i in sco_doc:
        scolar.append(i.to_dict())
    return render(request, 'withdrawl.html', {"with": scolar})


def update_status(request):
    status = request.GET.get('id', "")
    db = firestore.client()
    db.collection('withdraw').document(status).update({
        "status":True
    })
    sco_doc = db.collection("withdraw").get()
    scolar = []
    for i in sco_doc:
        scolar.append(i.to_dict())
    return render(request, 'withdrawl.html', {"with": scolar})