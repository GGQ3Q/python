# python
jupyter画面看起来没有md舒服啊，还是想用md,
# 基础
## 变量
命名dont do that：空格 中文 数字开头 关键词
虚数部分字符：j
```python
z = 3 + 1j#1不能忽略！

print(z)          # 输出: (3+4j)
print(f"结果是: {z}") # 使用 f-string 输出: 结果是: (3+4j)
print(z.real,z.imag) #提取复数的实部和虚部。返回的结果都是浮点数

x = 10
y = 20
z = complex(x, y)
print(z)  # 输出: (10+20j)
```
## 运算
a**b 表示a的b次方
## 比价运算符
print(x==y)这种比较的可直接写在括号里表示输出ture 或者false
比较运算符可以用于不同类型的值，例如数字、字符串等
## 循环语句
if条件不用括号
注意缩进
while循环的条件始终为True，则会导致无限循环

```python
for 变量 in 序列:
    执行的代码块 #遍历序列
    
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
    
for i in range(1, 6):#range为内置函数。表示1~6
    print(i)
```
## 函数
```python
#默认参数
def greet(name, message):#def是定义函数前要写的东西，同时要注意用冒号
    print(f"Hello, {name}! {message}")

greet("Alice", "How are you?")

#可变参数
def calculate_total(*args):
    total = sum(args)
    print(f"The total is {total}")

calculate_total(1, 2, 3, 4, 5)

#关键字参数
def display_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

display_info(name="Alice", age=25, city="New York")
#在这个例子中，display_info函数接收了三个关键字参数，并将它们以键值对的形式打印出来。
```
## 返回值
可返回多个值
## 模块
用import引入库or另外一个文件

from…import语句：
除了导入整个模块，还可以选择性地导入模块中的特定内容

在导入模块时，可以使用as关键字为模块指定别名
```python
import module_name as alias
from module_name import function_name as alias
```
## 列表[]

```python

numbers = [1, 2, 3, 4, 5]#创建列表
fruits = ['apple', 'banana', 'orange', 'grape']

print(numbers[0])  # 输出：1
print(fruits[2])   # 输出：orange

fruits.append('pear')   # 添加'pear'到fruits列表末尾
numbers.insert(2, 6)    # 在numbers列表的第三个位置插入6
fruits.remove('banana')  # 删除fruits列表中的'banana'
```
## 列表plus
```python
#切片
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
subset = numbers[2:7:2]  # 从索引2开始到索引7结束，步长为2,即跨几个数字选取
print(subset)  # 输出：[2, 4, 6]

#列表解析
squares = [x**2 for x in range(1, 11)]
print(squares)  # 输出：[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

#列表方法
#Python提供了丰富的列表方法，用于对列表进行增删改查等操作。常用的列表方法包括append()、extend()、insert()、remove()、pop()等

a = [1, 2]
a.append([3, 4])  # 结果：[1, 2, [3, 4]] （把列表当成一个整体放入,不管是列表还是单个数字）
a.extend([5, 6])  # 结果：[1, 2, [3, 4], 5, 6] （把元素拆开放入）
a.insert(0, 0)    # 结果：[0, 1, 2, [3, 4], 5, 6] （在开头插队）

b = ['apple', 'banana', 'apple', 'cherry']
b.remove('apple') # 结果：['banana', 'apple', 'cherry'] （只删第一个）

last_one = b.pop() # 结果：b 变为 ['banana', 'apple']，last_one 是 'cherry'
first_one = b.pop(0) # 结果：b 变为 ['apple']，first_one 是 'banana'
```
## 元组（）
不可以变,有序
```python
# 创建元组
t = (1, 2, 3, 4, 5)

# 访问元组元素
print(t[0])  # 输出：1

# 尝试修改元组元素（会报错）
t[0] = 10  # TypeError: 'tuple' object does not support item assignment
```
## 集合{}
集合（Set）是 Python 中的一种无序、不重复的数据类型。在集合中，每个元素都是唯一的，不存在重复的元素。集合的特点包括：

无序性：集合中的元素是无序的，无法通过索引来访问或修改元素。
唯一性：集合中的元素是唯一的，不允许存在重复的元素。
可变性：集合中的元素是可变的，可以通过添加或删除元素来修改集合。
不支持索引ing：由于集合是无序的，因此不支持通过索引ing来访问集合中的元
```python
# 创建一个集合
my_set = {1, 2, 3, 4, 5, 3, 2}
print(my_set)  # 输出结果为{1, 2, 3, 4, 5}，去除了重复的元素

# 添加元素
my_set.add(6)
print(my_set)  # 输出结果为{1, 2, 3, 4, 5, 6}

# 删除元素
my_set.remove(3)
print(my_set)  # 输出结果为{1, 2, 4, 5, 6}
```
## 类
不需要定义数据成员
```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} is barking!")
#创建字典对象
#字典是Python中的一种键值对集合，可以使用花括号来创建字典对象        
dict1 = {'name': 'Alice', 'age': 25}
dict2 = {'apple': 3, 'banana': 6, 'orange': 4}

#继承和多态的最简单例子
class Payment:
    def __init__(self,amount):
        self.amount=amount
    def __pay__(self):
        pass
class Wechat(Payment):
    def __pay__(self):
        print(f"微信收款{self.amount}元")
class Zhifubao(Payment):
    def __pay__(self):
        print(f"支付宝收款{self.amount}元")      

pay1 = Wechat(100)
pay1.__pay__()  # 输出: 微信收款 100 元

pay2 = Zhifubao(200)
pay2.__pay__()
```
## 读取文件内容
### 打开关闭文件
要打开一个文件，我们使用内置的open()函数。open()函数接受文件名和打开模式作为参数，并返回一个文件对象。
```python
file = open('example.txt', 'r')
#在这个例子中，我们打开了一个名为example.txt的文件，并指定了打开模式为'r'，表示只读。除了只读模式，open()函数还支持写入（'w'）、追加（'a'）等模式。如果文件不存在，使用写入或追加模式会创建一个新文件。

file.close()
#关闭文件
```
### 读写文件内容
 我们可以使用open()函数以及read()或者readline()方法来实现。
 ```python
 with open('file.txt', 'r') as file:#"r"只读模式
    content = file.read()#实际应用中，我们还可以使用readline()方法逐行读取文件内容
    print(content)
```
### 写入文件内容
```python
with open('file.txt', 'w') as file:
    file.write('Hello, world!')
```
### 关闭文件
在完成文件操作后，我们应当及时关闭文件，以释放系统资源。使用with语句可以帮助我们自动关闭文件，但在一些特殊情况下，我们也可以使用close()方法来手动关闭文件。

## 文件和目录的管理
### 目录的创建与删除
```python
import os
os.mkdir('exmaple_dir')
os.rmdir('new_dir')
```
### 目录的遍历
os模块中的listdir()方法可以列出目录中的文件和子目录
```python
files=os.listdir('example_dir')
for file in files
	print(file)
```
### 文件路径的重命名与复制
```python
import os
import shutil

# 重命名文件
os.rename('old_file.txt', 'new_file.txt')

# 复制文件
shutil.copy('source_file.txt', 'target_file.txt')
```
### 获取文件信息

```python
import os
file_size=os.path.getsize('file.txt')
create_time=os.path.geictime('同上')
modify_time=os.path.getmtime('同上')









```

```