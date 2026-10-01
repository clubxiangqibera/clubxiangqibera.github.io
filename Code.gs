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
 *
 * 更新日志:
 * v2.1 - 新增 updateAccount 功能 (修改学员姓名/密码)
 *       - 修正天梯/学员档案循环起始行为第2行 (r=1)
 *       - 移除服务端 PIN 验证 (改由前端负责)
 *       - ELO 使用前端传入的 K-factor delta
 */

const SHEET_ID = '1s_QoX0venwd3kDj1m3QoxgjJPsS82G9Ii8oMHr8150Y';

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: 'ok', msg: 'Club XiangQi Bera API v2.1 is running' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    const raw = e.postData.contents;
    const data = JSON.parse(raw);

    const action = data.action;
    if (action === 'addMatch') {
      return handleAddMatch(data);
    } else if (action === 'addStudent') {
      return handleAddStudent(data);
    } else if (action === 'updatePayment') {
      return handleUpdatePayment(data);
    } else if (action === 'updateAccount') {
      return handleUpdateAccount(data);
    } else if (action === 'uploadReceipt') {
      return handleUploadReceipt(data);
    } else if (action === 'deleteMatch') {
      return handleDeleteMatch(data);
    } else if (action === 'deleteStudent') {
      return handleDeleteStudent(data);
    } else if (action === 'clearTestData') {
      return handleClearTestData(data);
    } else {
      return respond({ status: 'error', error: '未知操作: ' + action });
    }

  } catch (err) {
    return respond({ status: 'error', error: err.toString() });
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

// 1. 录入对局 (ELO delta 由前端 K-factor 计算传入，或用默认值)
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
      const fileName = 'Record_' + data.date + '_' + data.redName + '_vs_' + data.blackName + '.jpg';
      const blob = Utilities.newBlob(decoded, contentType, fileName);
      const file = folder.createFile(blob);
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
      imgUrl = file.getUrl();
    } catch (e) {
      imgUrl = '图片保存异常: ' + e.toString();
    }
  }

  // 写入实战对局记录表
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

  // ELO delta: 前端传入 (K-factor 计算) 或 用默认 win=+20, draw=+5, loss=-10
  let redDelta = 0, blackDelta = 0;
  let redW = 0, redD = 0, redL = 0;
  let blackW = 0, blackD = 0, blackL = 0;

  if (data.redEloDelta !== undefined && data.blackEloDelta !== undefined) {
    // Frontend K-factor computed deltas
    redDelta = Number(data.redEloDelta) || 0;
    blackDelta = Number(data.blackEloDelta) || 0;
  } else {
    // Fallback defaults
    if (data.result.indexOf('红胜') !== -1) {
      redDelta = 20; blackDelta = -10;
    } else if (data.result.indexOf('黑胜') !== -1) {
      redDelta = -10; blackDelta = 20;
    } else {
      redDelta = 5; blackDelta = 5;
    }
  }

  // Win/draw/loss counters
  if (data.result.indexOf('红胜') !== -1) {
    redW = 1; blackL = 1;
  } else if (data.result.indexOf('黑胜') !== -1) {
    redL = 1; blackW = 1;
  } else {
    redD = 1; blackD = 1;
  }

  // 更新 天梯积分排位榜 (第2行起为数据，r=1)
  const ladderData = ladderSheet.getDataRange().getValues();
  for (let r = 1; r < ladderData.length; r++) {
    const pId = String(ladderData[r][1] || '').trim();
    if (pId === String(data.redId || '').trim()) {
      const curW = Number(ladderData[r][5]) || 0;
      const curD = Number(ladderData[r][6]) || 0;
      const curL = Number(ladderData[r][7]) || 0;
      const curElo = Number(ladderData[r][9]) || 200;
      const newElo = Math.max(200, curElo + redDelta);
      ladderSheet.getRange(r + 1, 5).setValue(calculateTier(newElo));
      ladderSheet.getRange(r + 1, 6).setValue(curW + redW);
      ladderSheet.getRange(r + 1, 7).setValue(curD + redD);
      ladderSheet.getRange(r + 1, 8).setValue(curL + redL);
      ladderSheet.getRange(r + 1, 9).setValue(curW + redW + curD + redD + curL + redL);
      ladderSheet.getRange(r + 1, 10).setValue(newElo);
    } else if (pId === String(data.blackId || '').trim()) {
      const curW = Number(ladderData[r][5]) || 0;
      const curD = Number(ladderData[r][6]) || 0;
      const curL = Number(ladderData[r][7]) || 0;
      const curElo = Number(ladderData[r][9]) || 200;
      const newElo = Math.max(200, curElo + blackDelta);
      ladderSheet.getRange(r + 1, 5).setValue(calculateTier(newElo));
      ladderSheet.getRange(r + 1, 6).setValue(curW + blackW);
      ladderSheet.getRange(r + 1, 7).setValue(curD + blackD);
      ladderSheet.getRange(r + 1, 8).setValue(curL + blackL);
      ladderSheet.getRange(r + 1, 9).setValue(curW + blackW + curD + blackD + curL + blackL);
      ladderSheet.getRange(r + 1, 10).setValue(newElo);
    }
  }

  // 同步更新 学员档案总册 ELO & Tier (第2行起为数据，r=1)
  if (studentSheet) {
    const stuData = studentSheet.getDataRange().getValues();
    for (let r = 1; r < stuData.length; r++) {
      const sId = String(stuData[r][0] || '').trim();
      if (sId === String(data.redId || '').trim()) {
        const curElo = Number(stuData[r][11]) || 200;
        const newElo = Math.max(200, curElo + redDelta);
        studentSheet.getRange(r + 1, 12).setValue(newElo);
        studentSheet.getRange(r + 1, 13).setValue(calculateTier(newElo));
      } else if (sId === String(data.blackId || '').trim()) {
        const curElo = Number(stuData[r][11]) || 200;
        const newElo = Math.max(200, curElo + blackDelta);
        studentSheet.getRange(r + 1, 12).setValue(newElo);
        studentSheet.getRange(r + 1, 13).setValue(calculateTier(newElo));
      }
    }
  }

  return respond({ status: 'ok', success: true, message: '对局录入并完成 ELO 积分结算！', imgUrl: imgUrl });
}

// 2. 登记新学员
function handleAddStudent(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const ladderSheet = ss.getSheetByName('天梯积分排位榜');

  const stuData = studentSheet.getDataRange().getValues();
  let count = 0;
  for (let r = 1; r < stuData.length; r++) {
    if (stuData[r][0] && stuData[r][0].toString().startsWith('XQB-')) {
      count++;
    }
  }
  const nextNum = count + 1;
  const newId = 'XQB-' + ('000' + nextNum).slice(-3);

  // 计算默认密码 = 级别数字 + 编号数字 (e.g. Lv2 XQB-007 → 2007)
  const lvMatch = (data.level || '').match(/Lv\s*(\d)/);
  const lvNum = lvMatch ? lvMatch[1] : '1';
  const defaultPwd = lvNum + ('000' + nextNum).slice(-3);

  // 写入学员档案总册
  // [ID, 中文, 英文, 性别, 年龄, 学校, 级别, 学费模式, 缴费状态, Combo到期, WhatsApp, ELO, 认定级别, 密码]
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
    '🥉 五级棋手',
    defaultPwd
  ]);

  // 同步添加至 天梯积分排位榜
  ladderSheet.appendRow([
    nextNum,
    newId,
    data.cnName,
    data.school,
    '🥉 五级棋手',
    0, 0, 0, 0,
    200
  ]);

  return respond({ status: 'ok', success: true, newId: newId, defaultPwd: defaultPwd, message: '新学员 ' + data.cnName + ' (' + newId + ') 已成功入库！默认密码: ' + defaultPwd });
}

// 3. 更新学费状态
function handleUpdatePayment(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const stuData = studentSheet.getDataRange().getValues();

  for (let r = 1; r < stuData.length; r++) {
    if (String(stuData[r][0] || '').trim() === String(data.studentId || '').trim()) {
      studentSheet.getRange(r + 1, 9).setValue(data.status || '已缴费 (Verified)');
      return respond({ status: 'ok', success: true, message: '学员 ' + data.studentId + ' 缴费状态已更新！' });
    }
  }
  return respond({ status: 'error', error: '未找到该学员编号: ' + data.studentId });
}

// 4. 修改学员账号信息 (姓名 / 密码)
function handleUpdateAccount(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const ladderSheet = ss.getSheetByName('天梯积分排位榜');
  const stuData = studentSheet.getDataRange().getValues();

  let found = false;
  for (let r = 1; r < stuData.length; r++) {
    if (String(stuData[r][0] || '').trim() === String(data.studentId || '').trim()) {
      // 更新中文姓名 (第2列)
      if (data.newName) {
        studentSheet.getRange(r + 1, 2).setValue(data.newName);
        // 同步更新天梯榜姓名
        const ladderData = ladderSheet.getDataRange().getValues();
        for (let lr = 1; lr < ladderData.length; lr++) {
          if (String(ladderData[lr][1] || '').trim() === String(data.studentId || '').trim()) {
            ladderSheet.getRange(lr + 1, 3).setValue(data.newName);
            break;
          }
        }
      }
      // 更新密码 (第14列，index 13)
      if (data.newPwd) {
        studentSheet.getRange(r + 1, 14).setValue(data.newPwd);
      }
      if (data.newLevel) {
        studentSheet.getRange(r + 1, 7).setValue(data.newLevel);
      }
      if (data.newLevel) {
        studentSheet.getRange(r + 1, 7).setValue(data.newLevel);
      }
      found = true;
      return respond({ status: 'ok', success: true, message: '账号信息已更新：' + data.studentId });
    }
  }

  if (!found) {
    return respond({ status: 'error', error: '未找到该学员编号: ' + data.studentId });
  }
}

// 5. 上传转账收据图片
function handleUploadReceipt(data) {
  try {
    const folder = getRecordFolder();
    const parts = data.receiptImage.split(',');
    const contentType = parts[0].split(':')[1].split(';')[0];
    const decoded = Utilities.base64Decode(parts[1]);
    const fileName = 'Receipt_' + data.studentId + '_' + new Date().toISOString().slice(0,10) + '.jpg';
    const blob = Utilities.newBlob(decoded, contentType, fileName);
    const file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    const imgUrl = file.getUrl();

    // Mark payment as pending verification in student sheet
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const studentSheet = ss.getSheetByName('学员档案总册');
    const stuData = studentSheet.getDataRange().getValues();
    for (let r = 1; r < stuData.length; r++) {
      if (String(stuData[r][0] || '').trim() === String(data.studentId || '').trim()) {
        studentSheet.getRange(r + 1, 9).setValue('⏳ 待核实 (收据已上传)');
        break;
      }
    }

    return respond({ status: 'ok', success: true, imgUrl: imgUrl, message: '转账收据已上传，待教练核实。' });
  } catch(e) {
    return respond({ status: 'error', error: '上传失败: ' + e.toString() });
  }
}

// 6. 删除单条实战对局记录
function handleDeleteMatch(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const matchSheet = ss.getSheetByName('实战对局记录表');
  const values = matchSheet.getDataRange().getValues();

  for (let r = 1; r < values.length; r++) {
    const rowDate = String(values[r][0] || '').trim();
    const rowRound = String(values[r][1] || '').trim();
    const rowRed = String(values[r][3] || '').trim();
    const rowBlack = String(values[r][6] || '').trim();

    // Match criteria: row index or match details
    if (data.rowIndex && Number(data.rowIndex) === r + 1) {
      matchSheet.deleteRow(r + 1);
      return respond({ status: 'ok', success: true, message: '对局记录已成功删除！' });
    }
    if (data.date === rowDate && data.round === rowRound && data.redName === rowRed && data.blackName === rowBlack) {
      matchSheet.deleteRow(r + 1);
      return respond({ status: 'ok', success: true, message: '对局记录已成功删除！' });
    }
  }
  return respond({ status: 'error', error: '未找到匹配的对局记录' });
}

// 7. 删除学员 (同时自档案总册与天梯榜移除)
function handleDeleteStudent(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const studentSheet = ss.getSheetByName('学员档案总册');
  const ladderSheet = ss.getSheetByName('天梯积分排位榜');

  const sId = String(data.studentId || '').trim();
  let deleted = false;

  if (studentSheet) {
    const sData = studentSheet.getDataRange().getValues();
    for (let r = 1; r < sData.length; r++) {
      if (String(sData[r][0] || '').trim() === sId) {
        studentSheet.deleteRow(r + 1);
        deleted = true;
        break;
      }
    }
  }

  if (ladderSheet) {
    const lData = ladderSheet.getDataRange().getValues();
    for (let r = 1; r < lData.length; r++) {
      if (String(lData[r][1] || '').trim() === sId) {
        ladderSheet.deleteRow(r + 1);
        break;
      }
    }
  }

  if (deleted) {
    return respond({ status: 'ok', success: true, message: `学员 ${sId} 已成功从档案及天梯榜删除！` });
  } else {
    return respond({ status: 'error', error: '未在学员档案中找到学号: ' + sId });
  }
}

// 8. 一键清空所有测试对局记录
function handleClearTestData(data) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const matchSheet = ss.getSheetByName('实战对局记录表');
  if (matchSheet) {
    const lastRow = matchSheet.getLastRow();
    if (lastRow > 1) {
      matchSheet.deleteRows(2, lastRow - 1);
    }
  }
  return respond({ status: 'ok', success: true, message: '所有实战对局记录已全部清空！' });
}
