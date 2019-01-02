from django.db import models
# Create your models here.


class NovelAuthor(models.Model):
    '''
    作者
    '''
    choices = (('1', '已完成'), ('2', '连载中'), ('3', '已暂停'))
    url = models.URLField()
    author_id = models.IntegerField(primary_key=True)
    author_name = models.CharField(max_length=25, verbose_name="作者名", help_text="作者名")
    column_name = models.CharField(max_length=25, verbose_name="专栏名", help_text="专栏名")
    specil_column = models.BooleanField(default=False, verbose_name="是否驻站", help_text="是否驻站")
    column_confession = models.TextField(max_length=500, verbose_name="作者自白", help_text="作者自白")
    collected_num = models.IntegerField(default=0, verbose_name="被收藏数")
    author_notice = models.TextField(max_length=500, verbose_name="主人告示")
    author_weibo = models.URLField(verbose_name='作者微博')
    send_gift = models.IntegerField(default=0, verbose_name='发出红包')
    good_novel = models.TextField(max_length=50)
    last_novel_id = models.IntegerField(default=0, verbose_name='最新作品id',null=True, blank=True)
    last_update_novel = models.CharField(max_length=100, verbose_name="最新作品名",null=True, blank=True)
    last_novel_status = models.CharField(max_length=1, choices=choices, verbose_name='最新作品状态',null=True, blank=True)
    last_novel_word_count = models.IntegerField(default=0, verbose_name='最新作品字数',null=True, blank=True)
    last_update_time = models.DateTimeField(null=True, blank=True, verbose_name='最后更新时间')
    click_num = models.IntegerField(default=0, verbose_name="点击数", help_text='点击数')

    class Meta:
        verbose_name = '作者信息'
        verbose_name_plural = verbose_name
        ordering = ['author_id']

    def __str__(self):
        return self.author_name


class FriendChain(models.Model):
    '''
    作者友链
    '''
    author = models.ForeignKey(NovelAuthor, on_delete=models.CASCADE, verbose_name="作者", related_name="friend_chain")
    friend_chain = models.IntegerField(verbose_name="友链作者id", null=True, blank=True)

    class Meta:
        verbose_name = "作者友链"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.author_name


class AuthorReader(models.Model):
    '''
    霸王排行榜
    '''
    author = models.ForeignKey(NovelAuthor, on_delete=models.CASCADE, verbose_name="作者", related_name="reader_rank")
    ranking = models.CharField(max_length=2, verbose_name='霸王票排行')
    reader_id = models.IntegerField(verbose_name='读者id', null=True)
    reader_name = models.CharField(max_length=25, verbose_name='读者名')
    reader_score = models.IntegerField(verbose_name='分数')
    reader_level = models.CharField(max_length=5, verbose_name='读者等级')

    class Meta:
        verbose_name = '读者霸王票'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.reader_name
