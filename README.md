# 系统建模与方法核心版

本版只保留系统模型、两阶段部署方法和验证它们的小型测试。**不包含论文数据、结果图、实验结果文件、批量实验或绘图模块。** 所有节点、服务、任务 DAG、流量与无线参数均由调用方提供。

原始 `CODE/` 及先前的 `CODE_ICC2026_ZJ/` 保留不动；后续以本目录作为核心代码入口。

## 阅读顺序

| 文件 | 职责 |
|---|---|
| [models.py](edge_msd/models.py) | 服务、任务 DAG、节点、用户、请求、实例和决策的数据结构与约束 |
| [config.py](edge_msd/config.py) | 方法控制参数，不构建论文场景 |
| [network.py](edge_msd/network.py) | 上行、多跳传输、DAG 输入就绪时间 |
| [capacity.py](edge_msd/capacity.py) | Gamma 有效容量解析式及显式负载代理下的时延映射 |
| [placement.py](edge_msd/placement.py) | 核心服务 QoS 评分、资源受限整数规划、部署多样性 |
| [controller.py](edge_msd/controller.py) | 轻量服务部署、路由、并行准入和虚拟队列；含 Proposed / PropAvg / LBRR / GA |
| [simulation.py](edge_msd/simulation.py) | 执行上述模型的时钟与状态转移；只返回内存中的诊断信息，不写文件 |

公式、单位、约束和方法适用边界集中在 [系统模型与方法说明](docs/MODEL_AND_METHOD.md)。建议先读该说明，再从 `Simulator.run()` 顺着调用关系阅读。

## 运行与检查

在本目录创建独立环境，避免与旧版同名的 `edge_msd` 导入包混用：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m examples.minimal
python -m pytest -q
```

Windows 使用 `.venv\Scripts\activate`。核心依赖仅 NumPy、SciPy、NetworkX；整数规划使用 SciPy 内置的 HiGHS，无需外部求解器路径。

[minimal.py](examples/minimal.py) 是“两个节点、两个服务、一个请求”的人工示例，只用于展示 API 和检查状态转移，并非论文参数。测试中的数值也仅用于手工核对单位、边界和约束。代码没有自动加载任何数据文件。

构建自己的 `Scenario` 后，调用方式为：

```python
from edge_msd.config import Settings
from edge_msd.simulation import Simulator

# scenario 由你用 Service / TaskType / Node / User / Scenario 构造。
# W_ms 需由你的负载模型明确指定，不能把队列长度直接当成到达率。
settings = Settings(ec_admission_window_ms=W_ms, wireless=False)
simulator = Simulator(scenario, settings, method="proposed")
diagnostics = simulator.run()
```

如果只检查单个方法，可直接调用 `place_core(scenario, network, settings)` 或 `Controller.step(...)`，不必运行执行引擎。

## 此次重点修正

- 有效容量的准入窗口必须显式指定；没有把并行数到负载的换算藏在默认论文数据中。
- 根阶段默认按任务输入大小转发，避免默认值为零时漏算有线传输。
- 路由包含实例槽位；评估与执行使用同一分配，不只给出节点后再次选择实例。
- 后续路由改变共享实例负载时，重新计算较早分配阶段的时延评分；计入实例中尚未到齐的数据。
- 核心部署支持 `Node.light_reserve`，显式给在线轻量部署保留资源；所有方法遵守相同资源规则。
- 校验忙实例保留、并行准入、控制时间递增、无效路由和场景引用。

这里的“正确”指模型定义、单位、约束、状态转移和已声明的方法实现一致。有效容量到有限 DAG 的端到端概率保证、在线贪心的全局最优性，并没有因此获得证明；这些边界在方法说明中明确区分。
