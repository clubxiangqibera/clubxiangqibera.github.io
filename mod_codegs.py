import io

with io.open('Code.gs', 'r', encoding='utf-8') as f:
    text = f.read()

func = '''
function handleUpdateMatchPhoto(data) {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const matchSheet = ss.getSheetByName('实战对局记录表');
    const values = matchSheet.getDataRange().getValues();
    
    const folder = getRecordFolder();
    const parts = data.imageBase64.split(',');
    const contentType = parts[0].split(':')[1].split(';')[0];
    const decoded = Utilities.base64Decode(parts[1]);
    const fileName = 'Record_' + data.date + '_' + data.redName + '_vs_' + data.blackName + '.jpg';
    const blob = Utilities.newBlob(decoded, contentType, fileName);
    const file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    const imgUrl = file.getUrl();

    let found = false;
    for (let r = 1; r < values.length; r++) {
      const rowDate = String(values[r][0] || '').trim();
      const matchDateStr = String(data.date).trim();
      // sometimes date is an object or formatted differently, but we try exact string match
      // to be safe we can use include
      if (rowDate.includes(matchDateStr) &&
          String(values[r][1] || '').trim() === String(data.round).trim() &&
          String(values[r][3] || '').trim() === String(data.redName).trim() &&
          String(values[r][6] || '').trim() === String(data.blackName).trim()) {
        matchSheet.getRange(r + 1, 9).setValue(imgUrl);
        found = true;
        break;
      }
    }
    
    if (found) {
      return respond({ status: 'ok', success: true, imgUrl: imgUrl });
    } else {
      return respond({ status: 'error', error: '找不到对应的比赛记录' });
    }
  } catch(e) {
    return respond({ status: 'error', error: e.toString() });
  }
}
'''

if 'handleUpdateMatchPhoto' not in text:
    text = text.replace('function handleDeleteMatch(data) {', func + '\nfunction handleDeleteMatch(data) {')
    text = text.replace("else if (action === 'deleteMatch')", "else if (action === 'updateMatchPhoto') {\n      return handleUpdateMatchPhoto(data);\n    } else if (action === 'deleteMatch')")
    with io.open('Code.gs', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Code.gs updated")
else:
    print("Already added")
