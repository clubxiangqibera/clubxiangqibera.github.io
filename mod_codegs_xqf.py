import io

with io.open('Code.gs', 'r', encoding='utf-8') as f:
    text = f.read()

handler_js = """
function handleUpdateMatchXQF(data) {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const matchSheet = ss.getSheetByName('实战对局记录表');
    const values = matchSheet.getDataRange().getValues();
    
    const folder = getRecordFolder(); // reuse same folder
    const parts = data.fileBase64.split(',');
    // XQF files might have different or empty mime types, we just decode base64
    const decoded = Utilities.base64Decode(parts[1]);
    const fileName = 'Record_' + data.date + '_' + data.redName + '_vs_' + data.blackName + '.xqf';
    const blob = Utilities.newBlob(decoded, 'application/octet-stream', fileName);
    const file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    const fileUrl = file.getUrl();

    let found = false;
    for (let r = 1; r < values.length; r++) {
      const rowDate = String(values[r][0] || '').trim();
      const matchDateStr = String(data.date).trim();
      if (rowDate.includes(matchDateStr) &&
          String(values[r][1] || '').trim() === String(data.round).trim() &&
          String(values[r][3] || '').trim() === String(data.redName).trim() &&
          String(values[r][6] || '').trim() === String(data.blackName).trim()) {
        matchSheet.getRange(r + 1, 10).setValue(fileUrl); // Column 10 is XQF
        found = true;
        break;
      }
    }
    
    if (found) {
      return respond({ status: 'ok', success: true, fileUrl: fileUrl });
    } else {
      return respond({ status: 'error', error: '找不到对应的比赛记录' });
    }
  } catch(e) {
    return respond({ status: 'error', error: e.toString() });
  }
}
"""

if 'handleUpdateMatchXQF' not in text:
    text = text.replace("} else if (action === 'updateMatchPhoto') {", "} else if (action === 'updateMatchXQF') {\n      return handleUpdateMatchXQF(data);\n    } else if (action === 'updateMatchPhoto') {")
    text = text.replace("function handleDeleteMatch(data) {", handler_js + "\nfunction handleDeleteMatch(data) {")

with io.open('Code.gs', 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Code.gs updated")
