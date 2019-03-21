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
    
위 `ModelForm`을 사용하면 `Form`과 다음과 같은 차이점이 있다.

```python
def create(request):
    # 기존의 Django Form을 사용했을 때 create
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            board = Board.objects.create(title=title, content=content)
            return redirect('boards:index')
    else:
        form = BoardForm()
    ctx = {
        'form': form
    }
    return render(request, 'boards/create.html', ctx)
    
def create(request):
    # ModelForm을 사용했을때의 create
    if request.method == 'POST':
        form = BoardForm(request.POST)
        # 이미 ModelForm에서 입력값 검증을 처리하므로 form의 cleaned_data를 받을 필요가 없다.
        if form.is_valid():
            board = form.save() # form에는 검증된 데이터만 존재하므로 save()로 모델 객체를 받을 수 있다.
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    ctx = {
        'form': form,
    }
    return render(request, 'boards/form.html', ctx)
```

`ModelForm`에서는 `cleaned_data`를 사용하지 않는다. 이미 요청이 들어왔을때 검증을 처리해주기 때문이다.
그리고 `ModelForm`의 객체에 `save()` 메서드가 존재한다. 이는 `Model` 객체의 `save()`와는 다르다.
`ModelForm`의 객체에 `save()`는 검증된 데이터를 가지고 해당 model 객체를 가져올 수 있다.

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
        
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board) # 1
        # instance를 전달하여 form에서 전달된 데이터를 해당 model로 받을 수 있다.
        if form.is_valid():
            board = board.save() # 2
            return redirect('boards:detail', board.id)
    else:
        form = BoardForm(instance=board) # 3
        # ModelForm에서는 initial이 아닌 instance로 객체를 전달해야한다.
    ctx = {
        'form': form,
        'board': board,
    }
    return render(request, 'boards/form.html', ctx)
```

`update`는 create와는 달리 클라이언트에게 이미 저장된 값을 보여주는게 UX 디자인 상 좋으므로 수정할 model의 값을 전달하는 것이 좋다.
이를 위해서는 `ModelForm`의 `instance` 인자를 이용한다.

> `Form`에서는 initial을 이용했다.

```python
form = BoardForm(request.POST, instance=board)
```
위와 같이 요청받은 입력값과 함께 데이터를 바꿀 모델을 instance 인자에 전달하여 수정된 model 객체를 얻을 수 있다.

```python
form = BoardForm(instance=board)
```
`request.POST` 없이 instance 인자에 수정할 model 객체를 전달하면 `ModelForm`에 등록한 `Meta` 정보를 이용하여 값을 바인딩해준다.

## - request.resolver_match

django template language에서 요청정보를 받을때 사용한다.

```
{% if request.resolver_match.url_name == 'create' %}
    <h1>NEW board</h1>
{% else %}
    <h1>EDIT board</h1>
{% endif %}
```

위와 같이 django url에서 url이름이 create인 경우는 `NEW board`를 아닌 경우는 `EDIT board`를 뷰에 렌더한다.

## - django-crispy-forms

`settings.py`에 app등록을 해주어야한다.

> 'crispy_forms'

그리고 `settings.py`에 아래와 같이 설정한다.
CRISPY_TEMPLATE_PACK = 'bootstrap4'

> 위 경우는 bootstrap을 사용하는 경우

`settings.py`에 `crispy`를 등록하면 이제 django template language에서 `crispy`를 사용할 수 있다.

사용하기 위해서는 `{% load crispy_forms_tags %}`로 crispy filter를 가져와야한다.

그리고 form 객체에 crispy 필터를 사용하여 CRISPY_TEMPLATE_PACK으로 등록한 스타일을 입힐 수 있다.

`{{ form|crispy }}`

## - form customize

위에서 `{{ form|crispy }}` 는 해당 설정 정보에 맞춰 `form`을 생성해준다.

만약 자동 설정이 싫다면 각각의 column을 따로 분리하여 설정할 수 있다.

```
# ex1
<form method="POST">
    {% csrf_token %}    
    {{ form.title }} 
    <!-- form에서 title column 만-->
    {{ form.content }} 
    <!-- form에서 content column 만-->
    <!-- 단, label은 없다. -->
    <input type="submit" value="생성">
</form>
```

단, 위 방식은 `{{ label_tag }}`가 없으므로 label없이 렌더된다.

label을 사용하려면 다음 아래의 두 방법이 있다.

```
# ex2
<!-- form의 field를 for문으로 출력하는 방법 -->
<form method="POST">
    {% csrf_token %}
    {% for field in form %}
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    {% endfor %}
    <input type="submit" value="생성">
</form>

# ex3
<!-- 기본적으로 각각 분기 -->
{{ form.non_field_errors }}
<form method="POST">
    {% csrf_token %}
    <div>
        {{ form.title.errors }}
        {{ form.title.label_tag }}
        {{ form.title }}
    </div>
    <div>
        {{ form.content.errors }}
        {{ form.content.label_tag }}
        {{ form.content }}
    </div>
    <input type="submit" value="생성">
</form>
```

위 2번째 예시는 for문으로 각각의 field를 보여주는 방법이다.

> errors는 만약 검증이 실패한 경우 전송되는 error message(flash)를 의미한다.

아래 3번째 예시는 아얘 각각의 field를 분리하여 직접 렌더하는 방법이다.

이외에 django에서 지원해주는 강력한 기능인 `form Helper` 기능이 있다.

form helper는 `ModelForm`을 정의한 class에 생성자(`__init__`)을 정의해야한다.

```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

...

# form_helper
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'POST'
    self.helper.add_input(Submit('submit', '작성'))
```

위와 같이 `crispy_forms.helper`의 FormHelper로 `POST` method에 대한 `form_helper`를 정의할 수 있다.

이렇게 정의한 `FormHelper`는 `{{ crispy form }}`으로 form을 렌더할 수 있다.

> crispy는 crispy_forms_tags를 load해야한다.