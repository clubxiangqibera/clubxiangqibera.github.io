import io

with io.open('../worker_v3.js', 'r', encoding='utf-8') as f:
    text = f.read()

proxy_logic = """
        if (["uploadReceipt", "updateMatchPhoto", "updateMatchXQF", "uploadEventPhoto"].includes(action)) {
           const gasUploadUrl = "https://script.google.com/macros/s/AKfycbyFY__BC0NXW87ZK1okkzhlskQ4PPBJx2QEXf0-8Icv8tbFHZcRSVge60TqU11DU4v_/exec";
           const gasRes = await fetch(gasUploadUrl, { method: "POST", body: JSON.stringify(payload) });
           const gasData = await gasRes.json();
           if (!gasData.success) return jsonResponse({ error: gasData.error || gasData.message }, 500, corsHeaders);

           const url = gasData.url;
           
           if (action === "uploadReceipt") {
             let s = students.find(s => s.id === payload.studentId);
             if (s) { s.payStatus = `⏳ 待核实|${url}`; await env.LICENSES.put("DB_STUDENTS", JSON.stringify(students)); }
           } else if (action === "updateMatchPhoto" || action === "updateMatchXQF") {
             const idx = matches.findIndex(m => m.date === payload.date && m.round === payload.round && m.redName === payload.redName && m.blackName === payload.blackName);
             if (idx !== -1) {
               if(action === "updateMatchPhoto") matches[idx].recordImg = url;
               if(action === "updateMatchXQF") matches[idx].xqfFile = url;
               await env.LICENSES.put("DB_MATCHES", JSON.stringify(matches));
             }
           }
           return jsonResponse({ success: true, url: url, message: "文件上传并保存成功！" }, 200, corsHeaders);
        }
"""

text = text.replace('if (action === "uploadReceiptData") {', proxy_logic + '\n        if (action === "uploadReceiptData") {')

with io.open('../worker_v3.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("worker proxy logic added")
