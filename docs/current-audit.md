# 仓库审计报告

## 1. 当前文件结构

```
PygameGoBang/
├── README.md
├── LICENSE
├── PygameGoBang/                      # 单机版（根目录命名不规范）
│   ├── Gobang.py                     # 主程序入口（UI + 规则 + 游戏逻辑全混在一起）
│   └── img-folder/
│       ├── window1.png
│       └── window2.png
└── PygameGoBang(LAN)/               # 联机版（独立文件夹）
    ├── Server.py                     # 服务端（UI + 网络 + 规则混在一起）
    └── Client.py                     # 客户端（UI + 网络 + 规则混在一起）
```

**问题**：
- 项目根目录命名 `PygameGoBang/` 与子目录 `PygameGoBang/` 名称相同，易混淆
- 缺少 `src/` 顶层结构
- 缺少 `tests/` 测试目录
- 缺少 `docs/` 文档目录
- 缺少配置文件目录 `configs/`

---

## 2. 当前主入口

| 版本 | 入口文件 | 启动方式 |
|------|----------|----------|
| 单机版 | `PygameGoBang/Gobang.py` | `python Gobang.py` |
| 联机版 | `PygameGoBang(LAN)/Server.py` + `Client.py` | 先 Server 后 Client |

---

## 3. 当前规则逻辑位置

**单机版 `Gobang.py:16-84`**：
- 棋盘状态：`status_list` 字典（0=空，1=白棋，2=黑棋）
- 棋盘大小：15×15（一维映射 `x*15+y`）
- 胜负判定：横/竖/正斜/反对角 四方向连5检测（代码47-84行）
- 轮次控制：`flag` 变量（0白棋走，1黑棋走）

**联机版 `Server.py` / `Client.py`**：
- 规则逻辑与单机版相同
- 数据通过 `---` 分隔符拼接为字符串，通过 socket 传输

---

## 4. 当前 UI 逻辑位置

**单机版 `Gobang.py:28-126`**：
- 绘制棋盘：第32-36行
- 绘制棋子：第39-44行
- 绘制落子光标：第86行
- 显示当前回合文字：第89-93行
- 键盘事件处理：第96-123行
- 刷新：`pygame.display.flip()`

**联机版 `Server.py:107-245`** / `Client.py:93-233`**：
- 逻辑相同，额外增加网络同步绘制

---

## 5. 当前网络逻辑位置

| 文件 | 位置 | 说明 |
|------|------|------|
| `Server.py:6-13` | `__init__` | 绑定IP/端口，监听连接 |
| `Server.py:60-72` | `send_data` | 线程发送数据 |
| `Server.py:74-87` | `recevie_data` | 线程接收数据 |
| `Client.py:6-10` | `__init__` | 连接服务器 |
| `Client.py:44-56` | `send_data` | 线程发送数据 |
| `Client.py:58-72` | `recevie_data` | 线程接收数据 |

---

## 6. 主要耦合问题

### 问题1：UI 与规则强耦合
- `Gobang.py` 中游戏规则判断（胜负检测、落子合法性）直接写在渲染循环中
- 无法在不启动 Pygame 的情况下测试规则

### 问题2：网络与游戏逻辑耦合
- `Server.py` / `Client.py` 中棋盘状态与网络状态混在同一个类中
- 无法单独测试网络协议或单独运行游戏引擎

### 问题3：硬编码问题
- 棋盘大小 `15` 在代码中多处硬编码
- IP 地址 `192.168.1.254` 硬编码
- 窗口尺寸 `350×285` / `400×285` 硬编码
- 网格偏移 `20` 硬编码
- `FPSClock 30` 硬编码

### 问题4：数据传递方式混乱
- 用字符串逆序拼接传输棋盘（`data_` 逆序构建第49行/65行）
- 用 `---` 作为分隔符，无校验机制

### 问题5：无配置体系
- 没有任何配置文件
- 所有参数散布在代码中

---

## 7. 不利于测试的问题

| 问题 | 描述 |
|------|------|
| Pygame 硬依赖 | 游戏逻辑无法在无头环境测试 |
| 全局变量 | `flag`, `movex`, `movey` 等用完即弃 |
| 棋盘用字典 | 应用 `dict` 而非 `list` 或 numpy，效率低 |
| 无单元测试 | 整个项目 0 个测试文件 |
| 胜负判定无 break | 循环在找到五子后继续运行 |

---

## 8. 重构优先级清单

### P0（必须先做）
1. 建立 `src/pygobang/` 目录结构，将核心逻辑与 UI 分离
2. 抽离 `core/board.py`、`core/rules.py`、`core/game.py`、`core/move.py`
3. 建立 `tests/` 目录，补基本单元测试
4. 建立 `pyproject.toml` + `Makefile` + 质量检查工具

### P1（基础能力）
5. 实现 `Bot` 基类 + `RandomBot` + `HeuristicBot`
6. 实现 `replay/` 系统（记录/序列化/回放）
7. 重构 UI 层调用新的核心接口

### P2（进阶 AI）
8. 实现 `MinimaxBot` + Alpha-Beta 剪枝
9. 建立 benchmark 体系

### P3（高级能力）
10. 实现 `AIAdvisor`（教练模式）
11. 实现 `AIReplayAnalyzer`（复盘模式）
12. FastAPI 服务层

---

## 9. 当前不可测试代码列表

```
PygameGoBang/Gobang.py         - 整个文件（行1-128）
PygameGoBang(LAN)/Server.py    - 整个文件（行1-245）
PygameGoBang(LAN)/Client.py    - 整个文件（行1-233）
```

原因：直接依赖 `import pygame` 和 `import socket`，无 mock 路径，无纯 Python 接口层。

---

## 10. 审计结论

现有代码是一个**功能可用但架构原始的单文件脚本集合**。主要问题不是功能缺失，而是**工程化程度极低**：

- 无法测试
- 无法扩展
- 无法自动化检查
- AI 能力为零
- 无配置/日志/错误处理体系

重构路径清晰：先解耦 → 再测试 → 再接 AI → 再扩展。
