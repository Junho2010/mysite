from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):
    def get_query(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """
    文章表MODEL
    """
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=250)
    slug = models.SlugField('标签', max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', verbose_name='作者')
    body = models.TextField('内容')
    publish = models.DateTimeField('发布时间', default=timezone.now)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    update = models.DateTimeField('更新时间', auto_now=True)
    status = models.CharField('状态', max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
