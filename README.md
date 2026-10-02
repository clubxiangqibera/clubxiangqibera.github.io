# 🏛️ Club XiangQi Bera (CXB) — 百乐县中国象棋公会管理系统

> **全栈单人开发** · Nicholas Wong · 2026  
> **技术栈**: Vanilla HTML/CSS/JS + Google Apps Script + Cloudflare Workers + KV + Google Drive

---

## 📋 目录 (Table of Contents)

- [系统概览](#-系统概览)
- [架构图](#-架构图)
- [文件清单](#-文件清单)
- [功能总览](#-功能总览)
- [数据模型](#-数据模型)
- [API 接口清单](#-api-接口清单)
- [部署指南](#-部署指南)
- [已知问题与改进计划](#-已知问题与改进计划)

---

## 🌐 系统概览

CXB 系统是为马来西亚百乐县中国象棋公会 (Persatuan Catur Cina Daerah Bera) 开发的一站式数字化管理平台，服务于教练、学员和家长三方用户。

### 三大用户角色

| 角色 | 入口 | 说明 |
|------|------|------|
| 🧑‍🎓 **学员 / 家长** | `index.html` | 查看天梯排名、个人战绩、缴费、上传棋谱 |
| 🧑‍🏫 **教练 (Coach)** | `admin.html` | 录入对局、管理学员、审核学费 (受权限控制) |
| 👑 **总管理员 (SuperAdmin)** | `admin.html` | 全部功能 + 账号管理 + 相册管理 + 学校授权 |

### 外部服务依赖

| 服务 | 用途 |
|------|------|
| **Google Sheets** | 电子表格数据库 (学员档案 / 对局记录 / 天梯榜) |
| **Google Apps Script** | 后端 API (读写 Sheets + Drive) |
| **Google Drive** | 云端文件存储 (记谱纸照片 / 收据 / XQF 棋谱 / 活动相册) |
| **Cloudflare Workers + KV** | 边缘网关 (登录鉴权 / 教练权限 / 学校授权 / 相册元数据) |
| **GitHub Pages** | 静态网站托管 (index.html + admin.html) |
| **Google Fonts** | Plus Jakarta Sans + Noto Sans SC 字体 |

---

## 🏗 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Pages                             │
│                  clubxiangqibera.github.io                       │
│           ┌──────────────┐  ┌──────────────┐                    │
│           │  index.html  │  │  admin.html  │                    │
│           │  (学生前台)   │  │  (教练后台)   │                    │
│           └──────┬───────┘  └──────┬───────┘                    │
└──────────────────┼─────────────────┼────────────────────────────┘
                   │                 │
         ┌─────────┴─────────────────┴──────────┐
         ▼                                      ▼
┌─────────────────────┐          ┌──────────────────────────────┐
│  Google Apps Script  │          │     Cloudflare Worker + KV   │
│  (Code.gs Web App)   │          │  cxb-license.workers.dev     │
│                      │          │                              │
│  POST 动作:           │          │  • /api/admin/login          │
│  • addMatch          │          │  • /api/admin/coaches        │
│  • addStudent        │          │  • /api/events               │
│  • updatePayment     │          │  • /api/admin/events         │
│  • uploadReceipt     │          │  • /api/verify               │
│  • changePassword    │          │  • /api/admin/create-license │
│  • updateMatchXQF    │          │  • /api/admin/list-licenses  │
│  • uploadEventPhoto  │          │  • /api/admin/extend         │
│  • deleteMatch       │          │  • /api/admin/end-key        │
│  • ...               │          │  • /api/admin/revoke         │
└──────────┬───────────┘          └──────────────────────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
┌────────┐  ┌──────────┐
│ Google │  │  Google   │
│ Sheets │  │  Drive    │
│ (数据)  │  │ (文件)    │
└────────┘  └──────────┘
```

---

## 📁 文件清单

| 文件 | 大小 | 行数 | 说明 |
|------|------|------|------|
| `web_deploy_org/index.html` | ~82KB | ~1,700 | 学员与公众前台 (含 CSS + JS) |
| `web_deploy_org/admin.html` | ~133KB | ~2,800 | 教练与总管理后台 (含 CSS + JS) |
| `web_deploy_org/Code.gs` | ~23KB | ~590 | Google Apps Script 后端 |
| `worker_v2.js` | ~12KB | ~315 | Cloudflare Worker 边缘网关 |
| `web_deploy_org/cxb_round_emblem.png` | - | - | 俱乐部圆形徽章 Logo |

### 文件同步位置 (3 份副本)
1. `web_deploy_org/` — GitHub Pages 源 (git push 部署)
2. `../web_v2/` — 本地备份
3. `../../Club XiangQi Bera/03_*/cxb_system_web/` — 共享文件夹

---

## 🎯 功能总览

### 学员前台 (`index.html`)

#### 公开模式 (免登录)
- ✅ 品牌导航栏 (汉堡菜单)
- ✅ Hero 统计面板 (学员数/对局数/段位体系)
- ✅ 教育营宣传 Banner + 海报放大 + Google Form 报名
- ✅ 实时滚屏战报 Ticker (最近 8 盘)
- ✅ 历届活动相册 (Cloudflare KV → Drive 缩略图)
- ✅ 全县天梯三甲领奖台 + 完整排位榜
- ✅ VIP 登录引导卡

#### 学员模式 (登录后)
- ✅ 个人战绩仪表盘 (ELO / 排位 / 段位 / 进度条)
- ✅ 8 个快捷导航图标 (日程/学费/天梯/棋谱/相册/设置/报名/群)
- ✅ 最近 5 场个人对局卡片 (胜/负/和)
- ✅ 训练日程 (按 Lv1/2/3 自动显示不同课表)
- ✅ 学费缴交 + 收据凭证上传
- ✅ 全县天梯 (自己行高亮)
- ✅ 实战棋谱 (**仅显示自己的对局** + 记谱纸查看 + XQF 上传/下载)
- ✅ 活动相册浏览
- ✅ 个人设置 (修改密码)

### 教练后台 (`admin.html`)

| Tab | 功能 | 权限 |
|-----|------|------|
| 📊 运营看板 | 4大KPI + 学员总览表 | Coach / SuperAdmin |
| 👥 学员建档 | 极速录入 + 档案管理 + 删除 | Coach / SuperAdmin |
| 💰 学费审核 | 审核清单 + 查看收据 + 确认缴费 | Coach / SuperAdmin |
| 📄 对局档案 | 卡片式归档 + 照片/XQF 上传 + 单条删除 | Coach / SuperAdmin |
| 🏆 锦标赛 | 瑞士制编排引擎 + SP98 导入 + ELO 结算 | Coach / SuperAdmin |
| 🏅 ELO天梯 | 三甲领奖台 + 全员排位 | Coach / SuperAdmin |
| 🔑 账号管理 | 教练CRUD + 权限配置 + 学员密码 | **SuperAdmin** |
| 📸 活动相册 | 创建相册 + 多图上传 + 编辑 | **SuperAdmin** |
| 🛡️ 学校授权 | 生成激活码 + 租约管理 + 延期/终止 | **SuperAdmin** |

---

## 📊 数据模型

### Google Sheets 表结构

#### 学员档案总册 (14 列)
| 列 | 字段 | 说明 | 示例 |
|----|------|------|------|
| A | id | 学号 | `XQB-007` |
| B | cnName | 中文名 (登录账号) | `林家豪` |
| C | enName | 英文名 | `Lim Jia Hao` |
| D | gender | 性别 | `男` |
| E | age | 年龄 | `12` |
| F | school | 学校 | `SJK(C) Triang (1)` |
| G | level | 班级 | `Lv 2 进阶班` |
| H | feeMode | 缴费模式 | `Combo 季度 (RM200)` |
| I | payStatus | 缴费状态 | `已缴费 (Verified)` 或 `⏳ 待核实\|imgUrl` |
| J | comboExpiry | 季度到期日 | `2026-12-31` |
| K | whatsapp | 家长电话 | `012-3456789` |
| L | elo | ELO积分 | `350` |
| M | tier | 段位 | `🥈 四级棋手` |
| N | password | 密码 | (默认: 级别数字+学号数字, 如 `2007`) |

#### 实战对局记录表 (10 列)
| 列 | 字段 | 说明 |
|----|------|------|
| A | date | 比赛日期 |
| B | round | 轮次名称 |
| C | redId | 红方学号 |
| D | redName | 红方姓名 |
| E | result | 赛果 (`🔴 红胜`, `⚫ 黑胜`, `🤝 和棋`) |
| F | blackId | 黑方学号 |
| G | blackName | 黑方姓名 |
| H | verdict | 裁决说明 |
| I | recordImg | 记谱纸照片 URL |
| J | xqfFile | XQF 棋谱文件 URL |

#### 天梯积分排位榜 (10 列)
| 列 | 字段 |
|----|------|
| A | rank (排名) |
| B | studentId (学号) |
| C | name (姓名) |
| D | school (学校) |
| E | tier (段位) |
| F | wins (胜) |
| G | draws (和) |
| H | losses (负) |
| I | total (总局) |
| J | elo (ELO) |

### Cloudflare KV 键值

| Key | 说明 |
|-----|------|
| `CXB-XXXX` | 学校授权码 `{ school, maxRounds, expiresAt, status }` |
| `COACH_ACCOUNTS` | 教练列表 `[{ id, name, pin, perms }]` |
| `EVENTS_GALLERY` | 相册列表 `[{ id, name, date, desc, photos }]` |

---

## 🔌 API 接口清单

### Google Apps Script (Code.gs) — POST Actions

| Action | 说明 | 写入目标 |
|--------|------|----------|
| `addMatch` | 录入对局 + ELO 结算 | 对局表 + 天梯榜 + 学员表 |
| `addStudent` | 快速建档 | 学员表 + 天梯榜 |
| `updatePayment` | 更新缴费状态 | 学员表 Col I |
| `updateAccount` | 修改姓名/密码/班级 | 学员表 + 天梯榜 |
| `uploadReceipt` | 上传收据图片 | Drive + 学员表 |
| `updateMatchPhoto` | 补传记谱纸照片 | Drive + 对局表 Col I |
| `updateMatchXQF` | 上传 XQF 棋谱 | Drive + 对局表 Col J |
| `changePassword` | 学员改密码 | 学员表 Col N |
| `deleteMatch` | 删除对局 | 对局表 |
| `deleteStudent` | 注销学员 | 学员表 + 天梯榜 |
| `clearTestData` | 清空全部对局 | 对局表 |
| `uploadEventPhoto` | 上传活动照片 | Drive |

### Cloudflare Worker — HTTP 接口

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/api/admin/login` | - | 登录鉴权 |
| POST | `/api/verify` | 授权码 | 学校端验证 |
| GET | `/api/admin/coaches` | PIN | 教练列表 |
| POST | `/api/admin/coaches` | PIN | 更新教练 |
| GET | `/api/events` | 公开 | 活动相册 |
| POST | `/api/admin/events` | PIN | 更新相册 |
| POST | `/api/admin/create-license` | PIN | 创建授权码 |
| POST | `/api/admin/list-licenses` | PIN | 列出授权码 |
| POST | `/api/admin/extend` | PIN | 延期授权 |
| POST | `/api/admin/end-key` | PIN | 终止授权 |
| POST | `/api/admin/resume-key` | PIN | 恢复授权 |
| POST | `/api/admin/revoke` | PIN | 删除授权 |

---

## 🚀 部署指南

### 前端部署 (GitHub Pages)
```bash
cd web_deploy_org
git add .
git commit -m "update"
git push origin main
# 访问: https://clubxiangqibera.github.io
```

### 后端部署 (Google Apps Script)
1. 打开 Google Apps Script 编辑器
2. 将 `Code.gs` 全部内容粘贴覆盖
3. **部署 → 管理部署 → 编辑 → 版本: 新版本 → 部署**

### Cloudflare Worker 部署
```bash
cd 03_系统自动化脚本与代码_Scripts_&_Code
python _AI_Scripts_Archive/upload_worker.py
```

---

## 🐛 已知问题与改进计划

### 🔴 严重 Bug (需立即修复)

| # | 问题 | 影响 | 文件 |
|---|------|------|------|
| 1 | `index.html` 的 `loadMatches` 未读取第10列 `xqfFile` | 学员端看不到 XQF 下载按钮 | index.html |
| 2 | `list-licenses` 会列出系统 Key (COACH_ACCOUNTS / EVENTS_GALLERY) | 误删将清空教练或相册 | worker_v2.js |
| 3 | 删除对局不回滚 ELO 和胜率 | 清空数据后 ELO 虚高 | Code.gs |
| 4 | 相册 `editEvent` / `deleteEvent` 函数未定义 | 无法编辑或删除相册 | admin.html |

### 🟡 安全隐患

| # | 问题 | 建议 |
|---|------|------|
| 5 | 密码与电话明文暴露在 CSV 公开链接 | 考虑服务端鉴权中间层 |
| 6 | 教练有 `licenses` 权限但 Worker 只接受 SuperAdmin PIN | 让 Worker 也接受教练 PIN |

### 🟢 功能优化 (Future)

| # | 建议 | 优先级 |
|---|------|--------|
| 7 | WhatsApp 群链接仍是占位符 | P0 |
| 8 | 锦标赛 Buchholz 轮空补偿不完整 | P2 |
| 9 | ELO 成长曲线图 (Chart.js) | P3 |
| 10 | 公告/通知系统 | P3 |
| 11 | 多语言 i18n 完善 | P4 |
| 12 | PWA 离线支持 | P5 |

---

## 📝 版本日志

| 日期 | 更新 |
|------|------|
| 2026-10-02 | 学员端重新设计: Bug修复、相册/设置/密码修改、XQF上传、个人对局过滤 |
| 2026-10-01 | 活动相册系统、教练管理系统、锦标赛瑞士制编排引擎 |
| 2026-09 | 初始版本: 学员建档、对局录入、ELO天梯、学费管理、学校授权 |

---

> **© 2026 Persatuan Catur Cina Daerah Bera (百乐县中国象棋公会)**  
> Built with ❤️ by Nicholas Wong
