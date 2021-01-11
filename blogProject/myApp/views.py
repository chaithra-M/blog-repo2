from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myApp.forms import EmailSendForm,CommentForm
from myApp.models import Comment
from django.core.mail import send_mail
from myApp.models import Post
def post_list_view(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    d={'post_list':post_list}
    return render(request,'myApp/post_list.html',d)
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    form=CommentForm()
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            newcomment=form.save(commit=False)
            newcomment.post=post
            newcomment.save()
            csubmit=True
    d={'post':post,'form':form,'csubmit':csubmit,'comments':comments}
    return render(request,'myApp/post_detail.html',d)
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=EmailSendForm()
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{0}[{1}]recommends you to read {2}'.format(cd['name'],cd['email'],post.title)
            message="Read Post At \n {0}\n\n{1} comments \n {2}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'mailt8513@gmail.com',[cd['to']])
    d={'post':post,'form':form}
    return render(request,'myApp/sharebymail.html',d)
