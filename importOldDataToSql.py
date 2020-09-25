'''
django批量导入数据到现有数据库中
'''
import os
# 脚本使用django之前要先告诉使用哪个seting文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doomfist.settings")

# django banben dayu 1.7deshihou, 需要加上下面两句
import django
if django.VERSION >= (1, 7):
    django.setup()

def main():
    from mysite.models import Blog
    with open(r"mysite\oldData\oldBlogData.txt", "r", encoding = "utf-8") as f:
        for line in f.readlines():
            name, tagline = line.split('****')
            Blog.objects.create(name = name, tagline = tagline)
            # 可用这个代替, 插入之前先判断是否创建， 效率要慢一点
            # Blog.objects.get_or_create(name = name, tagline = tagline)
    
    # BlgList列表存贮BLog对象，bulk_create只执行一条数据库语句，提高效率。
    # Blog.objects.bulk_create(BlogList)

if __name__ == "__main__":
    main()
    print("done!")