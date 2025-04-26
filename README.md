# Make Catalog

本程序为信息学竞赛中可能使用的一些来自在线评测平台的题目建立 Markdown 格式的目录。

本程序模拟正常收集整理题目的方式整理数据，单次运行的网络请求次数和频率在合理范围内。

**请不要密集使用本程序，以免给目标网站服务器带来较大负担。作者不对使用本程序产生的任何后果负责。**

**输入数据提供者和网站所有者对生成内容分别拥有可能产生的一切权利。**

本程序在 [GNU 通用公共许可证，版本 3 或更高](https://www.gnu.org/licenses) 下许可，作者 [Wang Yile](https://github.com/Wang-Yile)。

## 环境要求

使用本程序需要自行配置 Python 环境，要求如下：

- Python 3.9 以上
- 第三方库 requests、beautifulsoup4、lxml

本程序在如下环境中已被验证正常运行：

- Windows 11 24H2 (10.0.26100.3775)
- Python 3.13.0 64-bit
- requests 版本 2.32.3
- beautifulsoup4 版本 4.13.4
- lxml 版本 5.4.0

## 使用方法

```
# Windows
py make_catalog.py <infile> <outfile>
# Unix
python3 make_catalog.py <infile> <outfile>
```

其中 `<infile>` 是输入文件的路径，`<outfile>` 是程序写入结果的路径。所有文件都在 `utf-8` 格式下读写，换行方式取决于运行环境。

## 输入格式

输入文件包含若干行，空行将被忽略，其余每一行视为对一道题目的描述。

对于每道题目，可以使用两种方式描述：在线评测平台标识符，或者纯文本。

### 标识符

支持 [CodeForces](https://codeforces.com)、[UOJ](https://uoj.ac) 和基于 [UOJ 开源项目](https://github.com/vfleaking/uoj) 的 UOJ-Like 网站（目前可以通过标识符识别 [QOJ](https://qoj.ac)）。

不完全支持 [CodeForces Gym](https://codeforces.com/gyms)。

| 网站 | 标识符 | 格式 | 示例 |
|:-:|:-:|:-:|:-:|
| [CodeForces](https://codeforces.com) | `CF` | `CF` + 比赛编号 + 题目编号 | [`CF1A`](https://codeforces.com/contest/1/problem/A) |
| [UOJ](https://uoj.ac) | `UOJ` | `UOJ` + 题目编号 | [`UOJ1`](https://uoj.ac/problem/1) |
| [QOJ](https://qoj.ac) | `QOJ` | `QOJ` + 题目编号 | [`QOJ1`](https://qoj.ac/problem/1) |
| [CodeForces Gym](https://codeforces.com/gyms) | `GYM` | `GYM` + 比赛编号 + 题目编号 | [`GYM100001A`](https://codeforces.com/gym/100001/problem/A) |

**大小写敏感。**

### 纯文本

如果描述没有被识别为有效标识符，则认为其为纯文本。

该描述将被传递给 [洛谷题库](https://www.luogu.com.cn/problem/list) 进行搜索，并通过一定计算规则取最高匹配度的结果。如果任何一项结果匹配度都小于 50%，或者搜索没有返回结果，或者搜索失败，则不生成结果。

除非程序发生异常，不生成结果的题目按原样输出。

## 注意事项

爬取使用请求头仅包含 `User-Agent` 字段，值为

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0
```

由于效率问题，来自 CodeForces 网站的题目信息将从洛谷网爬取。

## 许可证

本程序在 [GNU 通用公共许可证，版本 3 或更高](https://www.gnu.org/licenses) 下许可，作者 [Wang Yile](https://github.com/Wang-Yile)。

```
Make Catalog
Copyright (C) 2025  Wang Yile

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
