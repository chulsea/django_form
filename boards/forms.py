from django import forms
from .models import Board

# class BoardForm(forms.Form):
#     기본 Form을 만드는 방법
#     title = forms.CharField(label='제목', 
#             widget=forms.TextInput(attrs={
#                 'placeholder': "THE TITLE",
#             }))
#     content = forms.CharField(label='내용',
#                 widget=forms.Textarea(attrs={
#                     'class': 'Content-input',
#                     'rows': 5,
#                     'cols': 50,
#                     'placeholder': 'Fill the content',
#                 }),
#                 error_messages={
#                     'required': '제발 내용을 입력해주세요',  
#                 })

class BoardForm(forms.ModelForm):
    # Model을 베이스로 Form을 만드는 방법
    class Meta:
        # 위 클래스를 설명하는 이너클래스
        model = Board # ModelForm을 생성할 model 클래스 제공
        # field = ['title', 'content',] # column명 지정
        fields = '__all__' # column명을 직접 지정하지 않고 모두 가져오는 방법
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "제목을 입력하세요!",
                'class': 'title'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': '내용을 입력하세요!',
                'class': 'content',
                'rows': 5,
                'cols': 50
            }),
        }
        error_messages = {
            'title': {
                'required': '제발 내용을 입력해주세요!'
            },
            'content': {
                'required': '내용 좀 입력해요!!'
            },
        }
            