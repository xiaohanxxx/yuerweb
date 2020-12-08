from django.shortcuts import render, HttpResponse
from baike import models
import json, datetime, time, random
from django.core.paginator import Paginator
from django.contrib.auth.models import User

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
    text = '''<P>　　人工授精</P>
<P>人工授精成功率<BR>人工授精过程<BR>人工授精价格<BR>人工授精注意事项</P>
<P>　　<STRONG>人工授精成功率</STRONG></P>
<P>　　现在人工授精是很常见的，对这样的做法能够提高怀孕几率，这对一些难怀孕的家莛来讲是一个很好选择，不过对人工授精的成功率是多少呢，在对这个问题上也是很多人不太清楚的，选择人工授精的时候，就需要对各方面问题进行很好认识,使得在选择的时候也是可以放心进行。那人工授精的成功率是多少呢?</P>
<P>　　很多夫妻想要了解人工授精的成功率有多高。其实，人工授精的成功率并不高，一般是20-30%左右，不建议做为首选，而女性受孕是一个比较复杂的生理过程，必须具备以下条件：</P>
<P>　　1、 卵巢排出正常的卵子;</P>
<P>　　2、 精液正常并含有正常的精子;</P>
<P>　　3、 卵子和精子能够在输卵管内相遇并结合成为受精卵;</P>
<P>　　4、 受精卵顺利地被输送进入子宫腔;</P>
<P>　　5、 子宫内膜已充分准备适合于受精卵着床。</P>
<P>　　这些环节中有任何一个不正常，便能阻碍女性受孕的成功。阻碍受孕的原因可能在女方，也可能属男方或在男女双方。建议想要做人工授精的夫妻到专科医院检查是否具备这几顶受孕的条件，根据检查的结果，在医生的指导下对症的治疗后试孕，再做决定。</P>
<P>　　人工授精的成功率差别很大。用丈夫精液人工授精可因精子数和活动率不同而有差异，与操作次数也有关。</P>
<P>　　人工授精的成功率取决于以下几个因素：首先，排卵的可预见性也很重要。月经越规律，怀孕的成功率越高。</P>
<P>　　其次，不育的原因是非常重要的，有良好的精子计数和活动力但不能性交的男性，其人工授精成功的机会明显高于精子有异常的男性。</P>
<P>　　第三，子宫内膜异位症或盆e感染史或输卵管疾病减少成功率，但既往曾怀孕者成功率较高。</P>
<P>　　第四，代孕女方的年龄因素也起着重要作用。如果女方超过35岁，其怀孕机会显著降低。</P>
<P>　　通过以上介绍，对人工授精的成功率是多少呢，都是有着很好认识，因此在对它得选择的时候，都是可以放心进行，这样的做法对女性身体没有任何的损害，不过在对它选择之前，也是需要对各方面问题进行了解，这样在进行的时候，也是可以放心。</P>
<P>　　<STRONG>人工授精的过程</STRONG></P>
<P>　　那么人工授精的过程复杂与否，其中又有哪些步骤呢，我们一起来看一下。</P>
<P>　　人工授精的过程：</P>
<P>　　首先，需对接受人工授精的不孕女性做详细的妇科检查，检查内外生殖器是否正常、子宫内膜活检腺体分泌是否良好、双侧输卵管是否通畅等，若这些都正常，才具备接受人工授精的条件。然后需要估计排卵日，以选择最佳的授精时间。常用的估计排卵日的方法包括铡定</P>
<P>　　基础体温、宫颈粘液&lt;一般在排卵前4-5天出现丨，或接近排卵日连续铡定尿黄体生成素的峰值，或连绫阴道起声波检查等。</P>
<P>　　在女方估计排卵期前，赠精者或丈夫经手淫取出精液，需对精液进行化验，若结果显示精液密度及活动度正常，待其精液液化后，用注射器或导管将精液注入阴道、子宫颈周围及子宫颈管内。女方卧床休息2-3小时使精液不致排出。</P>
<P>　　每位女性在一个月经周期中可进行3次人工授精，即在排卵日前3天开始，若按小时计算，即在排卵日前72小时、24小时和排卵后24小时各进行一次，若在一个月经周期中未能受孕，可连续做几个周期。必要时可用药物诱导排卵和调整好排卵期，以提高受孕率。判定人工授精的成败一般以12个周期为界。</P>
<P>　　<STRONG>人工授精价格</STRONG></P>
<P>　　不少夫妻都希望结婚后拥有一个健康的宝宝，筑造美满的三口之家，然而有的夫妻结婚多年，却因各种原因仍未能怀上◊随着科学技术的发展，人工授精受到越来越多人的接受，这顶医疗成果的成熟也造福了不少家庭，使更多家庭拥有健康的宝宝◊人工受精，即为将男性精液用人工方法注入女性子宫颈或宫腔内，以协助受孕的方法，主要用于由男性原因造成的不孕，如严重的尿道下裂、逆行射精、勃起障碍、无精症、少精症、弱精症、精液不液化症。</P>
<P>　　有些女性方面造成的不孕也能釆用人工受精，如阴道痉挛、宫颈细小、宫颈黏液异常、性交后试验欠佳等◊另外，有一些特殊情況，如免疫学原因的不孕，夫妇双方均是同一种常染色体隐性遗传病的杂合体或男性患常染色体显性遗传病，也可用人工授精的方法。那么人工授精多少钱呢?</P>
<P>　　人工授精每次价格在一般在3000-8000之间，不同的医院价格差别很大，而费用也要根据自身情況而定，跟人工授精难度也有关系。因此想要人工授精的夫妻可以到专业的医院咨询—下，在人工授精前要做好各顶检查，注意个人的清洁卫生，注意休息。</P>
<P>　　<STRONG>人工授精注意事项</STRONG></P>
<P>　　1、人工授精手术完毕后，患者应抬高臀部平卧30分钟，若感到有腹痛、腹胀、阴道不适等症状，应及时通知医务人员，以便及时处理。</P>
<P>　　2、人工授精术后2周内禁止过性生活，也不要洗盆浴。患者可以进行正常的工作及活动，但应避免剧烈运动。</P>
<P>　　3、使用促排卵药物的患者，若人工授精术后出现卵巢过度刺激综合征的症状，如腹胀、恶心、呕吐、体重增加明显、少尿等，应及时去医院进行检查治疗。</P>
<P>　　4、人工授精术后切记每天按照医嘱口服或注射黄体酮，这是非常重要的!意思就是药不能停喔!</P>
<P>　　5、两周后去医院抽血测HCG,确定是否怀孕。如果HCG大于5，恭喜你，怀孕了。接下来还需要口服或注射黄体酮，直至医生告知你可以停药了，还是那句“药不能停喔!”如果HCG小于5，就是没有怀孕，请你听从医生下一步的安排。<BR></P>'''

    # title = text.split('\n')[0].replace('<P>','')
    # title = title.replace('</P>','')
    # title = title.replace('　','')
    # text = text.split('\n')[1:]
    # # print(text)
    # models.Artical.objects.create(
    #     title = title,
    #     category = models.Child_menu.objects.get(id=2),
    #     thumb='thumbnail/gzh.png',
    #     content=''.join(text),
    # )
    return render(request, 'baike.html')


# 百科列表页渲染
def baike_list(request):
    return render(request, 'baike_list.html')


# 文章详情页渲染
def article(request):
    aid = request.GET.get('aid')

    article_obj = models.Artical.objects.get(id=aid)
    article_obj.click_count = article_obj.click_count+1 # 阅读数+1
    article_obj.save()
    x_article = models.Artical.objects.filter(id__gt=aid).order_by('id').first()
    s_article = models.Artical.objects.filter(id__lt=aid).order_by('-id').first()

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
    return render(request, 'article.html',{'article_data':data,'s_article':s_article,'x_article':x_article})


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
# @error
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
                    , 'baike_images': menu.baike_images.url
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




# 获取二级分类文章列表
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



# 获取一级栏目下的分类id及文章
@error
def getmenuarticle(request):
    if request.method == "POST":
        mid = request.POST.get('mid')  # 获取栏目id
        count = request.POST.get('count', 10)  # 获取每页数据条目，默认10条

        menu_obj = models.Bk_menu.objects.get(id=mid)
        child_menu = menu_obj.child_menu_set.all() # 该主栏目id下所有二级栏目

        data = [
            {
                'code':200,
                'msg':'成功',
                'menu_name':menu_obj.menu_name,
                'type':1,
                'list_data':list(
                    {
                        'id':i.id,
                        'menu_name':i.menu_name,
                        'type':2,
                        'list_data':list(
                            i.artical_set.all().values('id','title')[:int(count)]
                        )
                    } for i in child_menu
                )
             }
        ]


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
    # print(data)
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


# 获取最多阅读文章
@error
def articleread(request):
    if request.method == "POST":
        count = request.POST.get('count')
        read_article = models.Artical.objects.all().order_by('-click_count')[:int(count)].values('id','title','click_count')
        data = {
            'code':200,
            'msg':'成功',
            'data':list(read_article)
        }
        return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")


@error
def articlecommend(request):
    if request.method == "POST":
        count = request.POST.get('count')
        read_article = models.Artical.objects.filter(recommend=True)[:int(count)].values('id','title','thumb','excerpt','click_count')
        data = {
            'code':200,
            'msg':'成功',
            'data':list(read_article)
        }
        return HttpResponse(json.dumps(data, cls=JsonCustomEncoder), content_type="application/json")

