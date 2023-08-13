from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Peep
#unregister groups 
admin.site.unregister(Group)

#Mix Profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile

#Simplify data

#Extend User Model

class UserAdmin(admin.ModelAdmin):
    model = User
    #Just Display username fields 
    fields = ["username"]
    inlines = [ProfileInline]
    

#Unregister initial user
admin.site.unregister(User)

#Re-register and profile
admin.site.register(User,UserAdmin)
#admin.site.register(Profile)

admin.site.register(Peep)


