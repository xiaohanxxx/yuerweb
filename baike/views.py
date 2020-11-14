from django.shortcuts import render, HttpResponse
from baike import models
import json, datetime, time, random
from django.core.paginator import Paginator


# Create your views here.

# json序列化方法重写
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime.datetime):
            return (field + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
        elif isinstance(field, datetime.date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


# 函数运行时间计算装饰器
def GetRunTime(func):
    def call_func(*args, **kwargs):
        begin_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        Run_time = end_time - begin_time
        print(str(func.__name__) + "函数运行时间为" + str(Run_time))
        return ret

    return call_func


# 异常处理装饰器
def error(func):
    def errorcase(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except:
            data = {
                'code': 400,
                'msg': '获取数据失败',
                'data': []
            }
            return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")

    return errorcase


# 百科主页渲染
def baike(request):
    return render(request, 'baike.html')


# 百科列表页渲染
def baike_list(request):
    return render(request, 'baike_list.html')


# 文章详情页渲染
def article(request):
    aid = request.GET.get('aid')
    article_obj = models.Artical.objects.get(id=aid)
    data = {
        'code': 200,
        'msg': 'success',
        'data': [
            {
                'id': article_obj.id,
                'category_id': article_obj.category_id,
                'title': article_obj.title,
                'author': article_obj.author,
                'excerpt': article_obj.excerpt,
                'thumb': article_obj.thumb,
                'recommend': article_obj.recommend,
                'content': article_obj.content,
                'click_count': article_obj.click_count,
                'add_time': article_obj.add_time
            }
        ]
    }
    return render(request, 'article.html',{'article_data':data})


# 获取栏目api,1,2级栏目
@error
def baikemenuapi(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        code = 200
        msg = '成功'
        if int(type) == 1:
            menu = models.Bk_menu.objects.all().values()
        elif int(type) == 2:
            menu = models.Child_menu.objects.all().values()
        else:
            code = 400
            msg = '接口错误'
            menu = list()
        data = {
            'code': code,
            'msg': msg,
            'data': list(menu)
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


# def xTree(data):
#     resData = []
#     for i in data:
#         chk = {"id": i.id, "menu_name": i.menu_name, "child": []}
#         if i.child_menu_set.all():
#             chk['child'] = xTree(i.child_menu_set.all())
#         resData.append(resData)
#     return resData


# 获取百科全部三级栏目api
@GetRunTime
def sjldapi(request):
    if request.method == "POST":
        count = request.POST.get('count')
        menu_one = models.Bk_menu.objects.all()
        data = list()
        for menu in menu_one:
            data.append(
                {
                    'mid': menu.id
                    , 'menu_name': menu.menu_name
                    , 'type': '1'
                    , 'children': list(
                    {
                        'mid': child.id
                        , 'menu_name': child.menu_name
                        , 'type': '2'
                        , 'children': list(
                        {
                            'articleid': article['id']
                            , 'title': article['title']
                        }
                        for article in child.artical_set.all().values('id', 'title')[:int(count)]
                    )
                    }
                    for child in menu.child_menu_set.all()
                )
                }
            )
        return HttpResponse(json.dumps(data), content_type="application/json")




# 获取分类文章列表
@error
def articlelistapi(request):
    mid = request.POST.get('mid')  # 获取栏目id
    page = request.POST.get('page', 1)  # 获取页码
    count = request.POST.get('count', 10)  # 获取每页数据条目，默认10条

    menu_obj = models.Child_menu.objects.get(id=mid)
    menu_name = menu_obj.menu_name  # 二级栏目名
    article_list = menu_obj.artical_set.all().values('id', 'title', 'category_id', 'author', 'thumb', 'recommend',
                                                     'excerpt', 'click_count', 'add_time')  # 查询该三级栏目id下的文章数据
    paginator = Paginator(article_list, count)  # 分页
    page_data = paginator.page(page)  # 获取对应页码文章
    page_sum = paginator.num_pages  # 栏目下总页数
    data = {
        'code': 200,
        'msg': 'success',
        'menu_name': menu_name,
        'pages': page_sum,
        'data': list(page_data.object_list)
    }

    # print(json.dumps(data,cls=JsonCustomEncoder))
    return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")


# 获取文章最新列表
@error
def articletimelist(request):
    count = request.POST.get('count', 10)  # 获取每页数据条目，默认10条
    article_list = models.Artical.objects.all()[:int(count)].values()
    data = {
        'code': 200,
        'msg': 'success',
        'data': list(article_list)
    }
    print(data)
    return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")


# 获取文章详情
@error
def articleapi(request):
    aid = request.GET.get('aid')
    article_obj = models.Artical.objects.get(id=aid)
    data = {
        'code': 200,
        'msg': 'success',
        'data': [
            {
                'id': article_obj.id,
                'category_id': article_obj.category_id,
                'title': article_obj.title,
                'author': article_obj.author,
                'excerpt': article_obj.excerpt,
                'thumb':article_obj.thumb,
                'recommend':article_obj.recommend,
                'content': article_obj.content,
                'click_count': article_obj.click_count,
                'add_time': article_obj.add_time
            }
        ]
    }
    return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")
