# -*- coding:utf8 -*-
from pure_pagination import Paginator, PageNotAnInteger


def get_page_data(request, all_data, perpage):
    try:
        page_num = request.GET.get('page', 1)
    except PageNotAnInteger:
        page_num = 1

    p = Paginator(all_data, perpage, request=request)

    datas = p.page(page_num)
    return datas
