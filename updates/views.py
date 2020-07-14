from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import Post, Comment
from .forms import PostForm, CommentForm
from users.models import CustomUser

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


decorators = [user_passes_test(lambda u: u.is_superuser)]

# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

@method_decorator(decorators, name='dispatch')
class CreatePostView(CreateView):
    redirect_field_name = 'updates/post_detail.html'

    form_class = PostForm

    model = Post

@method_decorator(decorators, name='dispatch')
class PostUpdateView(UpdateView):
    redirect_field_name = 'updates/post_detail.html'

    form_class = PostForm

    model = Post

@method_decorator(decorators, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('updates:post_list')

@method_decorator(decorators, name='dispatch')
class DraftListView(ListView):
    redirect_field_name = 'updates/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')






@user_passes_test(lambda u: u.is_superuser)
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    email_list = get_emails()
    for email in email_list:
        html_message = render_to_string('updates/new_post_email.html', {'id':pk, 'email':email})
        plain_msg = strip_tags(html_message)
        send_mail('New Update from the Joneses To Read!', plain_msg, 'noreply@jonezfam.com', [email,], html_message=html_message, fail_silently=False)
    post.publish()
    return redirect("updates:post_list")


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('updates:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'updates/comment_form.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('updates:post_detail', pk=comment.post.pk)


@user_passes_test(lambda u: u.is_superuser)
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('updates:post_detail', pk=post_pk)


def get_emails():
    users = CustomUser.objects.all()
    email_list = []
    for user in users:
        if user.email_update == True:
            email_list.append(user.email)
    return email_list
