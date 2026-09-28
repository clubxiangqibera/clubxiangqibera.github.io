/**
 * Club XiangQi Bera - Google Apps Script 云端后端 API
 * 电子表格 ID: 1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y
 * 
 * 部署步骤 (只需一次，耗时约 3 分钟):
 * 1. 打开 Google 电子表格: https://docs.google.com/spreadsheets/d/1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y
 * 2. 菜单点击: 扩展程序 (Extensions) -> Apps Script
 * 3. 将本文件全部代码复制粘贴进去，覆盖已有内容
 * 4. 点击右上角蓝色「部署」(Deploy) ->「新建部署」(New deployment)
 * 5. 类型选择「Web 应用」(Web app):
 *    - 说明: CXB Admin API
 *    - 执行身份 (Execute as): 我 (Me)
 *    - 谁可以访问 (Who has access): 所有人 (Anyone)  <-- 非常重要！
 * 6. 点击「部署」，授权权限，复制生成的「Web 应用网址」(Web app URL)
 * 7. 将该 URL 填入 admin.html 的 const GAS_API_URL = '...' 中！
 */

const SHEET_ID = '1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y';
const ADMIN_PIN = '8888';

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: 'ok', msg: 'Club XiangQi Bera API is running' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    const raw = e.postData.contents;
    const data = JSON.parse(raw);

    // 验证管理密码 PIN
    if (data.pin !== ADMIN_PIN) {
      return respond({ success: false, error: 'PIN 密码错误，未经授权' });
    }

    const action = data.action;
    if (action === 'addMatch') {
      return handleAddMatch(data);
    } else if (action === 'addStudent') {
      return handleAddStudent(data);
    } else if (action === 'updatePayment') {
      return handleUpdatePayment(data);
    } else {
      return respond({ success: false, error: '未知操作: ' + action });
    }

  } catch (err) {
    return respond({ success: false, error: err.toString() });
  }
}

function respond(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// 辅助：获取或创建存储对局记录纸的 Google Drive 文件夹
function getRecordFolder() {
  const folderName = 'CXB_对局记录纸_MatchRecords';
  const folders = DriveApp.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.createFolder(folderName);
}

// 计算段位
function calculateTier(elo) {
  if (elo >= 1300) return '👑 一级棋手';
  if (elo >= 1000) return '💎 二级棋手';
  if (elo >= 700) return '🥇 三级棋手';
  if (elo >= 400) return '🥈 四级棋手';
  return '🥉 五级棋手';
}

// 1. 录入对局
function handleAddMatch(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const matchSheet = ss.getSheetByName('实战对局记录表');
  const ladderSheet = ss.getSheetByName('天梯积分排位榜');
  const studentSheet = ss.getSheetByName('学员档案总册');

  // 如果上传了记录纸图片 (base64)
  let imgUrl = '';
  if (data.recordImage && data.recordImage.indexOf('data:image') !== -1) {
    try {
      const folder = getRecordFolder();
      const parts = data.recordImage.split(',');
      const contentType = parts[0].split(':')[1].split(';')[0];
      const decoded = Utilities.base64Decode(parts[1]);
      const fileName = `Record_${data.date}_${data.redName}_vs_${data.blackName}.jpg`;
      const blob = Utilities.newBlob(decoded, contentType, fileName);
      const file = folder.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      imgUrl = file.getUrl();
    } catch (e) {
      // 图片保存失败不影响比赛成绩录入
      imgUrl = '图片保存异常: ' + e.toString();
    }
  }

  // 写入实战对局记录表
  // 结构: 对局日期 | 轮次/类别 | 红方编号 | 红方姓名 | 对局结果 | 黑方编号 | 黑方姓名 | 胜负判定 | 记录纸图片
  matchSheet.appendRow([
    data.date,
    data.round,
    data.redId,
    data.redName,
    data.result,
    data.blackId,
    data.blackName,
    data.verdict,
    imgUrl
  ]);

  // 计算 ELO 与战绩变化
  // 规则: 胜 +20, 和 +5, 负 -10
  let redDelta = 0, blackDelta = 0;
  let redW = 0, redD = 0, redL = 0;
  let blackW = 0, blackD = 0, blackL = 0;

  if (data.result.indexOf('红胜') !== -1) {
    redDelta = 20; blackDelta = -10;
    redW = 1; blackL = 1;
  } else if (data.result.indexOf('黑胜') !== -1) {
    redDelta = -10; blackDelta = 20;
    redL = 1; blackW = 1;
  } else {
    redDelta = 5; blackDelta = 5;
    redD = 1; blackD = 1;
  }

  // 更新 天梯积分排位榜 (从第4行开始是数据)
  const ladderData = ladderSheet.getDataRange().getValues();
  for (let r = 3; r < ladderData.length; r++) {
    const pId = ladderData[r][1]; // 学员编号
    if (pId === data.redId) {
      const curW = Number(ladderData[r][5]) || 0;
      const curD = Number(ladderData[r][6]) || 0;
      const curL = Number(ladderData[r][7]) || 0;
      const curElo = Number(ladderData[r][9]) || 200;
      const newElo = Math.max(200, curElo + redDelta);
      const newTier = calculateTier(newElo);

      ladderSheet.getRange(r + 1, 5).setValue(newTier);
      ladderSheet.getRange(r + 1, 6).setValue(curW + redW);
      ladderSheet.getRange(r + 1, 7).setValue(curD + redD);
      ladderSheet.getRange(r + 1, 8).setValue(curL + redL);
      ladderSheet.getRange(r + 1, 9).setValue(curW + redW + curD + redD + curL + redL);
      ladderSheet.getRange(r + 1, 10).setValue(newElo);
    } else if (pId === data.blackId) {
      const curW = Number(ladderData[r][5]) || 0;
      const curD = Number(ladderData[r][6]) || 0;
      const curL = Number(ladderData[r][7]) || 0;
      const curElo = Number(ladderData[r][9]) || 200;
      const newElo = Math.max(200, curElo + blackDelta);
      const newTier = calculateTier(newElo);

      ladderSheet.getRange(r + 1, 5).setValue(newTier);
      ladderSheet.getRange(r + 1, 6).setValue(curW + blackW);
      ladderSheet.getRange(r + 1, 7).setValue(curD + blackD);
      ladderSheet.getRange(r + 1, 8).setValue(curL + blackL);
      ladderSheet.getRange(r + 1, 9).setValue(curW + blackW + curD + blackD + curL + blackL);
      ladderSheet.getRange(r + 1, 10).setValue(newElo);
    }
  }

  // 同步更新 学员档案总册 的 ELO & Tier
  if (studentSheet) {
    const stuData = studentSheet.getDataRange().getValues();
    for (let r = 3; r < stuData.length; r++) {
      const sId = stuData[r][0];
      if (sId === data.redId) {
        const curElo = Number(stuData[r][11]) || 200;
        const newElo = Math.max(200, curElo + redDelta);
        studentSheet.getRange(r + 1, 12).setValue(newElo);
        studentSheet.getRange(r + 1, 13).setValue(calculateTier(newElo));
      } else if (sId === data.blackId) {
        const curElo = Number(stuData[r][11]) || 200;
        const newElo = Math.max(200, curElo + blackDelta);
        studentSheet.getRange(r + 1, 12).setValue(newElo);
        studentSheet.getRange(r + 1, 13).setValue(calculateTier(newElo));
      }
    }
  }

  return respond({ success: true, message: '对局录入并自动完成 ELO 积分结算！', imgUrl: imgUrl });
}

// 2. 登记新学员
function handleAddStudent(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const ladderSheet = ss.getSheetByName('天梯积分排位榜');

  const stuData = studentSheet.getDataRange().getValues();
  // 计算新学号 XQB-00X
  let count = 0;
  for (let r = 3; r < stuData.length; r++) {
    if (stuData[r][0] && stuData[r][0].toString().startsWith('XQB-')) {
      count++;
    }
  }
  const nextNum = count + 1;
  const newId = 'XQB-' + ('000' + nextNum).slice(-3);

  // 写入学员档案总册
  // [ID, 中文, 英文, 性别, 年龄, 学校, 级别, 学费模式, 缴费状态, Combo到期, WhatsApp, ELO, 认定级别]
  studentSheet.appendRow([
    newId,
    data.cnName,
    data.enName || '',
    data.gender || '男',
    data.age || '',
    data.school,
    data.level,
    data.feeMode || '月缴',
    '⏳ 待缴费',
    '',
    data.whatsapp || '',
    200,
    '🥉 五级棋手'
  ]);

  // 同步添加至 天梯积分排位榜
  // [当前排名, 学员编号, 棋手姓名, 所在学校, 认定级别, 胜, 和, 负, 总对局, ELO]
  ladderSheet.appendRow([
    nextNum,
    newId,
    data.cnName,
    data.school,
    '🥉 五级棋手',
    0, 0, 0, 0,
    200
  ]);

  return respond({ success: true, newId: newId, message: `新学员 ${data.cnName} (${newId}) 已成功入库并建档！` });
}

// 3. 更新学费状态
function handleUpdatePayment(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const stuData = studentSheet.getDataRange().getValues();

  for (let r = 3; r < stuData.length; r++) {
    if (stuData[r][0] === data.studentId) {
      // 第9列为 缴费状态
      studentSheet.getRange(r + 1, 9).setValue(data.status || '已缴费 (Verified)');
      return respond({ success: true, message: `学员 ${data.studentId} 状态已更新为 ${data.status}！` });
    }
  }

  return respond({ success: false, error: '未找到该学员编号: ' + data.studentId });
}
