from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render, get_object_or_404
from .models import User, Competition, Team, Discussion, TeamApplication, Notification
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    return render(request, "home.html")

def blog(request):
    # if request.method == 'POST':

    #     # 获取POST数据
    #     name = request.POST.get('name')
    #     url = request.POST.get('url')
    #     # 获取其他表单字段
    #     start_regi = request.POST.get('start_regi')
    #     end_regi = request.POST.get('end_regi')
    #     start_compt = request.POST.get('start_compt')
    #     number = request.POST.get('number')
    #     intro = request.POST.get('intro')
    #     category = request.POST.get('category')


    #     # 检查 content 是否存在
    #     if name:
    #         # 创建 new_competition 对象并将其保存到数据库
    #         new_competition = Competition(
    #                 name=name,
    #                 url=url,
    #                 start_regi=start_regi,
    #                 end_regi=end_regi,
    #                 start_compt=start_compt,
    #                 number=number,
    #                 intro=intro,
    #                 category=category
    #             )
    #         new_competition.save()

    #         # 返回响应，可以是重定向或其他响应
    #         return HttpResponse('讨论已发布')
    competition = Competition.objects.all()  # 查询数据库中的所有Discussion对象
    print(competition)
    return render(request, "blog.html",  {'competition': competition})

# 新建竞赛
# path('competition/add/', views.competition_add)
# from django.contrib import messages 增加弹窗功能
def competition_add(request):
    # 默认为 POST 表单    
    name = request.POST.get("name")
    url = request.POST.get("url")
    inputfile = request.FILES.get('inputfile')
    number = request.POST.get("number")
    
    # 竞赛类别单选项
    category = request.POST.get("category")

    start_regi = request.POST.get("start_regi")
    end_regi = request.POST.get("end_regi")
    start_compt = request.POST.get("start_compt")
    intro = request.POST.get("intro")

    # 处理上传的文件
    if inputfile:
        # 保存文件到media目录中
        file_name = default_storage.save('competition_images/' + inputfile.name, ContentFile(inputfile.read()))

        # 获取文件的URL
        file_url = 'competition_images/' + inputfile.name

    Competition.objects.create(name = name,
                                url = url, 
                                image = file_url,
                                number = number,
                                category = category,
                                start_regi = start_regi,
                                end_regi = end_regi,
                                start_compt = start_compt,
                                intro = intro
                                )
    # return HttpResponse("添加成功")
    messages.error(request, '添加成功')
    return redirect("/blog/") # urls.py 中的 blog.html 地址

# 删除竞赛
# path('competition/delete/', homeviews.competition_delete),
def competition_delete(request):
    nid = request.GET.get("nid")
    Competition.objects.filter(id=nid).delete()
    # return HttpResponse("删除成功")
    messages.error(request, '删除成功')
    return redirect("/blog/")

# 依据文本输入搜索竞赛
# path('blog/search/', homeviews.blog_search),
def blog_search(request):
    # 默认为 GET
    input = request.GET.get('input')
    error_msg = ''

    if not input:
        error_msg = '请输入关键词'
        return render(request, 'blog.html', {'error_msg': error_msg})

    competition = Competition.objects.filter(name = input)

    return render(request, "blog.html",  {'error_msg': error_msg, 'competition': competition})

# 发布评论
def blogs(request, competition_id):
    if request.method == 'POST':
        # 获取当前登录用户
        user = request.user
        if not user.is_authenticated:
            return redirect('/login/')
        # user = User.objects.first()
        competition = Competition.objects.get(pk=competition_id)

        # 获取POST数据
        content = request.POST.get('comment')

        # 检查 content 是否存在
        if content:
            # 创建 Discussion 对象并将其保存到数据库
            new_discussion = Discussion(content=content, user=user, competition=competition)
            new_discussion.save()

            # 返回响应，可以是重定向或其他响应
            return HttpResponse('讨论已发布')
    # 获取所有Discussion对象
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    competition = Competition.objects.get(pk=competition_id)
    teams = Team.objects.filter(competition=competition)
    print(teams)
    discussions = Discussion.objects.filter(competition=competition)
    return render(request, 'blog-single.html', {'competition': competition, 'discussions': discussions, 'teams': teams ,'user': user})



# 加入 competition_id 竞赛下的 team_id 团队
def team_join(request, competition_id, team_id): 
    team = Team.objects.get(pk=team_id)
    application = TeamApplication.objects.create(applicant=request.user, team=team, status='pending')

    #给队长的信息
    Notification.objects.create(
        recipient=team.creator,
        content=f"{request.user.user_name} 申请加入你们的队伍 {team.name}.",
        related_application=application
    )

    #给申请者的信息
    Notification.objects.create(
        recipient=request.user,
        content=f"你申请加入队伍 {team.name}.",
        related_application=application
    )

    print(application)

    return redirect("/personal/")


# 创建 competition_id 竞赛下新的 team
def team_add(request, competition_id):
    
    # 默认为 POST
    
    name = request.POST.get("name")
    intro = request.POST.get("intro")
    # 获取当前登录用户
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')

    # 获取当前竞赛
    competition = Competition.objects.get(pk=competition_id)
    Team.objects.create(name = name,
                        competition = competition, 
                        creator = user,
                        intro = intro
                        )
    # Question: members 如何添加到 team 中
    # 注意 在 models 添加 intro 字段 
    # 返回
    competition = Competition.objects.get(pk=competition_id)
    teams = Team.objects.filter(competition=competition)
    discussions = Discussion.objects.filter(competition=competition)
    return render(request, 'blog-single.html', {'competition': competition, 'discussions': discussions, 'teams': teams})

# 依据标签输入搜索竞赛
# path('competition/delete/', homeviews.competition_search),
def competition_search(request, type):
    competition = Competition.objects.filter(category=type)
    # return HttpResponse("删除成功")

    return render(request, "blog.html",  {'competition': competition})

def team_search(request, competition_id):
    # print("team_search")
    competition = Competition.objects.get(pk=competition_id)
    input = request.GET.get('input')
    teams = Team.objects.filter(competition=competition, name=input)
    print(teams)
    discussions = Discussion.objects.filter(competition=competition)
    return render(request, 'blog-single.html', {'competition': competition, 'discussions': discussions, 'teams': teams})
    # 希望跳转到界面2：团队列表
    # 默认为 GET

# # 删除成员
# def member_delete(request, nid):
#     Team.members.objects.filter(id=nid).delete()
#     return redirect('/blog-single/')



# def blogs(request, competition_id):
#     # 创建一个新的 User 实例
#     new_user = User(
#         user_name="开心超人",
#         user_id=3,  # 你需要选择一个唯一的学号
#         user_password="2003",
#         profile="images/1成员1.jpeg",  # 上传的头像文件路径
#         bio="我是开心超人",
#         major="Attaker Science"
#     )

#     # 保存该实例到数据库
#     new_user.save()
#     # 创建一个新的 Competition 实例
#     new_competition = Competition(
#         name="全国大学生数学竞赛",
#         image="images/数学.png",  # 上传的竞赛图片文件路径
#         start_regi="2023-11-01",
#         end_regi="2023-12-25",
#         start_compt="2023-11-30",
#         url="http://www.cmathc.cn/",
#         number=100,
#         intro="全国大学生数学竞赛,非常challenge",
#         category=1  # 使用合适的类别值
#     )

#     # 保存该实例到数据库
#     new_competition.save()
#     # # 创建一个新的 Team 实例
#     # new_team = Team(
#     #     name="超人队",
#     #     competition=new_competition,  # 将团队与特定竞赛相关联
#     #     creator=new_user,  # 将团队的创建者设置为特定用户
#     # )

#     # # 保存该实例到数据库
#     # new_team.save()
#     # # 创建一个新的 Discussion 实例
#     # new_discussion = Discussion(
#     #     content="good good",
#     #     user=new_user,  # 将讨论与特定用户相关联
#     #     competition=new_competition,  # 将讨论与特定竞赛相关联
#     # )
#     # # 保存该实例到数据库
#     # new_discussion.save()
#     competition = Competition.objects.get(pk=competition_id)
#     teams = Team.objects.filter(competition=competition)
#     discussions = Discussion.objects.filter(competition=competition)
#     return render(request, 'blog-single.html', {'competition': new_competition, 'discussions': discussions, 'teams': teams})
