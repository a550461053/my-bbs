from mybbs.models import *
from django import forms

class TopicForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = forms.CharField(label="主题名", max_length=128,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    brief = forms.CharField(label="简介", max_length=255,
                            widget=forms.Textarea(attrs={'class': 'form-control'}))
    # 可以有多个管理员
    # admins = forms.MultipleChoiceField(label="管理员",
    #                          widget=forms.CheckboxSelectMultiple(),)
                            # choices=[u.name for u in User.objects.all()],)

    sex = forms.ChoiceField(label='性别', choices=gender)

class CommentForm(forms.Form):
    """
    评论表单
    """
    article = forms.CharField(widget=forms.HiddenInput())
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author",
                                      "class": "comment_input",
                                      "required": "required", "size": "25",
                                      "tabindex": "1"}),
                             max_length=50, error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id": "email", "type": "email",
                                                           "class": "comment_input",
                                                           "required": "required",
                                                           "size": "25", "tabindex": "2"}),
                             max_length=50, error_messages={"required": "email不能为空", })
    url = forms.URLField(widget=forms.TextInput(attrs={"id": "url", "type": "url",
                                                       "class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                         max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id": "comment",
                                                           "class": "message_input",
                                                           "required": "required",
                                                           "cols": "25",
                                                           "row": "5", "tabindex": "4"}),
                              error_messages={"required": "评论不能为空",})
    c_time = models.DateTimeField(auto_now_add=True)
