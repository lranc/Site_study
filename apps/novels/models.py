from django.db import models
from authors.models import NovelAuthor
# Create your models here.


class Novel(models.Model):
    process_choices = ((1, '已完成'), (2, '连载中'), (3, '暂停'))
    sign_choices = ((1, '已签约'), (2, '未签约'))
    gender_choices = (
        (1, '无'), (2, '言情'), (3, '纯爱'), (4, '百合'),
        (5, '女尊'), (6, '无CP'))
    copyright_choices = ((1, '无'), (2, '原创'), (3, '衍生'))
    era_choices = (
        (1, '无'), (2, '近代现代'), (3, '古色古香'), (4, '架空历史'),
        (5, '幻想未来'))
    type_choices = (
        (1, '无'), (2, '爱情'), (3, '武侠'), (4, '奇幻'), (5, '仙侠'),
        (6, '游戏'), (7, '传奇'), (8, '科幻'), (9, '童话'), (10, '惊悚'),
        (11, '悬疑'), (12, '轻小说'), (13, '古典衍生'), (14, '东方衍生'),
        (15, '西方衍生'), (16, '其他衍生'))
    view_choices = (
        (1, '无'), (2, '男主'), (3, '女主'), (4, '主攻'), (5, '主受'),
        (6, '互攻'), (7, '不明'))
    style_choices = (
        (1, '无'), (2, '悲剧'), (3, '正剧'), (4, '轻松'), (5, '爆笑'),
        (6, '暗黑'))
    author = models.ForeignKey(NovelAuthor, on_delete=models.CASCADE, verbose_name='作者', related_name="novel", null=True)
    novel_id = models.IntegerField(primary_key=True)
    novel_name = models.CharField(max_length=25, verbose_name="作品名")
    url = models.URLField()
    novel_intro = models.TextField(max_length=1500, verbose_name='作品简介')
    search_key = models.CharField(max_length=50, verbose_name='查询关键字')
    copyright = models.IntegerField(choices=copyright_choices, verbose_name='原创性', null=True, )
    gender_view = models.IntegerField(choices=gender_choices, verbose_name='性向', null=True)
    era = models.IntegerField(choices=era_choices, verbose_name='时代', null=True)
    noveltype = models.IntegerField(choices=type_choices, verbose_name='类型', null=True)
    novel_view = models.IntegerField(choices=view_choices, verbose_name='作品视角', null=True)
    novel_style = models.IntegerField(choices=style_choices, verbose_name='作品风格', null=True)
    novel_series = models.CharField(max_length=40, verbose_name='作品系列')
    novel_progress = models.IntegerField(choices=process_choices, verbose_name='作品状态')
    novel_word_count = models.IntegerField(verbose_name='作品字数')
    novel_publish = models.CharField(max_length=30, verbose_name='出版情况')
    novel_sign = models.IntegerField(choices=sign_choices, verbose_name='签约情况')
    novel_criticism = models.TextField(max_length=1000, verbose_name='作品简评')
    novel_bawangrank = models.IntegerField(verbose_name='霸王票排行')
    novel_bawangnum = models.IntegerField(verbose_name='霸王票数量')
    total_download = models.IntegerField(verbose_name='总下载数')
    novip_click = models.IntegerField(verbose_name='非VIP点击')
    total_comment = models.IntegerField(verbose_name='总评论数')
    current_collect_count = models.IntegerField(verbose_name='被收藏数')
    nutrient_count = models.IntegerField(verbose_name='营养液数')
    novel_score = models.IntegerField(verbose_name='文章积分')
    chapter_count = models.IntegerField(verbose_name='章节数量')
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text='点击数')

    def __str__(self):
        return self.novel_name


class NovelTags(models.Model):

    choices = (
        (1, '无'), (2, '快穿'), (3, '甜文'), (4, '穿书'), (5, '重生'),
        (6, '娱乐圈'), (7, '爽文'), (8, '系统'), (9, '穿越时空'), (10, '种田文'),
        (11, '综漫'), (12, '仙侠修真'), (13, '随身空间'), (14, '强强'),
        (15, '生子'), (16, '星际'), (17, '情有独钟'), (18, '豪门世家'),
        (19, '年代文'), (20, '英美衍生'), (21, '末世'), (22, '校园'),
        (23, '女配'), (24, '灵异神怪'), (25, '无限流'), (26, '网王'),
        (27, '美食'), (28, '虐恋情深'), (29, '超级英雄'), (30, '青梅竹马'),
        (31, '火影'), (32, '破镜重圆'), (33, '我英'), (34, '异能'),
        (35, '性别转换'), (36, '天作之合'), (37, '游戏网游'), (38, '清穿'),
        (39, '打脸'), (40, '异世大陆'), (41, '宫廷侯爵'), (42, '直播'),
        (43, '少年漫'), (44, '家教'), (45, '都市情缘'), (46, '天之骄子'),
        (47, '悬疑推理'), (48, '武侠'), (49, '古穿今'), (50, '现代架空'),
        (51, '女强'), (52, '未来架空'), (53, '升级流'), (54, '宫斗'),
        (55, '猎人'), (56, '少女漫'), (57, '前世今生'), (58, '民国旧影'),
        (59, '年下'), (60, '励志人生'), (61, '复仇虐渣'), (62, '逆袭'),
        (63, '婚恋'), (64, '竞技'), (65, '黑篮'), (66, '东方玄幻'),
        (67, '奇幻魔幻'), (68, '幻想空间'), (69, '红楼梦'), (70, '恐怖'),
        (71, '历史衍生'), (72, '布衣生活'), (73, '女扮男装'), (74, '日韩'),
        (75, '海贼王'), (76, '机甲'), (77, '洪荒'), (78, '西幻'), (79, '网红'),
        (80, '平步青云'), (81, '科举'), (82, '业界精英'), (83, '灵魂转换'),
        (84, '市井生活'), (85, '朝堂之上'), (86, '西方罗曼'), (87, '相爱相杀'),
        (88, '齐神'), (89, '因缘邂逅'), (90, '宅斗'), (91, '科幻'), (92, '血族'),
        (93, '古代幻想'), (94, '西方名著'), (95, '江湖恩怨'), (96, '魔法幻情'),
        (97, '死神'), (98, '异国奇缘'), (99, '港台'), (100, '原著向'),
        (101, '花季雨季'), (102, '近水楼台'), (103, '都市异闻'),
        (104, '古典名著'), (105, '成长'), (106, '网配'), (107, '银魂'),
        (108, '乔装改扮'), (109, '姐弟恋'), (110, '美娱'), (111, '制服情缘'),
        (112, '阴差阳错'), (113, '时代奇缘'), (114, '亡灵异族'), (115, '小门小户'),
        (116, '史诗奇幻'), (117, '传奇'), (118, '授权衍生'), (119, '职场'),
        (120, '商战'), (121, '恋爱合约'), (122, '三教九流'), (123, '经商'),
        (124, '骑士与剑'), (125, '异闻传说'), (126, '边缘恋歌'), (127, '七五'),
        (128, '七年之痒'), (129, '乡村爱情'), (130, '聊斋'), (131, '霹雳'),
        (132, '异想天开'), (133, '圣斗士'), (134, '爱情战争'), (135, '时尚流行'),
        (136, '奇谭'), (137, '大冒险'), (138, 'SD'), (139, '婆媳')
        )
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, verbose_name='作品', related_name="noveltags")
    novel_tag = models.IntegerField(choices=choices, verbose_name='作品标签')

    class meta:
        verbose_name = '作品标签'
        ordering = 'novel'