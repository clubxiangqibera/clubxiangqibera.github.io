# Club XiangQi Bera (CXB) 象棋赛事与学员天梯管理系统

**百乐象棋俱乐部（Club XiangQi Bera）** 官方青少年天梯积分排位系统、总控管理后台与校内选拔赛对阵系统。

---

## 🌐 线上系统访问入口 (Official Live Links)

| 页面名称 | 访问地址 | 用途说明 |
| :--- | :--- | :--- |
| **🏆 学员天梯公榜** | [clubxiangqibera.github.io](https://clubxiangqibera.github.io/) | 手机/电脑自适应天梯排行榜、学员战绩与记谱纸查阅 |
| **⚙️ 俱乐部总控后台** | [clubxiangqibera.github.io/admin.html](https://clubxiangqibera.github.io/admin.html) | 学员档案管理、学费审核、锦标赛组织、授权码分发 |
| **🏫 校园比赛对阵系统** | [clubxiangqibera.github.io/school.html](https://clubxiangqibera.github.io/school.html) | 中小学内部选拔赛、一键瑞士轮编排、大屏投影与正规打印 |

---

## 🔑 核心权限与访问秘钥 (Access Credentials)

* **👑 总控超级管理员 PIN**：`7789`
  * 拥有完整控制权限：学员建档、学费审核、排位编排、生成并管理各校比赛授权码。
* **🎓 教练员快速通道 PIN**：`6666`
  * 可组织比赛、录入对局、查看天梯与成绩单。
* **♟️ 学员/家长默认查询密码**：`级别数字 + 编号数字`（例如 Lv2 学员 XQB-002 默认密码为 `2002`）。
* **🛡️ 学校比赛授权码**：由总控后台生成，例如 `CXB-NKZY`，也可直接通过链接访问：`https://clubxiangqibera.github.io/school.html?pin=CXB-NKZY`。

---

## 📁 代码库与文件架构说明

### 1. 网页前端系统 (`web_deploy_org/` / `web_v2/` / `Club XiangQi Bera/...`)
- **`index.html`**：学员天梯排行榜前台（纯原生 HTML5/CSS3/ES6，无重度外部依赖）。
- **`admin.html`**：俱乐部全功能赛事与学员管理后台（含瑞士轮编排算法、ELO 结算、学费与授权码管理）。
- **`school.html`**：学校独立选拔赛系统（支持一键中/英双语切换、现场投影白板、A4 标准双语成绩单与对阵表打印）。
- **`cxb_round_emblem.png`** / **`cxb_logo_clean.png`**：俱乐部官方高清矢量与透明会徽。

### 2. 竞赛对阵核心规则 (Swiss Pairing Engine)
- 严谨实现瑞士制同分编排规则，高分对碰，低分对碰。
- 自动避开同轮或跨轮已遇对手。
- 优先平衡红黑先后手棋色交替。
- 轮空选手（Bye）自动获得 1 分，并在后续轮次优先保障正式对局。

### 3. 云端接口与无服务器架构 (Backend Infrastructure)
- **Google Apps Script (`Code.gs`)**：直连 Google 电子表格，充当学员主数据库与对局数据仓。
- **Cloudflare Workers (`worker_v2.js`)**：提供低延迟 API 网关与 KV 授权校验，支持授权码一键生成、核销与有效期锁定。

---

## 📝 详细更新日志 (Changelog)
查阅详细历史修复与版本迭代请参见：[CHANGELOG.md](CHANGELOG.md)。
