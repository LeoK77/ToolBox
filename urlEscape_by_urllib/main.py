import urlEscape_by_urllib.urlEscape as urlEscape
import path_analysis.path_analysis as path_analysis
import os

if __name__ == '__main__':
    root_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/_posts'
    root_paths = path_analysis.get_all_path(root_path)
    for path in root_paths:
        basename, ext = os.path.splitext(path)
        if ext == '.md':
            urlEscape.url_escape_to_chinese(path)
