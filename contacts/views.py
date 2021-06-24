from django.shortcuts import render
from django.views import View
from .forms import CollegeForm
from .models import CollegeName,CollegeContact
from .helpers import get_results,get_phone_emails



# Create your views here.


class CollegeView(View):


    def get(self,request):
        form =CollegeForm()
        ctx={"form":form}
        return render(request,"contacts/home.html",ctx)


    def post(self,request):

        if CollegeName.objects.filter(name=request.POST['name']).exists():
            id = CollegeName.objects.filter(name=request.POST['name'])[0].id
            print(id)
            print(id)

            obj=CollegeContact.objects.filter(college=str(id))[0]

            def str_to_list(str1):
                str1=str1.strip('{}').split(', ')
                for i in range(len(str1)):
                    str1[i]=str1[i].strip("''")
                return str1

            obj={"numbers":str_to_list(obj.numbers),"emails":str_to_list(obj.emails)}

        else:
            form = CollegeForm(request.POST)




            results = get_results(request.POST['name'])
            emails,phones = get_phone_emails(results)



            if emails or phones:
                form.save()
                id = CollegeName.objects.filter(name=request.POST['name'])
                obj = CollegeContact(emails=emails, numbers=phones, college=id[0])

                obj.save()
            else:
                obj=[]



        ctx={"object":obj,"name":request.POST['name']}
        return render(request,"contacts/list.html",ctx)






