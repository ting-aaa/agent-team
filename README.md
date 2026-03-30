AgentTeams - 多Agent研发团队系统

自我进化的虚拟研发团队模拟系统，具备严格流程执行、从0创建能力、知识积累和团队进化。

## 核心特性

### 1. 严格流程执行
- 工作流状态机强制执行项目流程
- 制作人→策划→程序→美术→运维的完整工作链
- 每个步骤必须由对应角色完成，不允许跳过

### 2. 从0创建能力
- **Skill创建**：定义和管理团队技能
- **工具编写**：创建和集成开发工具
- **环境搭建**：配置开发和部署环境
- **服务搭建**：定义和部署服务
- **Agent招募**：动态创建新的团队成员

### 3. 知识积累
- **技术文档库**：学习资料、技术方案、API文档
- **项目文档库**：项目设计、架构、需求文档
- **经验库**：项目经验、最佳实践、问题解决方案
- **自动更新**：日报自动更新知识库

### 4. 团队进化
- **能力库管理**：追踪每个Agent的技能和经验
- **成长记录**：记录里程碑和成长历史
- **团队报告**：生成团队和个人成长报告

## 项目结构

```
agent-teams/
├── agents/              # Agent角色定义
├── engine/              # 工作流和决策引擎
├── storage/             # 数据存储层
├── knowledge/           # 知识库系统
├── projects/            # 项目管理
├── reports/             # 日报和成长追踪
├── capabilities/        # 能力扩展系统
├── cli.py              # 命令行界面
└── config.py           # 配置文件
```

## 快速开始

### 初始化团队
```bash
uv run python init_team.py
```

### 创建项目
```bash
uv run python cli.py project create MyProject "Project description"
```

### 执行工作流
```bash
uv run python cli.py workflow MyProject producer blueprint
uv run python cli.py workflow MyProject designer design
uv run python cli.py workflow MyProject producer design_review
```

### 生成日报
```bash
uv run python cli.py report programmer \
  --tasks "Task1,Task2" \
  --issues "Issue1" \
  --plan "Tomorrow plan" \
  --knowledge "New knowledge"
```

### 创建Skill
```bash
uv run python cli.py skill create "SkillName" "Description" "category" "implementation" "created_by"
```

### 招募Agent
```bash
uv run python cli.py agent recruit "AgentName" "programmer" \
  --skills "Skill1,Skill2" \
  --description "Description"
```

### 查看团队状态
```bash
uv run python cli.py agent team
```

### 生成成长报告
```bash
uv run python cli.py growth Programmer
```

## 工作流程

```
制作人(提出蓝图)
  ↓
策划(生成方案设计)
  ↓
制作人(审查方案)
  ↓
策划(会议宣讲)
  ↓
策划(调整方案)
  ↓
制作人(确定方案)
  ↓
程序(分析需求)
  ↓
程序(环境搭建/工具编写/Git/Jenkins/看板)
  ↓
程序(开发功能)
  ↓
美术(制作资源)
  ↓
运维(部署/发布)
```

## 团队规范

- **学习规范**：技术文档必须保存到知识库
- **文档规范**：项目文档必须编写
- **经验规范**：每周总结项目经验
- **日报规范**：每日必须提交日报

## 数据存储

所有数据以JSON/YAML格式存储在`data/`目录：

```
data/
├── team/                # Agent配置和招募记录
├── projects/            # 项目数据
├── knowledge/           # 知识库文档
├── reports/             # 日报和成长记录
└── capabilities/        # Skill、工具、环境、服务配置
```

## 测试

运行各阶段测试：

```bash
uv run python test_phase2.py  # 工作流和规范
uv run python test_phase3.py  # 日报和知识积累
uv run python test_phase4.py  # 能力扩展系统
```

## 技术栈

- **Python 3.10+**
- **Anthropic Claude API**：AI决策和分析
- **uv**：项目管理和依赖管理
- **JSON/YAML**：数据存储

## 核心模块

### Agent角色
- Producer（制作人）：提出蓝图、审查、确定方案
- Designer（策划）：方案设计、宣讲、调整
- Programmer（程序员）：需求分析、环境搭建、开发
- Artist（美术）：资源制作
- DevOps（运维）：部署发布

### 工作流引擎
- 状态机管理工作流转移
- 强制执行流程顺序
- 支持任务分解和迭代

### 决策引擎
- 集成Claude API进行需求分析
- 生成设计方案
- 审查和优化

### 知识库系统
- 自动更新知识库
- 追踪Agent能力
- 记录成长历史

## 使用示例

### 完整项目流程

```bash
# 1. 创建项目
uv run python cli.py project create WebApp "Web application project"

# 2. 制作人提出蓝图
uv run python cli.py workflow WebApp producer blueprint

# 3. 策划生成方案
uv run python cli.py workflow WebApp designer design

# 4. 制作人审查
uv run python cli.py workflow WebApp producer design_review

# 5. 策划宣讲
uv run python cli.py workflow WebApp designer presentation

# 6. 策划调整
uv run python cli.py workflow WebApp designer design_adjust

# 7. 制作人确定
uv run python cli.py workflow WebApp producer design_confirm

# 8. 程序分析需求
uv run python cli.py workflow WebApp programmer requirement_analysis

# 9. 程序环境搭建
uv run python cli.py workflow WebApp programmer environment_setup

# 10. 程序开发
uv run python cli.py workflow WebApp programmer development

# 11. 美术制作资源
uv run python cli.py workflow WebApp artist resource_creation

# 12. 运维部署
uv run python cli.py workflow WebApp devops deployment

# 13. 生成日报
uv run python cli.py report programmer --tasks "Completed development" --knowledge "New patterns"

# 14. 查看成长报告
uv run python cli.py growth Programmer
```

## 许可证

MIT
