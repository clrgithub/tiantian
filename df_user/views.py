#coding=utf-8
from __future__ import unicode_literals
import hashlib
from django.shortcuts import render,redirect
from models import *
from df_goods.models import *
from df_order.models import *
from django.http import JsonResponse, HttpResponseRedirect
from user_decorator import login

def register(request):
    context = {'title': '用户注册'}
    return render(request,'df_user/register.html', context)

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    if uname == '' or upwd == '' or upwd2 == '' or uemail == '':
        return redirect('/user/register/')

    if upwd != upwd2:
        return redirect('/user/register/')
        print ('pwd error')
    s1 = hashlib.sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user=UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def register_exist(sequest):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def Login(request):
    uname = request.COOKIES.get('uname', '')
    context={'title': '用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request, 'df_user/login.html', context)

def Login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)

    users = UserInfo.objects.filter(uname=uname)

    if len(users) == 1:
        s1 = hashlib.sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)

            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            print request.session['user_name']
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

def Logout(request):
    request.session.flush()
    return redirect('/')

@login
def Info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_idsl = goods_ids.split(',')
    # GoodsInfo.objects.filter(id__in=goods_idsl) #一次查询所有id,但按id来排序
    goods_list = []
    if goods_ids != '':
        for goods_id in goods_idsl:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name': 1,
               'goods_list': goods_list,
               'option': 1}
    return render(request, 'df_user/user_center_info.html', context)

@login
def order(request):
    """
    此函数用户给下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id，构造购物车对象供订单使用
     """
     uid = request.session.get('user_id')
     user = OrderInfo.objects.filter(user=uid)
     # 获取勾选的每一个订单对象，构造成list，作为上下文传入下单页面
     orderlist = []
     for order in user:
         orderlist.append(order)

     context = {'title': '用户中心', 'page_name': 1, 'option': 2, 'orderlist': orderlist}
     return render(request, 'df_user/user_center_order.html', context)

@login
def Site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        post = request.POST
        user.usjname = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.upost = post.get('uyoubian')
        user.umobile = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1, 'option': 3}
    return render(request, 'df_user/user_center_site.html', context)


























