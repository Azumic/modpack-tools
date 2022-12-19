import os
from os import path
import hashlib
from filediff.diff import file_diff_compare


blacklist = ['openloader', 'fancymenu', 'MusicTriggers']


def compare_file(original, modpacks):
    try:
        with open(original, 'rb') as of:
            content = of.read()
            o1 = hashlib.md5(content).hexdigest()
    except OSError as reason:
        print('文件出错了T_T')
        print('出错原因是' + str(reason))
        return False

    with open(modpacks, 'rb') as mf:
        content = mf.read()
        m1 = hashlib.md5(content).hexdigest()
    return not o1 == m1


# 创建多级文件（不含文件）
def create_dir(file_path):
    if path.exists(file_path) is False:
        os.makedirs(file_path)


def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        is_bl = False
        real_url = path.join(url, f)
        if path.isfile(real_url):
            for bl in blacklist:
                if bl in real_url:
                    is_bl = True
                    break

            if is_bl:
                continue

            dirname = path.dirname(real_url)
            basename = path.basename(real_url)

            ori_file = real_url.replace('modpacks', 'original')
            if compare_file(ori_file, real_url) is True:
                outputdir = dirname.replace('modpacks', 'diff')
                create_dir(outputdir)
                file_diff_compare(ori_file, real_url, outputdir + '/' + basename.split('.')[0] + '.html', show_all=True)

        elif path.isdir(real_url):
            scaner_file(real_url)
        else:
            print("其他情况")
            pass


scaner_file('./modpacks/')