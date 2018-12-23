import markdown
from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from comments.models import Comments
from comments.forms import CommentForm
from django.core.mail import send_mail
from comments.forms import CommentForm

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6

    def get_queryset(self):
        return super(IndexView, self).get_queryset().filter(is_deleted = False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0 : page_number - 1]
            if left[0] > 2:
               left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number -3 ) if (page_number - 3 ) > 0 else 0 : page_number -1 ]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last':last,
        }

        return data


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg':error_msg,})

    post_list = Post.objects.filter(Q(title__icontains=q) |Q(body__icontains=q), is_deleted=False)
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})



def update_likes(request):
    pk = request.POST.get('pk')
    likes = request.POST.get('likes')
    post = get_object_or_404(Post, pk = pk)
    print('%s' % likes )
    post.update_likes(likes)

    return render(request, 'blog/detail.html', {'post':post})



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        if not request.COOKIES.get('post_%s_read' % self.object.pk ):
            self.object.increase_views()

        response.set_cookie('post_%s_read' % self.object.pk, 'true')
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)

        md = markdown.Markdown(extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          TocExtension(slugify=slugify),
                                      ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        post = super(PostDetailView, self).get_object(queryset=None)
        # 获取文章下的评论list
        post_content_type = ContentType.objects.get_for_model(post)
        comment_list = Comments.objects.filter(content_type = post_content_type,object_id = post.pk, parent=None)
        # 评论表单
        comment_form = CommentForm(initial={'content_type':post_content_type.model, 'object_id':post.pk, 'reply_comment_id': 0})
        # 上一页，下一页
        pre_post = Post.objects.filter(id__gt=post.id).last()
        next_post = Post.objects.filter(id__lt=post.id).first()
        # 获取context
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'comment_form':comment_form,
            'comment_list':comment_list.order_by('-created_time'),
            'pre_post':pre_post,
            'next_post':next_post,
        })
        return context



class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month = month, is_deleted=False)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate, is_deleted=False)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag, is_deleted=False)


def profile(request):
    name='龚奥博'
    return render(request, 'blog/profile.html', {'name': name})