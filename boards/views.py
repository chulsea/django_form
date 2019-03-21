from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    ctx = {
        'boards': boards
    }
    return render(request, 'boards/index.html', ctx)
    
# def create(request):
#     기존의 Django Form을 사용했을 때 create
#     if request.method == 'POST':
#         form = BoardForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             content = form.cleaned_data.get('content')
#             board = Board.objects.create(title=title, content=content)
#             return redirect('boards:index')
#     else:
#         form = BoardForm()
#     ctx = {
#         'form': form
#     }
#     return render(request, 'boards/create.html', ctx)
    
def create(request):
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

def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    ctx = {
        'board': board,
    }
    return render(request, 'boards/detail.html', ctx)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)
        
# def update(request, board_pk):
#     board = get_object_or_404(Board, pk=board_pk)
#     if request.method == 'POST':
#         form = BoardForm(request.POST)
#         if form.is_valid():
#             board.title = form.cleaned_data.get('title')
#             board.content = form.cleaned_data.get('content')
#             board.save()
#             return redirect('boards:detail', board.id)
#     else:
#         form = BoardForm(initial=board.__dict__)
#         """
#         board가 가지고 있는 값을 dictionary로 가져온다
#         원래는 initial에 dictionary로 주기 때문에 __dict__로 준다.
#         만약 위와같이 하지 않는다면
#         form = BoardForm(initial={'title': board.title, 'content': board.content})
#         이와 같이 사용해야한다.
#         """
#     ctx = {
#         'form': form
#     }
#   return render(request, 'boards/create.html', ctx)
        
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        # instance를 전달하여 form에서 전달된 데이터를 해당 model로 받을 수 있다.
        if form.is_valid():
            board = board.save()
            return redirect('boards:detail', board.id)
    else:
        form = BoardForm(instance=board)
        # ModelForm에서는 initial이 아닌 instance로 객체를 전달해야한다.
    ctx = {
        'form': form,
        'board': board,
    }
    return render(request, 'boards/form.html', ctx)
