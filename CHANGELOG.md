# Club XiangQi Bera (CXB) 系统更新日志与版本记录

本文档详细记录百乐象棋俱乐部（Club XiangQi Bera）系统、管理后台以及学校选拔赛对阵系统的版本迭代、Bug 修复及功能更新历史。

---

## 📅 [2026-10-01] 核心修复与正式多语言体系升级

### 1. 🛡️ 学校对阵编排系统 (`school.html`) 按钮无响应 Bug 彻底修复
- **故障原因根因排查**：
  1. `renderActiveTourney()` 内部存在重复变量声明 `const t = I18N[currentLang] || I18N.zh;`，导致现代浏览器 JavaScript 引擎抛出 `Uncaught SyntaxError: Identifier 't' has already been declared`，导致整个脚本解析中止。
  2. 国际化字典对象 `I18N` 与 `setLoginLang` 函数原先声明在脚本末尾，而在顶部登录验证与渲染逻辑调用时存在暂时性死区（Temporal Dead Zone - TDZ）风险。
- **修复方案**：
  1. 移除 `renderActiveTourney()` 中第 2 处重复的 `const t` 声明。
  2. 将语言包对象 `I18N`、切换函数 `setLoginLang` 与当前语言状态变量提前至 `<script>` 标签最顶部立即初始化。
  3. 清理 `showSchoolApp()` 异常捕获块中的重复 `const` 声明。
  4. 验证输入框在带有 URL 参数 `?pin=CXB-NKZY` 时能够自动填入并直接调用验证，所有按钮点击与回车触发全部恢复正常。

### 2. 🌐 双语系统（中/英）深度完善与品牌规范化
- **消除第三方残留文字**：
  - 全面清理所有 `SP98 Official Swiss-System` 等非本俱乐部旧称。
  - 中文统一规范为：**百乐象棋对阵编排系统**（认证单位：**百乐县象棋公会认证**）。
  - 英文统一规范为：**Club XiangQi Bera Pairing System**（认证单位：**Certified by Persatuan Catur Cina Daerah Bera**）。
- **界面与打印排版 100% 全球化**：
  - 登录页与系统顶部均配备固定的 **中文 / English** 语言切换按钮，切换时按钮居中稳定不移位。
  - 正式比赛打印成绩单与对阵单支持 100% 完整英文报表输出（表头、轮次、台次、对手、得分、累进分对手分及公会认证印鉴）。

### 3. 📁 俱乐部系统目录归档 (`Club XiangQi Bera/03_学员天梯与联赛系统_Web_&_System/`)
- 根据组织架构规范，将最新完整网页系统代码包及高清徽章资源同步归档到俱乐部专属目录：
  - `Club XiangQi Bera/03_学员天梯与联赛系统_Web_&_System/cxb_system_web/`
  - 包含 `admin.html`、`index.html`、`school.html`、`Code.gs`、徽章与图标资产。

---

## 📅 [2026-09-30] 瑞士轮比赛后台与学校对阵端构建

### 1. 🏆 管理后台比赛模块 (`admin.html`)
- 新增瑞士轮锦标赛排程与记分板（支持积分编排、同分破同分规则、避免重复对碰、红黑先后手平衡）。
- 整合 ELO 动态 K-factor 积分结算系统。
- 增加比赛授权激活码生成与 Cloudflare KV 联动。

### 2. 🏫 学校轻量化对阵系统 (`school.html`)
- 专为各中小学校内选拔赛定制，输入俱乐部下发的授权码（PIN）后即可使用。
- 具备现场投影模式（大屏白板显示台次对阵）与 A4 纸张成绩单排版。
- 接入 Cloudflare Workers + KV 实时鉴权体系。

---

## 📅 [2026-09-28] 天梯大榜与对局记录查看 (`index.html`)
- 搭建学员 ELO 动态等级榜与段位勋章体系。
- 增加学员战绩清查、记谱纸图片 Lightbox 弹窗浏览。
- 对接 Google Sheets 数据库，支持云端自动同步。
