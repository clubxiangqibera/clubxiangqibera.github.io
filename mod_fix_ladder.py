import io

with io.open('../worker_v3.js', 'r', encoding='utf-8') as f:
    text = f.read()

ladder_logic = """
      if (url.pathname === "/api/ladder.csv" && request.method === "GET") {
        const stuStr = await env.LICENSES.get("DB_STUDENTS");
        const matStr = await env.LICENSES.get("DB_MATCHES");
        const students = JSON.parse(stuStr || "[]");
        const matches = JSON.parse(matStr || "[]");
        
        const stats = {};
        for (const s of students) {
           stats[s.cnName] = { w:0, d:0, l:0, total:0, id: s.id, name: s.cnName, school: s.school, tier: s.tier, elo: parseInt(s.elo)||200 };
        }
        for (const m of matches) {
           if(stats[m.redName]) {
              stats[m.redName].total++;
              if(m.result==="🔴 红胜") stats[m.redName].w++;
              else if(m.result==="⚫ 黑胜") stats[m.redName].l++;
              else stats[m.redName].d++;
           }
           if(stats[m.blackName]) {
              stats[m.blackName].total++;
              if(m.result==="⚫ 黑胜") stats[m.blackName].w++;
              else if(m.result==="🔴 红胜") stats[m.blackName].l++;
              else stats[m.blackName].d++;
           }
        }
        const ladder = Object.values(stats).sort((a,b) => b.elo - a.elo);
        let csv = "rank,studentId,name,school,tier,wins,draws,losses,total,elo\\n";
        ladder.forEach((p, i) => {
           csv += `${i+1},${esc(p.id)},${esc(p.name)},${esc(p.school)},${esc(p.tier)},${p.w},${p.d},${p.l},${p.total},${p.elo}\\n`;
        });
        return new Response(csv, { headers: { ...corsHeaders, "Content-Type": "text/csv; charset=utf-8" } });
      }
"""

text = text.replace('      if (url.pathname === "/api/students.csv" && request.method === "GET") {', ladder_logic + '\n      if (url.pathname === "/api/students.csv" && request.method === "GET") {')

with io.open('../worker_v3.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("worker_v3.js ladder logic added")
