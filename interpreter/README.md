# mini-Scheme 解答

实现 Python 3 解释器，入口为 `src/main.py`。只使用 Python 标准库。

```bash
echo "(+ 1 2)" | python src/main.py
python src/main.py file1.scm file2.scm
python src/main.py < program.scm
python autograder.pyz python src/main.py
python -m unittest discover -s tests -v
```

## 模块

| 文件 | 职责 |
| --- | --- |
| values.py | Symbol、Pair、空表、闭包和内置过程 |
| lexer.py | 字符串、转义、注释和词法切分 |
| parser.py | 括号、引用与点对语法 |
| environment.py | 词法作用域与外层环境查询 |
| primitives.py | 规范中的算术、比较、列表、谓词与输出过程 |
| evaluator.py | 特殊形式、求值与过程调用 |
| printer.py | 布尔、字符串、真列表和点对打印 |
| main.py | 多文件共享全局环境与标准输入入口 |

函数调用按应用序求值，`if/cond/and/or/quote` 等特殊形式单独处理。闭包保存定义时的环境。只有 `#f` 为假，Python 的 `True == 1` 不用作 Scheme 相等判据。整数除法向零截断，使用整数绝对值相除避免大整数转换为浮点产生误差。

## 验证

仓库原始评分器 12 组全部 PASS。另加 8 组 unittest，检查真假语义、并行 let 与闭包、大整数除法、点对和类型区分、字符串转义、cond 返回值、多文件共享环境与错误输入。全部通过。正式隐藏用例尚未运行，不能将公开通过写成正式满分。

调试过程中，过早增加了“let 同名绑定必须报错”的限制，导致公开第 010 组失败。原规范没有要求这种限制，因此删除了该额外拒绝逻辑。所有绑定表达式仍在外层环境求值，再统一放入新环境，同名绑定由后项覆盖。

不实现规范明确排除的宏、set!、可变参数 lambda 或尾调用优化保证。错误输入输出可读错误并返回非零状态。

## 来源与工具

根据 [原仓库规范](https://github.com/woo114515/minischeme-starter) 实现。Codex 辅助编写模块、设计补充测试和修复失败用例。上游评分器原样使用，没有读取其隐藏期望输出或修改其内容。

## 评分器位置

官方评分器未放入公开教学仓库。可从原仓库获取，或使用本次程序题源码 ZIP 中的原样副本，再在解释器目录执行评分命令。公开仓库不包含原始纳新题或个人面试材料。
