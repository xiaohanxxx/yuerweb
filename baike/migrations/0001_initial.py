# Generated by Django 3.1.2 on 2020-11-02 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bk_menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=50, verbose_name='栏目名称')),
                ('is_active', models.BooleanField(default=True, verbose_name='显示')),
                ('idx', models.IntegerField(verbose_name='排序')),
            ],
            options={
                'verbose_name': '百科栏目',
                'verbose_name_plural': '百科栏目',
            },
        ),
        migrations.CreateModel(
            name='Child_menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.CharField(max_length=50, verbose_name='子栏目名称')),
                ('is_active', models.BooleanField(default=True, verbose_name='显示')),
                ('idx', models.IntegerField(verbose_name='排序')),
            ],
            options={
                'verbose_name': '百科分类',
                'verbose_name_plural': '百科分类',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.CharField(max_length=50, verbose_name='栏目名称')),
                ('is_active', models.BooleanField(default=True, verbose_name='显示')),
                ('idx', models.IntegerField(verbose_name='排序')),
                ('relation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='baike.bk_menu', verbose_name='上级栏目')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Artical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('author', models.CharField(default='育儿网', max_length=30, verbose_name='作者')),
                ('content', models.TextField(verbose_name='内容')),
                ('excerpt', models.CharField(blank=True, max_length=100, verbose_name='摘要')),
                ('click_count', models.IntegerField(default=0, verbose_name='点击次数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='baike.menu', verbose_name='文章栏目')),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
                'ordering': ['-add_time'],
            },
        ),
    ]