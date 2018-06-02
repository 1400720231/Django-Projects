from django import forms
from .models import Comments,Praise
# 评论表单
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comments']
        labels={'comments':''}
        widgets = {'comments': forms.Textarea(attrs={'cols': 50,'rows':5})}


class PraiseForm(forms.ModelForm):
    class Meta:
        model = Praise
        fields = ['user','poem']
        
      