from django.contrib import admin

# Register your models here.
from mysite.models import Article

class ArticleAdmin(admin.ModelAdmin):
    # 显示字段成员
    list_display = ('title', 'author', 'content_and_score')
    search_fields = ('title',)
 
    # 后台搜索功能
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ArticleAdmin, self).get_search_results(request, queryset, search_term)
        try:
            queryset |= self.model.objects.filter(title = search_term)
        except:
            pass
        return queryset, use_distinct


admin.site.register(Article, ArticleAdmin)