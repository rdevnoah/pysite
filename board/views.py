
from django.db.models import Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def delete(request, id):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')
    board = Board.objects.get(id=id)
    if authuser['id'] != board.user.id:
        return HttpResponseRedirect('/board')

    title = '작성자에 의해 삭제된 글입니다.'
    content = '삭제되었습니다.'

    result = Board.objects.filter(id=id).update(title=title, content=content)

    return HttpResponseRedirect('/board')


def modify(request, id):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    board = Board.objects.get(id=id)

    if authuser['id'] != board.user.id:
        return HttpResponseRedirect('/board')

    title = request.POST['title']
    content = request.POST['title']

    results = Board.objects.filter(id=id).update(title=title, content=content)
    return HttpResponseRedirect('/board')


def modifyform(request, id):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    board = Board.objects.get(id=id)

    if authuser['id'] != board.user.id:
        return HttpResponseRedirect('/board')

    data = {'board': board}
    return render(request, 'board/modify.html', data)


def detail(request, id):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    board = Board.objects.get(id=id)

    data = {'board': board}
    response = render(request, 'board/view.html', data)

    check = False
    if not request.COOKIES.get(str(authuser['id'])):
        response.set_cookie(str(authuser['id']),str(id))
    else:
        already_read = request.COOKIES.get(str(authuser['id']))
        read_list = already_read.split(':')
        check = False
        for read in read_list:
            print(str(id), '-------', read)
            if read == str(id):
                check = True
                break
        if check is False:
            already_read = already_read + ':' + str(id)
            response.set_cookie(str(authuser['id']), already_read)
    if check is False:
        Board.objects.filter(id=id).update(hit=F('hit') + 1)

    return response


def list(request, nowpage=1, kwd=None):
    if kwd is None:
        total_post_count = Board.objects.count()
    else:
        total_post_count = Board.objects.filter(Q(title__contains=kwd) | Q(content__contains=kwd)).filter(content__contains=kwd).count()
    post_count_per_page = 5
    page_count_per_page_group = 5
    start_row_num = int(post_count_per_page * (nowpage-1))
    total_page = int(total_post_count / post_count_per_page if total_post_count % post_count_per_page == 0 else total_post_count / post_count_per_page + 1)
    total_page_group = int(total_post_count / (post_count_per_page * page_count_per_page_group) if (total_post_count % (post_count_per_page* page_count_per_page_group) == 0) else total_post_count / (post_count_per_page * page_count_per_page_group) + 1)
    now_page_group = int(nowpage / page_count_per_page_group if nowpage % page_count_per_page_group == 0 else nowpage / page_count_per_page_group + 1)
    start_page_of_page_group = int(page_count_per_page_group * now_page_group - (page_count_per_page_group - 1))
    end_page_of_page_group = int(total_page if page_count_per_page_group * post_count_per_page * now_page_group >= total_post_count else now_page_group * page_count_per_page_group)
    previous_page_group = True if start_page_of_page_group > 1 else False
    next_page_group = True if now_page_group < total_page_group else False

    if kwd is None:
        results = Board.objects.all().order_by('-groupno', 'orderno', '-regdate')[
                  start_row_num:post_count_per_page + start_row_num]
    else:
        results = Board.objects.filter(Q(title__contains=kwd) | Q(content__contains=kwd)).order_by('-groupno', 'orderno', '-regdate')[
                  start_row_num:post_count_per_page + start_row_num]

    pagenum = []

    for i in range(start_page_of_page_group, end_page_of_page_group+1):
        pagenum.append(i)

    data = {
        'total_count': total_post_count,
        'pagenum' : pagenum,
        'previous_page_group' : previous_page_group,
        'next_page_group': next_page_group,
        'start_page_of_page_group': start_page_of_page_group,
        'end_page_of_page_group': end_page_of_page_group,
        'nowpage' : nowpage,
        'list' : results

    }

    return render(request,'board/list.html', data)


def writeform(request, id=None):
    if id is None:
        return render(request, 'board/write.html')
    else:
        data = {'parent_id':id}
        return render(request, 'board/write.html', data)


def write_reply(request, parent_id):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')

    board = Board()

    parent = Board.objects.get(id=parent_id)

    groupno = parent.groupno
    orderno = parent.orderno + 1
    depth = parent.depth + 1

    results = Board.objects.filter(groupno=groupno).filter(orderno__gte=orderno).update(orderno=F('orderno')+1)

    title = request.POST['title']
    content = request.POST['content']
    userid = request.session['authuser']['id']

    board.title = title
    board.content = content
    board.user_id = userid
    board.groupno = groupno
    board.orderno = orderno
    board.depth = depth

    board.save()

    return HttpResponseRedirect('/board')


def write(request):
    authuser = None
    try:
        authuser = request.session['authuser']
    except Exception as e:
        authuser = None
    if authuser is None:
        return HttpResponseRedirect('/user/loginform')
    board = Board()
    title = request.POST['title']
    content = request.POST['content']
    userid = request.session['authuser']['id']
    orderno = 1
    groupno = 1
    groupnovalue = Board.objects.aggregate(max_groupno=Max('groupno'))
    if groupnovalue['max_groupno'] is not None:
        groupno = int(groupnovalue['max_groupno']) + 1

    board.title = title
    board.content = content
    board.user_id = userid
    board.groupno = groupno
    board.orderno = orderno

    board.save()

    return HttpResponseRedirect('/board')