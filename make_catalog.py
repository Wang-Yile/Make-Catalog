import os
import re
import sys
import time
import difflib
from urllib.parse import quote
from functools import cache

import bs4
import requests

if len(sys.argv) != 3:
    print(f"用法: python3 {sys.argv[0]} <infile> <outfile>")
    exit(1)
infile = os.path.abspath(sys.argv[1])
outfile = os.path.abspath(sys.argv[2])

with open(infile, encoding="utf-8") as file:
    lines = [line.strip() for line in file.read().splitlines() if line.strip() != ""]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}

class OJ():
    @cache
    def get(self, s: str): ...
    def markdown(self, s: str): ...
    def title(self, s: str): ...
    def token(self, s: str): ...
class CodeForces(OJ):
    def __init__(self):
        self._pattern = re.compile("^CF[1-9][0-9]*[A-Z][1-9]*")
    @cache
    def get(self, s):
        pat = self._pattern.match(s)
        if pat is None:
            return None
        pid, title = s[2:pat.endpos], s[pat.endpos:].strip()
        url = f"https://www.luogu.com.cn/problem/CF{pid}"
        if title == "":
            resp = requests.get(url, headers=headers)
            if resp.ok:
                soup = bs4.BeautifulSoup(resp.text, "lxml")
                title = soup.find("title").text.removeprefix(f"CF{pid} ").removesuffix(" - 洛谷")
        return pid, title, url
    def markdown(self, s):
        ret = self.get(s)
        if ret is None:
            return None
        pid, title, url = ret
        return f"- [CodeForces {pid} {title}]({url})"
    def title(self, s):
        return self.get(s)[1]
    def token(self, s):
        return f"CF{self.get(s)[0]}"
class CodeForcesGym(OJ):
    def __init__(self):
        self._pattern = re.compile("^GYM[1-9][0-9]*[A-Z]")
    @cache
    def get(self, s):
        pat = self._pattern.match(s)
        if pat is None:
            return None
        pid = s[3:pat.endpos]
        contest, count = pid[:6], pid[6:]
        url = f"https://codeforces.com/gym/{contest}/problem/{count}"
        return pid, url
    def markdown(self, s):
        ret = self.get(s)
        if ret is None:
            return None
        pid, url = ret
        return f"- [CodeForces {pid}]({url})"
class UOJLike(OJ):
    def __init__(self, url = "uoj.ac", preffix: str = "UOJ", suffix: str = " - 题目 - Universal Online Judge"):
        self._url = url
        self._preffix = preffix
        self._suffix = suffix
        self._pattern = re.compile(f"^{preffix}[1-9][0-9]*")
    @cache
    def get(self, s):
        pat = self._pattern.match(s)
        if pat is None:
            return None
        pid, title = s[:pat.endpos].removeprefix(self._preffix), s[pat.endpos:].strip()
        url = f"https://{self._url}/problem/{pid}"
        if title == "":
            resp = requests.get(url, headers=headers)
            if resp.ok:
                soup = bs4.BeautifulSoup(resp.text, "lxml")
                title = soup.find("title").text.removesuffix(self._suffix)
        return pid, title, url
    def markdown(self, s):
        ret = self.get(s)
        if ret is None:
            return None
        pid, title, url = ret
        return f"- [{self._preffix}{pid} {title}]({url})"
    def title(self, s):
        return self.get(s)[1]

oj = {
    "CodeForces": CodeForces(),
    "GYM": CodeForcesGym(),
    "UOJ": UOJLike(),
    "QOJ": UOJLike("qoj.ac", "QOJ", " - Problem - QOJ.ac"),
}
ret = []
token = []
for prob in lines:
    print(f"{prob}:")
    for name in oj:
        host: OJ = oj[name]
        md = host.markdown(prob)
        if md is not None:
            print(f"    \033[32;1mmatch\033[0m \033[;4m{name}\033[0m", end=" ")
            ret.append(md)
            tok = host.token(prob)
            if tok is not None:
                print(f"\033[34;1mfound\033[0m {host.title(prob)} ({host.token(prob)})")
                token.append(tok)
            else:
                print(f"\033[34;1mfound\033[0m {host.title(prob)}")
            break
    else:
        print("    \033[31;1mmismatch\033[0m", end=" ", flush=True)
        url = f"https://www.luogu.com.cn/problem/list?keyword={quote(prob)}&type=AT%7CB%7CCF%7CP%7CSP%7CUVA"
        resp = requests.get(url, headers=headers)
        if not resp.ok:
            print("\033[33;1mignored\033[0m")
            ret.append(f"- {prob}")
            continue
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        lis = soup.find("div", {"class": "lg-container"}).find_all("li")
        lst = []
        for li in lis:
            pid = li.text.split(chr(160))[0]
            title = li.text.removeprefix(pid).strip()
            seq = difflib.SequenceMatcher(None, prob, title)
            ratio = (2 * seq.ratio() + seq.quick_ratio()) / 3
            lst.append((ratio, pid, title))
        if len(lst) == 0:
            print("\033[33;1mignored\033[0m")
            ret.append(f"- {prob}")
            continue
        lst.sort(key=lambda x: x[0], reverse=True)
        ratio, pid, title = lst[0]
        print(f"\033[34;1mfound\033[0m {title} ({pid})", end=" ")
        if ratio < 0.5:
            print(f"[ratio=\033[33;1m{ratio*100:.2f}\033[0m%] \033[33;1mignored\033[0m")
            ret.append(f"- {prob}")
            continue
        print(f"[ratio={ratio*100:.2f}%]")
        url = f"https://www.luogu.com.cn/problem/{pid}"
        if pid.startswith("P") or pid.startswith("B"):
            ret.append(f"- [Luogu {pid} {title}]({url})")
            token.append(pid)
        else:
            ret.append(f"- [{pid} {title}]({url})")
            token.append(pid)

with open(outfile, "w", encoding="utf-8") as file:
    file.write("\n".join(ret))
    tm = time.localtime()
    file.write(f"\n\n**本目录由 Make Catalog 自动生成，不提供任何担保。输入数据提供者和网站所有者对生成内容分别拥有可能产生的一切权利。  \n数据收集日期：{tm.tm_year}-{tm.tm_mon:02d}-{tm.tm_mday:02d}**")
print("\033[35;1mfinal\033[0m:", ",".join(token))