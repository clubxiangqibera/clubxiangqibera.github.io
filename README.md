# Club XiangQi Bera — 青少年象棋天梯排位系统 V2 (CXB ELO System)

百乐象棋俱乐部（Club XiangQi Bera）官方青少年天梯积分排位系统与学员管理门户。

## 🌟 系统特色与页面结构
- **公开天梯排行榜 (`index.html`)**：
  - 手机/电脑自适应，荣耀三甲动态奖台（#1 荣膺「👑 月度擂主」）
  - CXB ELO 积分成长体系：基准 200 分起步，对齐正规竞技五级制（五级至一级棋手）
  - 动态天梯晋阶进度条与胜率环比
  - 最近对局动态跑马灯与实战对局清单
  - **记谱纸图片查看**：支持点击展开、大图 Lightbox 弹窗浏览已上传的对局记谱纸原件
  - 直连 Google Sheets 数据库，60 秒自动静默刷新

- **教练与管理后台 (`admin.html`)**：
  - 独立 PIN 密码保护（默认 PIN: `8888`，24小时免登录凭证）
  - **总览面板**：学员总数、本月预估收入、待收学费、对局总数核心指标
  - **学员管理**：全校区学员花名册与一键入库建档
  - **实战录入**：单盘录入 + SP98 瑞士制战报智能批量解析入库
  - **对局记谱纸上传**：支持拍照或相册选择对局纸图片上传，自动归档并展示
  - **学费追踪**：查看每位学员就读级别、Combo 模式、到期月份及一键标记缴费
  - 官方收款账户一览：Public Bank `3246504527`（Persatuan Catur Cina Daerah Bera）

- **云端后端 API (`Code.gs`)**：
  - Google Apps Script 自动化脚本
  - 支持向 Google Sheets 自动追加对局记录、计算升降级积分、建档新学员、更新学费状态及将记谱纸照片自动存储至 Google Drive

---

## 🚀 Google Apps Script (GAS) 部署指南 (3分钟完成)

若需启用后台一键写入 Google 表格及照片上传功能：
1. 打开俱乐部官方表格：[Google Sheets 后台](https://docs.google.com/spreadsheets/d/1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y)
2. 菜单栏点击：**扩展程序 (Extensions)** -> **Apps Script**
3. 将项目中的 `Code.gs` 文件全部代码复制粘贴到编辑器中，覆盖保存
4. 点击右上角 **部署 (Deploy)** -> **新建部署 (New deployment)**：
   - 齿轮选择 **Web 应用 (Web app)**
   - 说明填：`CXB Admin API`
   - 执行身份 (Execute as)：**我 (Me)**
   - 谁可以访问 (Who has access)：**所有人 (Anyone)** *(务必选择此项)*
5. 点击 **部署**，授权 Google 账号权限，复制生成的 `Web 应用网址`
6. 在 `admin.html` 中找到 `const GAS_API_URL = 'YOUR_GAS_DEPLOYMENT_URL';`，将网址替换进去并保存即可！

---
© 2026 Club XiangQi Bera (百乐象棋俱乐部) · 版权所有
