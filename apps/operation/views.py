from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount, LikeRecord, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import CommentForm


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)


class LikeView(View):
    '''
    添加喜欢与取消喜欢
    '''
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return ErrorResponse(400, 'you were not login')
        content_type = request.GET.get('content_type')
        object_id = int(request.GET.get('object_id'))
        try:
            content_type = ContentType.objects.get(model=content_type)
            model_class = content_type.model_class()
            model_obj = model_class.objects.get(pk=object_id)
        except ObjectDoesNotExist:
            return ErrorResponse(401, 'object not exist')

        # 处理数据
        if request.GET.get('is_like') == 'true':
            # 进行点赞判断
            like_record, created = LikeRecord.objects.get_or_create(
                content_type=content_type, object_id=object_id, user=user)
            if created:
                # 未进行过点赞
                like_count, created = LikeCount.objects.get_or_create(
                    content_type=content_type, object_id=object_id)
                like_count.liked_num += 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                # 已点赞过,不能重复点赞
                return ErrorResponse(402, 'you had liked')

        else:
            # 取消点赞
            if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
                # 有过点赞,取消点赞
                like_record = LikeRecord.objects.get(
                    content_type=content_type, object_id=object_id, user=user)
                like_record.delete()
                # 点赞总数减1
                like_count, created = LikeCount.objects.get_or_create(
                    content_type=content_type, object_id=object_id)
                if not created:
                    like_count.liked_num -= 1
                    like_count.save()
                    return SuccessResponse(like_count.liked_num)
                else:
                    return ErrorResponse(404, 'data error')
            else:
                # 没点赞过,无法取消
                return ErrorResponse(403, 'you did not like it')


class AddComment(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def post(self, request):
        data = {}
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment()
            comment.user = request.user
            comment.text = comment_form.cleaned_data['text']
            comment.content_object = comment_form.cleaned_data['content_object']
            parent = comment_form.cleaned_data['parent']
            if parent is not None:
                comment.root = parent.root if parent.root is not None else parent
                comment.parent = parent
                comment.reply_to = parent.user
            comment.save()
            # 返回数据
            data['status'] = 'SUCCESS'
            data['username'] = comment.user.get_nickname_or_username()
            data['comment_time'] = comment.comment_time.timestamp()
            data['text'] = comment.text
            data['content_type'] = ContentType.objects.get_for_model(
                comment).model
            data['user_icon'] = comment.user.usericon.url
            if parent is not None:
                data['reply_to'] = comment.reply_to.get_nickname_or_username()
            else:
                data['reply_to'] = ''
            data['pk'] = comment.pk
            data['root_pk'] = comment.root.pk if comment.root is not None else ''
        else:
            data['status'] = 'ERROR'
            data['message'] = list(comment_form.errors.values())[0][0]
        return JsonResponse(data)
