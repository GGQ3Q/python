# 对于git
## 一些我老是忘记的名词：
 分布式版本控制系统：指的就是读取 存储 修改文档的一个管理器，git就是一个。
 版本库：就是仓库，git可以管理里面所有的文件（注意是./git所在的文件夹！不是./git内部！）
## 我第一次操作遇到的问题
 把文本（txt/md）放到./git内部了，这时候会显示错误，要放在版本库里
 文件名包含空格或特殊字符，可能需要用引号括起来，或者使用转义。如文件名是studynote.md就不用双引号，如果是中文或空格需要双引号。
 目录名称最好用英文
## 要注意的一些点
 >windows系统如果想在git库里面放文字文件（txt啥的）不能用自带记事本，同时不能用微软的文件。用vscode，提交时记得改后缀(后期：但是一般用md吧，至于为啥改后缀我不记得了...)

 添加某个文件时，该文件必须在当前目录下存在，用ls或者dir命令查看当前目录的文件，看看文件是否存在，或者是否写错了文件名。
 git add可以一次多加几个文件，commit一次性提交
## 一些基础指令
```git
 $git add 文件名
 $git add . #添加所有##注意add与. 有个空格
 $git commit -m message #文件提交注释
 $git log #近到远的更改版本
 $git diff #查看更改
 $git log --pretty=oneline #切换文件格式（含commit id）
 $git reset --hard commit id or HEAD^.... #更改版本
 $git relog #历史操作
 $git init #初始化仓库
 $git branch -m master #更改分支
 $git push -m origin master #第一次push
 $git remote rm <name>
 $ git remote add origin github上的SSH地址

```
## 合并分支：（对于不小心搞得两个重复的本地连接同一个库和分支混乱）
1.pullrequest，new一个，这里保证合并的分支文件和进度一致。 如果呈现“没有区别”可能是方向错了，点一下箭头，或者检查一下文件状态有没有忘记push
2.merge 起名
3.check目标本地分支 pull
#保证远程与本地文件一致
4.强制把本地库与目标远程分支连接
5.  删除远程与本地分支
>感觉自己这次的情况比较特殊，合并大致思路是这样，详情还是得问问gemini什么的
