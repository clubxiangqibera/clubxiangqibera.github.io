import io
import re

with io.open('../worker_v2.js', 'r', encoding='utf-8') as f:
    old_worker = f.read()

# Extract old logic inside the fetch try block
m = re.search(r'try \{([\s\S]*?)return jsonResponse\(\{ status: "ok"', old_worker)
if m:
    old_logic = m.group(1)
else:
    old_logic = "// Failed to extract old logic"

worker_v3_code = """
const ADMIN_SECRET = "7789";

function jsonResponse(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...headers, "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET,POST,OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }
  });
}

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
};

// CSV Escaper
function esc(str) {
  if (str === null || str === undefined) return '""';
  const s = String(str);
  if (s.includes('"') || s.includes(',') || s.includes('\\n')) {
    return '"' + s.replace(/"/g, '""') + '"';
  }
  return '"' + s + '"';
}

function calcElo(eloA, eloB, actualScoreA, kFactor = 32) {
  const expectedA = 1 / (1 + Math.pow(10, (eloB - eloA) / 400));
  return Math.round(eloA + kFactor * (actualScoreA - expectedA));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    try {
      // --- 1. DB CSV ENDPOINTS (Replacements for Google Sheets CSV export) ---
      if (url.pathname === "/api/students.csv" && request.method === "GET") {
        const stuStr = await env.LICENSES.get("DB_STUDENTS");
        const students = JSON.parse(stuStr || "[]");
        let csv = "id,cnName,enName,gender,age,school,level,feeMode,payStatus,comboExpiry,whatsapp,elo,tier,password\\n";
        for (const s of students) {
          csv += `${esc(s.id)},${esc(s.cnName)},${esc(s.enName)},${esc(s.gender)},${esc(s.age)},${esc(s.school)},${esc(s.level)},${esc(s.feeMode)},${esc(s.payStatus)},${esc(s.comboExpiry)},${esc(s.whatsapp)},${esc(s.elo)},${esc(s.tier)},${esc(s.password)}\\n`;
        }
        return new Response(csv, { headers: { ...corsHeaders, "Content-Type": "text/csv; charset=utf-8" } });
      }

      if (url.pathname === "/api/matches.csv" && request.method === "GET") {
        const matStr = await env.LICENSES.get("DB_MATCHES");
        const matches = JSON.parse(matStr || "[]");
        let csv = "date,round,redId,redName,result,blackId,blackName,verdict,recordImg,xqfFile\\n";
        for (const m of matches) {
          csv += `${esc(m.date)},${esc(m.round)},${esc(m.redId)},${esc(m.redName)},${esc(m.result)},${esc(m.blackId)},${esc(m.blackName)},${esc(m.verdict)},${esc(m.recordImg)},${esc(m.xqfFile)}\\n`;
        }
        return new Response(csv, { headers: { ...corsHeaders, "Content-Type": "text/csv; charset=utf-8" } });
      }

      // --- 2. DB ACTION ENDPOINT (Replacement for Code.gs doPost) ---
      if (url.pathname === "/api/action" && request.method === "POST") {
        const payload = await request.json();
        const action = payload.action;

        let students = JSON.parse(await env.LICENSES.get("DB_STUDENTS") || "[]");
        let matches = JSON.parse(await env.LICENSES.get("DB_MATCHES") || "[]");

        if (action === "addMatch") {
          const redName = payload.redName;
          const blackName = payload.blackName;
          const result = payload.result;
          
          let sRed = students.find(s => s.cnName === redName);
          let sBlack = students.find(s => s.cnName === blackName);
          if (!sRed || !sBlack) return jsonResponse({ error: "未找到红方或黑方档案" }, 400, corsHeaders);

          let k = payload.delta ? parseInt(payload.delta) : 32;
          let eloRed = parseInt(sRed.elo) || 200;
          let eloBlack = parseInt(sBlack.elo) || 200;

          let scoreRed = 0.5, scoreBlack = 0.5;
          if (result === "🔴 红胜") { scoreRed = 1; scoreBlack = 0; }
          else if (result === "⚫ 黑胜") { scoreRed = 0; scoreBlack = 1; }

          let newRed = calcElo(eloRed, eloBlack, scoreRed, k);
          let newBlack = calcElo(eloBlack, eloRed, scoreBlack, k);

          sRed.elo = newRed;
          sBlack.elo = newBlack;

          matches.push({
            date: payload.date, round: payload.round,
            redId: sRed.id, redName: redName,
            result: result,
            blackId: sBlack.id, blackName: blackName,
            verdict: payload.verdict || "", recordImg: "", xqfFile: ""
          });

          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          await env.LICENSES.put("DB_MATCHES", JSON.stringify(matches));
          return jsonResponse({ success: true, message: "对局录入成功！" }, 200, corsHeaders);
        }

        if (action === "deleteMatch") {
          const idx = matches.findIndex(m => m.date === payload.date && m.round === payload.round && m.redName === payload.redName && m.blackName === payload.blackName);
          if (idx === -1) return jsonResponse({ error: "对局未找到" }, 404, corsHeaders);
          
          // ELO Rollback Logic!
          const m = matches[idx];
          let sRed = students.find(s => s.cnName === m.redName);
          let sBlack = students.find(s => s.cnName === m.blackName);
          
          if (sRed && sBlack) {
             let k = 32;
             let eloRed = parseInt(sRed.elo) || 200;
             let eloBlack = parseInt(sBlack.elo) || 200;
             let scoreRed = 0.5, scoreBlack = 0.5;
             if (m.result === "🔴 红胜") { scoreRed = 1; scoreBlack = 0; }
             else if (m.result === "⚫ 黑胜") { scoreRed = 0; scoreBlack = 1; }
             
             // Approximate rollback (reverse the k factor delta)
             const expectedRed = 1 / (1 + Math.pow(10, (eloBlack - eloRed) / 400));
             const expectedBlack = 1 / (1 + Math.pow(10, (eloRed - eloBlack) / 400));
             
             sRed.elo = Math.round(eloRed - k * (scoreRed - expectedRed));
             sBlack.elo = Math.round(eloBlack - k * (scoreBlack - expectedBlack));
          }

          matches.splice(idx, 1);
          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          await env.LICENSES.put("DB_MATCHES", JSON.stringify(matches));
          return jsonResponse({ success: true, message: "对局已删除，ELO已回滚！" }, 200, corsHeaders);
        }

        if (action === "addStudent") {
          const nextId = "XQB-" + String(students.length + 1).padStart(3, '0');
          students.push({
            id: nextId, cnName: payload.cnName, enName: payload.enName,
            gender: payload.gender, age: payload.age, school: payload.school,
            level: payload.level, feeMode: payload.feeMode, payStatus: "⏳ 待核实",
            comboExpiry: "", whatsapp: payload.whatsapp, elo: 200,
            tier: "🏅 待定等级", password: payload.password
          });
          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          return jsonResponse({ success: true, message: "学员档案创建成功！" }, 200, corsHeaders);
        }

        if (action === "updateAccount") {
          let s = students.find(s => s.id === payload.studentId);
          if(s) {
            if(payload.newName) s.cnName = payload.newName;
            if(payload.newPwd) s.password = payload.newPwd;
            if(payload.newLevel) s.level = payload.newLevel;
            await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          }
          return jsonResponse({ success: true, message: "账号更新成功！" }, 200, corsHeaders);
        }

        if (action === "changePassword") {
          let s = students.find(s => s.id === payload.studentId);
          if(!s || s.password !== payload.oldPassword) return jsonResponse({ error: "旧密码错误" }, 400, corsHeaders);
          s.password = payload.newPassword;
          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          return jsonResponse({ success: true, message: "密码修改成功！" }, 200, corsHeaders);
        }

        if (action === "updatePayment") {
          let s = students.find(s => s.id === payload.studentId);
          if(s) {
            s.payStatus = "已缴费 (Verified)";
            if(payload.expiryStr) s.comboExpiry = payload.expiryStr;
            await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          }
          return jsonResponse({ success: true, message: "缴费状态更新成功！" }, 200, corsHeaders);
        }

        if (action === "deleteStudent") {
          students = students.filter(s => s.id !== payload.studentId);
          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          return jsonResponse({ success: true, message: "学员已注销！" }, 200, corsHeaders);
        }

        if (action === "clearTestData") {
          await env.LICENSES.put("DB_MATCHES", "[]");
          students.forEach(s => s.elo = 200);
          await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students));
          return jsonResponse({ success: true, message: "测试数据已清空，ELO已重置！" }, 200, corsHeaders);
        }

        if (action === "saveFileUrl") {
          const type = payload.type;
          if (type === "receipt") {
             let s = students.find(s => s.id === payload.studentId);
             if (s) { s.payStatus = `⏳ 待核实|${payload.url}`; await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students)); }
          } else if (type === "matchPhoto" || type === "matchXQF") {
             const idx = matches.findIndex(m => m.date === payload.date && m.round === payload.round && m.redName === payload.redName && m.blackName === payload.blackName);
             if (idx !== -1) {
               if(type === "matchPhoto") matches[idx].recordImg = payload.url;
               if(type === "matchXQF") matches[idx].xqfFile = payload.url;
               await env.LICENSES.put("DB_MATCHES", JSON.stringify(matches));
             }
          }
          return jsonResponse({ success: true, message: "文件链接已保存！" }, 200, corsHeaders);
        }

        return jsonResponse({ error: "未知操作: " + action }, 400, corsHeaders);
      }

      // --- 3. EXISTING WORKER LOGIC ---
""" + old_logic + """
      return jsonResponse({ status: "ok", msg: "Club XiangQi Bera Worker v3.0 (KV DB) is Running" }, 200, corsHeaders);
    } catch (err) {
      return jsonResponse({ error: err.toString() }, 500, corsHeaders);
    }
  }
};
"""

with io.open('../worker_v3.js', 'w', encoding='utf-8') as f:
    f.write(worker_v3_code)

print("worker_v3.js built.")
