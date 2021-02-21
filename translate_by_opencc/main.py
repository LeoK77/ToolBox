import translate_by_opencc.translate as translate

if __name__ == '__main__':
    filenames = [
        # Hexo主题Butterfly配置文件简体化
        r'C:\Users\LeoK77\Documents\WorkSpace\Blog-Hexo-LeoK77\node_modules\hexo-theme-butterfly\_config.yml'
    ]
    for filename in filenames:
        translate.tradition_to_simple(filename)
    pass
