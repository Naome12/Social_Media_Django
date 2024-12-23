from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .models import *

@csrf_exempt
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.creater:
        return HttpResponse(status=403)
    if request.method == "POST":
        if request.POST.get("edit_mode") == "true":
            post.edit_mode = True
            post.save()
            return redirect("profile", username=request.user.username)
        text = request.POST.get("text")
        pic = request.FILES.get("picture")
        img_chg = request.POST.get("img_change")
        try:
            post.content_text = text
            if img_chg == "true" and pic:
                post.content_image = pic
            post.edit_mode = False
            post.save()
            return redirect("profile", username=request.user.username)  
        except Exception as e:
            print(e)
            return JsonResponse({"success": False, "error": str(e)})
    return HttpResponse(status=405)


# <!-- {% extends 'network/index.html' %} {% load static %} {% block profile %}
# <div class="w-full">
#   <div class="h-48 bg-cover bg-center" style="background-image: url(/media/{{username.cover}});"></div>

#   <div class="flex flex-col items-center -mt-16">
#     <div class="w-32 h-32 bg-cover bg-center rounded-full border-4 border-white" style="background-image: url(/media/{{username.profile_pic}});"></div>

#     <div class="text-center mt-4">
#       <div class="mb-4">
#         {% if user.username == username.username %}
#         <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
#           <a href="{% url 'editprofile' username %}">Edit Profile</a>
#         </button>
#         {% elif is_follower %}
#         <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
#           Following
#         </button>
#         {% else %}
#         <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600" onclick="follow_user(this, '{{username.username}}', 'edit_page')">
#           Follow
#         </button>
#         {% endif %}
#       </div>

#       <div class="text-gray-500 mb-4">
#         <i class="far fa-calendar-alt"></i> &nbsp; Joined {{ username.date_joined|date:"F Y" }}

#       </div>
#       <div class="flex space-x-8 text-center">
#         <div>
#           <strong class="text-xl">{{posts_count}}</strong><br />
#           <span class="text-gray-500">Posts</span>
#         </div>
#         <div>
#           <a href="{% url 'following' username %}" class="hover:text-blue-500">
#             <strong class="text-xl">{{following_count | default:0}}</strong
#             ><br />
#             <span class="text-gray-500">Following</span>
#           </a>
#         </div>
#         <div>
#           <a href="{% url 'followers' username %}" class="hover:text-blue-500">
#             <strong class="text-xl">{{follower_count | default:0}}</strong
#             ><br />
#             <span class="text-gray-500">Followers</span>
#           </a>
#         </div>
#       </div>
#     </div>
#   </div>
# </div>

# <div class="w-full mt-8">
#   {% if posts %}
#   <div class="grid gap-4">
#     {% for post in posts %}
#     <div class="bg-white p-4 rounded-lg shadow-md">
#       <p>{{ post.content_text }}</p>
#       {% if post.content_image %}
#       <img src="/media/{{ post.content_image }}" class="w-full mt-2 rounded-md" alt="Post Image"/>
#       {% endif %}

#       {% if post.creater == request.user %}
#       <div class="flex justify-end space-x-4 mt-4">
#         <form action="{% url 'deletepost' post.id %}" method="POST" onsubmit="return confirm('Are you sure you want to delete this post?');">
#           {% csrf_token %}
#           <button type="submit" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600">
#             Delete
#           </button>
#         </form>
#       </div>
#       {% endif %}
#     </div>
#     {% endfor %}
#   </div>
#   {% else %} {% block emptyprofile %}
#   <center class="mt-8">
#     <strong class="text-gray-700">@{{username}} hasn't posted</strong>
#     <div class="text-gray-500">When they do, their posts will show up here</div>
#   </center>
#   {% endblock %} {% endif %}
# </div>
# {% endblock %} -->

