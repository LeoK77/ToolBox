import urlEscape_by_urllib.urlEscape as urlEscape
import os

if __name__ == '__main__':
    root_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/_posts'
    root_paths = []
    urlEscape.get_all_path(root_path, root_paths)
    for path in root_paths:
        basename, ext = os.path.splitext(path)
        if ext == '.md':
            urlEscape.url_escape_to_chinese(path)
