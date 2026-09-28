from pathlib import Path

p = Path("app/src/main/assets/public/index.html")
h = p.read_text(encoding="utf-8")

h = h.replace("RoboKids LAB · Nivel 1 · V20 Multidispositivo", "RoboKids LAB · Nivel 1 · V23 Multidispositivo")
h = h.replace(" · ACEBOTT ESP32 MAX V1.0", "")

marker = "  brand:function(title){return "
if "experienceControl:function" not in h:
    helper = """  experienceControl:function(){var s=RK.state||{};if(RK.role==='teacher'&&s.experienceOptions&&s.experienceOptions.length){var opts=s.experienceOptions.map(function(x){var label=x.id==='spider'?'🕷️ Araña inteligente · QD020':'🤖🚗 Coche inteligente + brazo · QD001 + QD007';return '<option value="'+RK.esc(x.id)+'" '+(s.experienceId===x.id?'selected':'')+'>'+RK.esc(label)+'</option>';}).join('');return '<label class="connection" style="display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);padding:8px 10px;border-radius:14px"><b>Experiencia</b><select id="experienceSelect" class="select" style="min-width:330px;padding:8px 10px">'+opts+'</select></label>';}if(s.experienceName){return '<div class="connection">'+RK.esc(s.experienceId==='spider'?'🕷️ Araña inteligente · QD020':'🤖🚗 Coche inteligente + brazo · QD001 + QD007')+'</div>';}return '';},
"""
    i = h.find(marker)
    if i < 0:
        raise SystemExit("No se encontró brand:function")
    h = h[:i] + helper + h[i:]

h = h.replace('<div id="conn" class="connection">Servidor local</div>', "'+RK.experienceControl()+'")
h = h.replace(
    '<a class="btn purple" href="?role=screen">Abrir Proyector / TV →</a>',
    '<a class="btn purple" href="?role=screen" target="_blank" rel="noopener">Abrir Proyector / TV →</a>'
)
h = h.replace(
    '<a class="btn pink" href="?role=station">Abrir Estación →</a>',
    '<a class="btn pink" href="https://acebott.com/acecode/" target="_blank" rel="noopener">Abrir Estación →</a>'
)
h = h.replace(
    '<a class="btn pink" href="?access=student&role=station'+qRoom+'">Abrir Estación →</a>',
    '<a class="btn pink" href="https://acebott.com/acecode/" target="_blank" rel="noopener">Abrir Estación →</a>'
)

old = """Array.from({length:s.missionCount||14},function(_,i){return '<option value="'+(i+1)+'" '+(s.missionId===i+1?'selected':'')+'>Misión '+(i+1)+'</option>';}).join('')"""
new = """(s.missionOptions||[]).map(function(m){return '<option value="'+m.id+'" '+(s.missionId===m.id?'selected':'')+'>'+RK.esc(m.title)+'</option>';}).join('')"""
h = h.replace(old, new)

oldchg = """document.addEventListener('change',function(e){if(e.target.id==='missionSelect')action('set-mission',{missionId:Number(e.target.value)});if(e.target.id==='turnSelect')action('set-turn-team',{teamId:e.target.value});});"""
newchg = """document.addEventListener('change',function(e){if(e.target.id==='experienceSelect')action('set-experience',{experienceId:e.target.value});if(e.target.id==='missionSelect')action('set-mission',{missionId:Number(e.target.value)});if(e.target.id==='turnSelect')action('set-turn-team',{teamId:e.target.value});});"""
h = h.replace(oldchg, newchg)

h = h.replace("💾 Cargado al ESP32", "💾 Cargado al robot")
h = h.replace("V20", "V23")

p.write_text(h, encoding="utf-8")
print("V23 Android web UI patched")
