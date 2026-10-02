import io

with io.open('Code.gs', 'r', encoding='utf-8') as f:
    text = f.read()

# Task 5D
change_pwd_js = """
    } else if (action === 'changePassword') {
      return handleChangePassword(data);
"""
text = text.replace("} else if (action === 'uploadEventPhoto') {", change_pwd_js + "} else if (action === 'uploadEventPhoto') {")


handler_js = """
function handleChangePassword(data) {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const studentSheet = ss.getSheetByName('学员档案总册');
    const stuData = studentSheet.getDataRange().getValues();

    for (let r = 1; r < stuData.length; r++) {
      if (String(stuData[r][0] || '').trim() === String(data.studentId || '').trim()) {
        // Verify old password
        const storedPwd = String(stuData[r][13] || '').trim();
        // Calculate default password
        const lvMatch = (String(stuData[r][6] || '')).match(/Lv\\s*(\\d)/);
        const lvNum = lvMatch ? lvMatch[1] : '1';
        const idMatch = (String(stuData[r][0] || '')).match(/(\\d+)$/);
        const idNum = idMatch ? idMatch[1] : '001';
        const defaultPwd = lvNum + idNum;
        const currentPwd = storedPwd || defaultPwd;

        if (data.oldPassword !== currentPwd) {
          return respond({ status: 'error', error: '当前密码错误' });
        }

        if (!data.newPassword || data.newPassword.length < 4) {
          return respond({ status: 'error', error: '新密码至少4位' });
        }

        // Update password (column 14, index 13, so getRange row, 14)
        studentSheet.getRange(r + 1, 14).setValue(data.newPassword);
        return respond({ status: 'ok', success: true, message: '密码修改成功' });
      }
    }
    return respond({ status: 'error', error: '找不到学员' });
  } catch(e) {
    return respond({ status: 'error', error: e.toString() });
  }
}
"""
text = text.replace("function handleDeleteMatch(data) {", handler_js + "\nfunction handleDeleteMatch(data) {")

with io.open('Code.gs', 'w', encoding='utf-8') as f:
    f.write(text)
print("Code.gs updated successfully")
