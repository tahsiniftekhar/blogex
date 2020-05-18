from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Blog

def index(request):
    return render(request, 'index.html')


# SHow all the blogs

def blogs(request):
    if request.method == 'GET':
        blogList = Blog.objects.all().order_by('-date')
        paginator = Paginator(blogList, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        try:
            blogList = paginator.page(page_obj)
        except PageNotAnInteger:
            blogList = paginator.page(1)
        except EmptyPage:
            blogList = paginator.page(paginator.num_pages)  

        context = {
            'page_obj' : page_obj
        }
        return render(request, 'blogs.html', context)
    else:
        return render(request, "404.html")


# Read the blog

def read(request, id):
    if request.method == 'GET':
        blog = Blog.objects.get(id=id)
        is_liked = False
        if blog.like.filter(id=request.user.id).exists():
            is_liked = True
        context = {
            'blog' : blog,
            'is_liked' : is_liked,
            'total_likes' : blog.total_likes()
        }
        return render(request, 'read.html', context)
    else:
        return render(request, "404.html")


# Write a new blog

def write(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'write.html')
        else:
            return redirect('/account/login')
            

    elif request.method == 'POST':
        bname = request.POST["bname"]
        body = request.POST["body"]
        blog = Blog(title= bname, content= body, author_id = request.user.id)
        blog.save()
        messages.success(request, 'Created Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "404.html")


# Edit the created blog

def edit(request,id):
    blog = Blog.objects.get(id=id)
    context = {
        'edit_blog' : blog
    }
    if request.user.is_authenticated and request.user.id == blog.author_id:
        if request.method == "GET":
            return render(request, "edit.html", context)

        elif request.method == "POST":
            bname = request.POST["bname"]
            body = request.POST["body"]
            blog.title = bname
            blog.content= body
            blog.save()

            messages.success(request, 'Updated Successfully!')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        return render(request, "404.html")



# Delete the created blog

def delete(request, id):
    blog = Blog.objects.get(id=id)

    context = {
        'delete_blog' : blog
    }
    if request.user.is_authenticated and request.user.id == blog.author_id:
        if request.method == "GET":
            return render(request, "delete.html", context)

        elif request.method == "POST":
            blog.delete()

            return redirect("/blogs")
    else:
        return render(request, "404.html")


# Like/Dislike the Blog

def like_blog(request):
    blog = Blog.objects.get(id=request.POST["blog_id"])
    is_liked = False
    if blog.like.filter(id=request.user.id).exists():
        blog.like.remove(request.user)
        is_liked = False

    else:
        blog.like.add(request.user)
        is_liked = True
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))