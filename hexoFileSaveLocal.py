# 将hexo博客的markdown文件本地化，因为现在使用的是Gitee当图床，所以本地不联网的情况下无法看Markdown里的图片
# 说白了就是将gitee图床的图片都储存在本地，然后将Markdown里的img-url替换为本地连接
import path_analysis
import shutil
import os


def gitee_img_to_local(filename='', replacestr=''):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = path_analysis.get_abspath_dst(abspath_src)

    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                dst_file.write(line.replace(replacestr, ""))
    path_analysis.replace_or_not(abspath_src, abspath_dst)


if __name__ == '__main__':
    # Markdown源文件所在目录
    src_path_blog = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/_posts'
    src_path_blog = os.path.abspath(src_path_blog)
    # Blog-img源文件所在目录
    src_path_img = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Img-LeoK77'
    src_path_img = os.path.abspath(src_path_img)
    print(src_path_img)
    # Markdown目标存储目录
    dst_path_blog = r'D:/Study/BlogFiles'
    dst_path_blog = os.path.abspath(dst_path_blog)
    # 如果目标目录存在则删除此目录，避免复制失败
    if os.path.exists(dst_path_blog):
        shutil.rmtree(dst_path_blog)
    # 递归的将所有源文件都复制到目标文件处
    shutil.copytree(src_path_blog, dst_path_blog)
    path_analysis.copy_files(src_path_img, dst_path_blog)
    # 所有源文件，元组[0]是全地址，[1]是去除root_path的地址
    paths_md = path_analysis.get_both_path(dst_path_blog)
    index = 0
    while index < len(paths_md):
        # 删除源文件中的非Markdown文件
        if paths_md[index][0].find(".md") != -1:
            # markdown文件需要进行img-url替换，将gitee连接替换为本地连接
            replacestr = "https://gitee.com/leok77/blog-img-leok77/raw/main"
            replacestr += paths_md[index][1].replace(os.path.basename(paths_md[index][1]), '').replace(os.sep, '/')
            gitee_img_to_local(paths_md[index][0], replacestr)
        index += 1
