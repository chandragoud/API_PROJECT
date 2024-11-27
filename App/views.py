from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from App.models import *
from rest_framework.response import Response
import datetime as dt
import jwt
from datetime import datetime
from django.db import connection
from django.conf import settings
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate



# Create your views here.

@api_view(['POST'])
def user_registration(request):
    if request.method == "POST":     
        mobile = request.data.get('mobile')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        data = userregistration.objects.filter(mobile=mobile)
        if data:
            data.update(firstname=firstname,lastname=lastname,username=username,email=email,password=password)
            return Response({"data": request.data,"status":1,"code": 200})
        else:
            userregistration.objects.create(firstname=firstname,lastname=lastname,username=username,email=email,password=password,mobile=mobile)
            return Response({"data": request.data, "status":1,"code": 200})
    return Response({"data":[], "user_id":"","status":0, "code":400})



def generate_access_token(user):

    access_token_payload = {
        'user_id':str(user[0]),
        'exp': datetime.utcnow() + dt.timedelta(days=90, seconds=0),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
                              
    return access_token



@api_view(['POST'])
def login(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        # serializer = loginSerializer(data=request.data)
        # if serializer.is_valid():
        if userregistration.objects.filter(Q(email__iexact=email)).exists()==True:
            user=userregistration.objects.filter(Q(email__iexact=email))
            if user.filter(password=password):
                user.update(loginDateTime=datetime.now())
            # if userregistration.objects.filter(email=email).filter(password=password).exists()==True:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT user_id,firstname,lastname,username,email,password,mobile,createdDate,deletedDate,updatedDate,loginDateTime,logoutDateTime from Users.app_userregistration where email='"'"+str(email)+"'"' and password='"'"+str(password)+"'"';')
                    lk = cursor.fetchall()
                serializer = loginSerializerget(lk, many=True)
                access_token = generate_access_token(lk[0])
                user.update(is_authenticated = 1, access_token = access_token, loginDateTime=datetime.now())
                return Response({"message": "Login success", "data": serializer.data, "status":1, "count":[cursor.rowcount], "access_token":access_token, "code":200})
            return Response({"message": "In correct password", "data":[], "code":200, "count":[], "access_token":0, "status": 0})           
        return Response({"message":"In correct Email", "data":[], "code":200,"count":[], "access_token":0, "status":0})
        #return Response({"message":"Serializer error", "code":400, "count":[], "access_token":0, "status":0})
    return Response({"message":"In-Correct Post data", "code":400, "count":[], "access_token":0,  "status":0})


@api_view(['POST'])
def logout(request):
   
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        user_id = request.data.get("user_id")

        if email and password and user_id:
            try:
                user_details = userregistration.objects.get(user_id=user_id)

                user_details.is_authenticated = False
                user_details.access_token = None
                user_details.save()

                return Response({"message": "User logged out successfully", "code": 200})

            except userregistration.DoesNotExist:
                return Response({"message": "User not found", "code": 404})

        return Response({"message": "Invalid request data", "code": 400})

  
    return Response({"message": "Method not allowed", "code": 405})


# working on test1 branch
# testing purpose 
