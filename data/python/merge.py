import os
import subprocess

os.chdir('tmp')

print('处理规则')
subprocess.run("cat *.txt | sort -n | grep -v -E '^((#.*)|(\s*))$' | grep -v -E '^[0-9f\.:]+\s+(ip6\-)|(localhost|local|loopback)$' | grep -Ev 'local.*\.local.*$' | sed 's/127.0.0.1/0.0.0.0/g' | sed 's/::/0.0.0.0/g' | grep '0.0.0.0' | grep -Ev '.0.0.0.0 ' | sort | uniq > base-src-hosts.txt", shell=True)
subprocess.run("wait", shell=True)
subprocess.run("cat base-src-hosts.txt | grep -Ev '#|\$|@|!|/|\\|\*' | grep -v -E '^((#.*)|(\s*))$' | grep -v -E '^[0-9f\.:]+\s+(ip6\-)|(localhost|loopback)$' | sed 's/127.0.0.1 //' | sed 's/0.0.0.0 //' | sed 's/^/||&/g' | sed 's/$/&^/g' | sed '/^$/d' | grep -v '^#' | sort -n | uniq | awk '!a[$0]++' | grep -E '^((\|\|)\S+\^)'", shell=True)
print('合并规则')
subprocess.run("cat rules*.txt | grep -Ev '^((\!)|(\[)).*' | sort -n | uniq | awk '!a[$0]++' > tmp-rules.txt", shell=True)
subprocess.run("cat | grep -E '^[(\@\@)|(\|\|)][^\/\^]+\^$' | grep -Ev '([0-9]{1,3}.){3}[0-9]{1,3}' | sort | uniq > ll.txt", shell=True)
subprocess.run("cat *.txt | grep '^@' | sort -n | uniq > tmp-allow.txt", shell=True)
subprocess.run("wait", shell=True)

subprocess.run("cp tmp-allow.txt .././allow.txt", shell=True)
subprocess.run("cp tmp-rules.txt .././rules.txt", shell=True)
print('合并完成')


# 去重开始
print("规则去重中")
os.chdir(".././")  # 将当前目录更改为.././目录下
files = os.listdir()  # 得到文件夹下的所有文件名称
result = []
for file in files:  # 遍历文件夹
    if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
        if os.path.splitext(file)[1] == '.txt':
            # print('开始去重'+(file))
            f = open(file, encoding="utf8")  # 打开文件
            result = list(set(f.readlines()))
            result.sort()
            fo = open('test' + (file), "w", encoding="utf8")
            fo.writelines(result)
            f.close()
            fo.close()
            os.remove(file)
            os.rename('test' + (file), (file))
            # print((file) + '去重完成')

# 处理完毕
print("规则去重完成")