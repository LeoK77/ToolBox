# 目的：将Markdown源文件中的https图片连接替换为本地图片连接，前提是图片仓库已经在本地pull好了

# 我的Hexo本地文件夹中source的目录结构：
# source
# ├─...
# ├─_drafts
#     ├─ComputerScience
#       ├─使用UbuntuPastebin分享文本.md
# (即 "_drafts/ComputerScience/使用UbuntuPastebin分享文本.md" —— 草稿/分类/文章名字)
#       ├─...
#     ├─...
# └─_posts
#     ├─ComputerScience
#       ├─使用UbuntuPastebin分享文本.md
# (即 "_posts/ComputerScience/使用UbuntuPastebin分享文本.md" —— 发布的文章/分类/文章名字)
#       ├─...
#     ├─...
# └─...

# 我的Gitee图床仓库储存图片的目录结构
# Blog-Img-LeoK77
# ├─ComputerScience
# │  ├─使用UbuntuPastebin分享文本
# |    ├─20210314213131.png
# (即 "ComputerScience/使用UbuntuPastebin分享文本/20210314213131.png" —— 分类/文章名字/图片名字)
# |    ├─...
# |  ├─...
# ├─...
import path_analysis
import shutil
import os


# 去除文章中指定的要删除的内容(单行删除)
def article_sentence_remove(article_path: str, str_sentence_remove: str):
    abspath_src = os.path.abspath(article_path)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = path_analysis.get_abspath_dst(abspath_src)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                dst_file.write(line.replace(str_sentence_remove, ""))
    path_analysis.replace_or_not(abspath_src, abspath_dst)


# 将文章保存到本地
def save_local(src_path_blog_source_dir: str, src_path_img: str, dst_path: str, str_remove: str):
    src_path_blogs = [
        src_path_blog_source_dir + '_posts',
        src_path_blog_source_dir + '_drafts'
    ]
    for index in range(len(src_path_blogs)):
        src_path_blogs[index] = os.path.abspath(src_path_blogs[index])
    src_path_img = os.path.abspath(src_path_img)
    dst_path = os.path.abspath(dst_path)
    # 复制文章及图片到指定位置
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    os.makedirs(dst_path)
    for src_path_blog in src_path_blogs:
        path_analysis.copy_files(src_path_blog, dst_path)
    path_analysis.copy_files(src_path_img, dst_path)
    # 文章中图片连接重定向到本地
    all_filepath = path_analysis.get_all_filepath_class(dst_path)
    for index in range(len(all_filepath)):
        full_path = all_filepath[index].get_full_path()
        if full_path.find(".md") != -1:
            file_path_without_root_dir = all_filepath[index].get_filepath_without_root_dir()
            str_remove += file_path_without_root_dir.replace(
                os.path.basename(file_path_without_root_dir), ''
            ).replace(os.sep, '/')
            article_sentence_remove(full_path, str_remove)


if __name__ == '__main__':
    save_local(
        r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/',
        r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Img-LeoK77',
        r'D:/Study/HexoArticles',
        "https://gitee.com/leok77/blog-img-leok77/raw/main"
    )
