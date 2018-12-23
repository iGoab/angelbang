from django.shortcuts import render, get_object_or_404, redirect,reverse
from blog.models import Post
from .models import Comments
from django.http import JsonResponse
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm


# Create your views here.
def update_comments(request):
    referer = request.META.get('HTTP_REFERER', reverse('blog:index'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comments = Comments()
        comments.user = comment_form.cleaned_data['user']
        comments.text = comment_form.cleaned_data['text']
        comments.content_object = comment_form.cleaned_data['content_object']
        comments.save()

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comments.root = parent.root if not parent.root is None else parent
            comments.parent = parent
            comments.reply_to = parent.user
        comments.save()

        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comments.user.username
        data['created_time'] = comments.created_time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{M}%S{s}').format(y='年', m='月', d='日',h='时',M='分',s='秒')
        data['text'] = comments.text
        if not parent is None:
            data['reply_to'] = comments.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comments.pk
        data['root_pk'] = comments.root.pk if not comments.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]

    return JsonResponse(data)
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
