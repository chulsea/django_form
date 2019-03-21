# HTML form tag

## - Django Form

> html Form을 지원해주는 Django class

app 폴더에 `forms.py`를 만든다.

그후 `django` 프로젝트의 forms 모듈을 가져온다.

```python
from django import forms
```

위 의존성을 가지고 `django form`을 생성할 수 있다.

이렇게 생성한 Form 클래스로 html form을 만들 수 있다.

```python
from django import forms

class BoardForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
```

위와 같이 만든 Form 클래스로 view에서 전달하는 form 데이터의 유효성 검사를 시행할 수 있다.

```python
if request.method == 'POST':
    form = BoardForm(request.POST)
    # form 유효성 체크를 위해 binding
    if form.is_valid(): # form 데이터가 유효한지 검사
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')
        board = Board.objects.create(title=title, content=content)
        return redirect('boards:index')
```

위 예시로는 `BoardForm 클래스`로 form 객체를 만든 후 form의 cleaned_data로 유효성 검사한 데이터를 받아올 수 있다.
form 객체를 생성할 때 request.POST로 요청을 전달하여 해당 요청의 전달값을 처리할 수 있도록 만든다.

`django template language`에서는 위 form 객체로 form을 생성할 수 있다.

```python
form = BoardForm()
ctx = {
    'form': form
}
return render(request, 'boards/detail.html', ctx)
```

위와 같이 `template`에 form 객체를 전달하여 form 객체로 입력 form을 만들 수 있도록 한다.
이때는 아무 인자없이 Form 클래스의 객체를 생성하면 기본 form이 생성된다.

template에서는 `{{ form }}`으로 입력 form을 생성할 수 있다.

```html
<form method="POST">
    {% csrf_token %}    
    {{ form }}
    <input type="submit" value="생성">
</form>
```

위 form으로 client에서 유효성 검사 (required, maxlength 등)를 진행하고 만약 form 데이터가 유효하지 않다면
즉시 해당 페이지에서 error 메세지를 보여준다.

위와 같이 만든 form의 속성값, label 등을 커스텀할 수 있다.

```python
class BoardForm(forms.Form):
    title = forms.CharField(label='제목', 
            widget=forms.TextInput(attrs={
                'placeholder': "THE TITLE",
            }))
    content = forms.CharField(label='내용',
                widget=forms.Textarea(attrs={
                    'class': 'Content-input',
                    'rows': 5,
                    'cols': 50,
                    'placeholder': 'Fill the content',
                }),
                error_messages={
                    'required': '제발 내용을 입력해주세요',  
                })
    
```

label 속성으로 해당 input의 이름을 커스텀할 수 있다. 또한 widget으로 속성을 조절할 수 있다.


```python
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    ctx = {
        'board': board,
    }
    return render(request, 'boards/detail.html', ctx)
```

`get_object_or_404`는 만약 없는 model data에 접근하는 경우 기존의 코드 `board = Board.objects.get(pk=board_pk)`에서는 500 server internal error를 클라이언트에 전달한다.
이를 방지하기 위해 만약 DB에 해당 pk에 해당하는 데이터가 없다면 404 에러를 클라이언트에 전달해준다.

get_object_or_404는 첫번째 인자로 model class, 두번째는 pk를 전달해주면 된다.

> get_object_or_404는 import해서 사용해야한다.

```python
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board.title = form.cleaned_data.get('title')
            board.content = form.cleaned_data.get('content')
            board.save()
            return redirect('boards:detail', board.id)
    else:
        form = BoardForm(initial=board.__dict__)
        """
        board가 가지고 있는 값을 dictionary로 가져온다
        원래는 initial에 dictionary로 주기 때문에 __dict__로 준다.
        만약 위와같이 하지 않는다면
        form = BoardForm(initial={'title': board.title, 'content': board.content})
        이와 같이 사용해야한다.
        """
    ctx = {
        'form': form
    }
    return render(request, 'boards/create.html', ctx)
```
위의 `create`와 `detail`에서 사용한 방법을 응용하여 django form으로 update를 구현할 수 있다.

이때 유의할 점은 Form 객체에서 기존에 수정할 데이터를 넘겨줘야한다는 점이다.
이를 위해 Form 생성자의 `initial` 이름인자로 dictionary 형태의 데이터를 넘겨주면 된다.
한번에 넘겨주려면 `모델객체.__dict__`로 넘겨주면 된다.

## - Django ModelForm

> 모델과 관련된 폼을 Model 객체를 참고하여 쉽게 만들어주는 Form 클래스

`ModelForm`은 Model 객체를 토대로 Form을 만드는 방법이다. 관련 모델을 토대로 Form을 만들경우 `ModelForm`으로 만드는 것이 좋다.

```python
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
```

`ModelForm`은 `forms.ModelForm`을 상속받아 정의할 수 있다.
이때 `Meta`라는 이너`inner`클래스를 정의하여 해당 `ModelForm`에 `Model`정보를 전달한다.

### Meta?

위에서 언급했듯이 `ModelForm`에서 사용할 `Model` 정보를 정의하는 클래스이다.
이를 기반으로 `ModelForm`에서 `Model`값을 베이스로 Form을 생성한다.

1. model : ModelForm을 생성할 model 클래스 명을 전달하는 property
    
    ```python
    model = Board 
    ```

2. fields : 해당 `ModelForm`에서 사용할 column 명을 지정하는 property

    ```python
    fields = ['title', 'content',]
    ```
    위와 같이 column명을 list 형태로 열거하여 전달할 수 있다. 단, 위 경우 column이 많아지면 등록에 불편함이 있다.
    만약 해당 Model에 모든 column을 지정한다면 아래와 같이 설정한다.
    
    ```python
    fields = '__all__'
    ```
    
3. widgets : 각 column의 input에 속성을 정의하는 방법
    
    > ModelForm에서의 widgets은 Form의 widget과 동일하게 정의한다.

4. error_messages : 각 column의 입력값 검증에서 알맞은 데이터가 전달되지않아 오류가 나는 경우 전달하는 메세지

    ```python
    error_messages = {
        'title': {
            'required': '제발 내용을 입력해주세요!'
        },
        'content': {
            'required': '내용 좀 입력해요!!'
        },
    }
    ```
    
    - required로 값이 없는 경우의 에러메세지를 전달할 수 있다.
    
위 `ModelForm`으로 

## - django-crispy-forms

