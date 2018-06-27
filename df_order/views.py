# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.shortcuts import render, redirect
from df_user.models import UserInfo
from df_cart.models import CartInfo
from df_user import user_decorator
from df_goods.models import GoodsInfo
from models import *
from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse

@user_decorator.login
def Order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')

    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    # 判断用户手机号是否为空，分别做展示
    if user.umobile == '':
        umobile = ''
    else:
        umobile = user.umobile[0:3] + \
                 '****' + user.umobile[-4:]

    # 构造传递到模板中的数据
    context = {'title': '提交订单',
               'page_name': 1,
               'carts': carts,
               'user': user,
               'umobile': umobile,
               'cart_ids': ','.join(cart_ids)}
    print cart_ids1
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@user_decorator.login
def Order_handle(request):
    tran_id = transaction.savepoint()
    try:
        post = request.POST
        print "+++++++++++[" + post + "]+++++++++++"
        orderlist = post.getlist('id[]')
        total = post.get('total')
        address = post.get('address')

        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('user_id')
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(total)
        order.oaddress = address
        order.save()

        # 遍历购物车中提交信息，创建订单详情表
        for orderid in orderlist:
            cartinfo = CartInfo.objects.get(id=orderid)
            # good = GoodsInfo.objects.get(cartinfo__id=cartinfo.id)
            good = GoodsInfo.objects.get(pk=cartinfo.goods_id)
            # print '*'*10
            # print cartinfo.goods_id
            # 判断库存是否够
            if int(good.gkucun) >= int(cartinfo.count):
                # 库存够，移除购买数量并保存
                good.gkucun -= int(cartinfo.count)
                good.save()

                goodinfo = GoodsInfo.objects.get(cartinfo__id=orderid)

                # 创建订单详情表
                detailinfo = OrderDetailInfo()
                detailinfo.goods_id = int(goodinfo.id)
                detailinfo.order_id = int(order.oid)
                detailinfo.price = Decimal(int(goodinfo.gprice))
                detailinfo.count = int(cartinfo.count)
                detailinfo.save()

                # 循环删除购物车对象
                cartinfo.delete()
    #接收购物车编号
    # cart_ids = request.POST.get('cart_ids[]')
    # print "+++++++++++[" + cart_ids + "]+++++++++++"
    # try:
    #     #创建订单对象
    #     order = OrderInfo()
    #     now = datetime.now()
    #     uid = request.session['user_id']
    #     order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
    #     order.user_id = uid
    #     order.odate = now
    #     order.ototal = Decimal(request.POST.get('total'))
    #     order.save()
    #     #创建详单对象
    #     cart_ids1 = [int(item) for item in cart_ids.split(',')]
    #     for id1 in cart_ids1:
    #         detail = OrderDetailInfo()
    #         detail.order = order
    #         # 查询购物车信息
    #         cart = CartInfo.objects.get(id=id1)
    #         # 判断商品库存
    #         goods = cart.goods
    #         if goods.gkucun >= cart.count:
    #             goods.gkucun = cart.goods.gkucun - cart.count
    #             goods.save()
    #             # 完善详单信息
    #             detail.goods_id = goods.id
    #             detail.price = goods.gprice
    #             detail.count = cart.count
    #             detail.save()
    #             # 删除购物车数据
    #             cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                # 返回json供前台提示失败
                return JsonResponse({'status': 2})
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print "=============%s=========="%e
        transaction.savepoint_rollback(tran_id)
    return JsonResponse({'status': 1})

@user_decorator.login
def Pay(request, oid):
    tran_id = transaction.savepoint()
    # try:
    order = OrderInfo.objects.get(oid=oid)
    order.zhifu = 1

    order.save()
    # except Exception as e:
    # print '==================%s' % e
    # transaction.savepoint_rollback(tran_id)
    print '*' * 10
    print order.zhifu
    print order.oid
    context = {'oid': oid}
    return render(request, 'df_order/pay.html', context)
    # order = OrderInfo.objects.get(oid=oid)
    # order.oIsPay = True
    # order.save()
    # context = {'order': order}
    # return render(request, 'df_order/pay.html', context)
