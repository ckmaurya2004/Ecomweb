from django.shortcuts import render
from .models import BlogPost

# Create your views here.

from django.http import HttpResponse

# Create your views here.
def index (request):
    allpost = BlogPost.objects.all()
    return render(request,'blog/index.html',{'allpost':allpost})

def blogPost (request,id):
    post = BlogPost.objects.filter(post_id = id)[0]
    return render(request,'blog/blogpost.html', {'post':post,})

