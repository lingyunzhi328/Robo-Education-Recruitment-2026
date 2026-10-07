# Robo Education Recruitment 2026

ROS 2 入门教学资料与模块化 mini-Scheme 解释器。作者：郑子毅。

## 目录

```text
topic/内训选题.md       三次内训的完整方案
slides/                10 分钟课件源文件、PDF 和逐页讲稿
examples/              ROS 2 圆形运动、点位控制与独立控制数学
tests/                 不依赖 ROS 安装的控制数学测试
docs/troubleshooting.md 排查方法与课前联调清单
interpreter/           mini-Scheme 源码、补充测试与运行说明
```

## 运行教学示例

使用已验证的 Ubuntu 24.04 + ROS 2 Jazzy 环境，每个新终端加载：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

另一个终端进入仓库，运行圆形控制器：

```bash
source /opt/ros/jazzy/setup.bash
python3 examples/circle_node.py
```

八秒后它持续发布零速度。按 Ctrl+C 退出，重新启动或重置 turtlesim，然后运行 `python3 examples/point_node.py`。两个自动控制器不同时运行，也不要同时开键盘控制器。

独立逻辑测试：

```bash
python3 -m unittest discover -s tests -v
```

当前提交的四项控制数学测试均通过，但它们不替代 ROS 节点通信、图形环境和实车安全测试。

## 4.5.3 Git 与 GitHub 使用记录

### 使用了哪些功能

本次通过 GitHub 创建远程仓库，使用 `git clone` 获取本地目录，再用 `git add`、`git commit` 和 `git push` 分步提交。通过 `git status`、`git diff` 与 `git log` 检查内容和提交历史。先提交内训方案与目录说明，再提交课件和示例，解释器作为另一项可复现成果整理。

提交历史中的每次提交都有实际文件变化。主题分支与 Pull Request 是建议的后续维护流程，本次没有把未执行的 PR 过程写成已完成操作。

### 遇到的问题与处理

1. 中文路径与编码：Python 处理本地文件时统一 UTF-8，文件名保持稳定，避免依赖某一位成员的绝对路径。
2. ROS 官方网页反爬：改为读取同版本官方文档仓库源码，保持 Jazzy 的命令和接口一致。
3. 教学环境与当前机器不同：把控制数学独立出来运行单测，在文档中明确真实 ROS 环境的课前验收步骤。
4. 幻灯片导出：声明中文与代码字体，检查源文件结构、表格 editability 和逐页渲染，再导出 PDF。

### 多人如何维护

按课程与资源类型组织目录，主分支保存可复现版本。每个修改创建短主题分支，提交说明写清问题与改法，提出 PR 后至少由另一位成员核对内容。新命令要在统一环境运行，修改示例时同步更新讲义与课件。生成文件与源文件一同更新，不把缓存、密钥、原始私人材料放入仓库。常见故障沉淀到 `docs/`，大版本环境升级单独记录。

### AI 使用与检查

Codex 辅助设计课程、编写示例与解释器、整理文档和生成课件。使用 Firecrawl 核对 ROS 官方资料，按用户要求切换到本地部署服务。检查包括版本与字段核对、源码语法编译、控制数学测试、Scheme 官方验收及独立补充测试、课件渲染与资料结构检查。未在当前 Windows 环境宣称完成真实 ROS 节点或硬件联调。

## 主要参考

- [ROS 2 Jazzy 官方文档](https://docs.ros.org/en/jazzy/)
- [对应版本官方文档源码](https://github.com/ros2/ros2_documentation/tree/jazzy)
- [mini-Scheme 原始规范与评分器](https://github.com/woo114515/minischeme-starter)

课件各页的讲稿和 PowerPoint 备注保留与其内容相关的官方参考链接。
