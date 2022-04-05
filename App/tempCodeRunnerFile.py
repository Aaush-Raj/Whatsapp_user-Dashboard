
# def dashboard(request):
#     if request.user.is_authenticated:
#         return render(request, 'App/main_dashboard.html')
#         response= requests.get('https://api.runway.org.in/v1/metadata/categories',headers={'Api-key':'GLiNx_wCsi43Nd0DhVAspIG-_HtAuXLgLpL1cR8kFxQ'}).json()["categories"]   
#         return render(request, 'App/main_dashboard.html',{'response':response})

#     else:
#         return HttpResponseRedirect('/login/')

# @login_required 
# def playlist(request):
#     return render(request, 'App/playlist.html')

# @login_required 
# def notifications(request):
#     return render(request, 'App/notifications.html')


# @login_required 
# def settings(request):
#     return render(request, 'App/settings.html')

# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method =="POST":
#             fm = AuthenticationForm(request=request, data=request.POST)
#             if fm.is_valid():
#                 uname = fm.cleaned_data['username']
#                 upass= fm.cleaned_data['password']
#                 user = authenticate(username=uname, password=upass)
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, 'User Logged in Successfully!')
#                     return HttpResponseRedirect('/')
#                 else:
#                     messages.warning(request,'username or password not correct')
#                     return redirect('/login/')
        
#         else:
#             fm = AuthenticationForm()
#         return render(request, 'App/user_login.html', {'form':fm})
#     else: 
#         return HttpResponseRedirect('/')

# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect('/login/')


    
# # def save_form(request):
# #     if request.method =='POST':
# #         name=request.POST.get('username') 
# #         num=request.POST.get('number')
# #         email=request.POST.get('email')
# #         sub=request.POST.get('subject')
# #         msg=request.POST.get('message')
# #         cu = contact_us(Full_Name=name,Phone_Number=num,Email=email,Subject=sub,Message=msg)
# #         cu.save()
# #     return render(request,'App/main_dashboard.html')



# def home(request):
#     response= requests.get('https://api.runway.org.in/v1/metadata/categories',headers={'Api-key':'GLiNx_wCsi43Nd0DhVAspIG-_HtAuXLgLpL1cR8kFxQ'}).json()["categories"] 
#     states= requests.get('https://api.runway.org.in/v1/metadata/states',headers={'Api-key':'GLiNx_wCsi43Nd0DhVAspIG-_HtAuXLgLpL1cR8kFxQ'}).json()["states"] 
#     districts= requests.get('https://api.runway.org.in/v1/metadata/districts',headers={'Api-key':'GLiNx_wCsi43Nd0DhVAspIG-_HtAuXLgLpL1cR8kFxQ'}).json()["districts"] 
#     return render(request, 'App/main_dashboard.html',{'response':response, 'states':states,'districts':districts})



