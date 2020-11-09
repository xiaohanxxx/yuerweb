from django.shortcuts import render, HttpResponse
from baike import models
import json,datetime
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

# 百科主页
def baike(request):
    return render(request, 'baike.html')

# 百科列表页
def baike_list(request):
    return render(request,'baike_list.html')

# 文章详情页
def article(request):
    return render(request,'article.html')



# 异常处理装饰器
def error(func):
    def errorcase(request, *args, **kwargs):
        try:
            func(request, *args, **kwargs)
        except:
            data = {
                'code':400,
                'msg':'获取数据失败',
                'data':[]
            }
            return HttpResponse(json.dumps(data,cls=JsonCustomEncoder), content_type="application/json")
    return errorcase



# 获取栏目api,1,2,3级栏目

def baikemenuapi(request):
    if request.method == 'POST':
        type = request.GET.get('type')
        code = 200
        msg = '成功'
        if int(type) == 1:
            menu = models.Bk_menu.objects.all().values()
        elif int(type) == 2:
            menu = models.Child_menu.objects.all().values()
        elif int(type) == 3:
            menu = models.Menu.objects.all().values()
        else:
            code = 400
            msg = '接口错误'
            menu = list()

        data = {
            'code': code,
            'msg': msg,
            'menu': list(menu)
        }
        return HttpResponse(json.dumps(data), content_type="application/json")



# 获取百科全部三级栏目api
@error
def sjldapi(request):
    menu_one = models.Bk_menu.objects.all()
    data = []
    for i in menu_one:
        child = i.child_menu_set.all()
        for j in child:
            menu = j.menu_set.all()
            data.append(
                {
                    'id': i.id,
                    'menu_name': i.menu_name,
                    'type': 1,
                    'children': [
                        {
                            'id': j.id,
                            'menu_name': j.child_name,
                            'type': 2,
                            'children': [{"id": i.id, "menu_name": i.child_name, 'type': 3} for i in menu]
                        }
                    ],
                }
            )
    return HttpResponse(json.dumps(data), content_type="application/json")


# 获取分类文章列表
@error
def articlelistapi(request):
    mid = request.GET.get('mid') # 获取栏目id
    page = request.GET.get('page',1) # 获取页码
    count = request.GET.get('count',10) # 获取每页数据条目，默认10条

    menu_obj = models.Menu.objects.get(id=mid)
    menu_name = menu_obj.child_name # 三级栏目名
    article_list = menu_obj.artical_set.all().values('id','title','category_id','author','excerpt','click_count','add_time') # 查询该三级栏目id下的文章数据
    paginator = Paginator(article_list,count) # 分页
    page_data = paginator.page(page) # 获取对应页码文章
    page_sum = paginator.num_pages  # 栏目下总页数
    data = {
        'code':200,
        'msg':'success',
        'menu_name':menu_name,
        'pages':page_sum,
        'data':list(page_data.object_list)
    }

    # print(json.dumps(data,cls=JsonCustomEncoder))
    return HttpResponse(json.dumps(data,cls=JsonCustomEncoder), content_type="application/json")





from django.views import View
# from rest_framework.views import APIView

# # CBV test
# class OrderView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('获取订单')
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('创建订单')
#
#     def put(self, request, *args, **kwargs):
#         return HttpResponse('修改订单')
#
#     def delete(self, request, *args, **kwargs):
#         return HttpResponse('删除订单')

# 获取文章内容
@error
def articleapi(request):
    aid = request.GET.get('aid')
    article_obj = models.Artical.objects.get(id=aid)
    data = {
        'code':200,
        'msg':'success',
        'data':[
            {
                'id':article_obj.id,
                'category_id': article_obj.category_id,
                'title':article_obj.title,
                'author':article_obj.author,
                'excerpt':article_obj.excerpt,
                'content':article_obj.content,
                'click_count':article_obj.click_count,
                'add_time':article_obj.add_time
            }
        ]
    }
    return HttpResponse(json.dumps(data,cls=JsonCustomEncoder), content_type="application/json")

