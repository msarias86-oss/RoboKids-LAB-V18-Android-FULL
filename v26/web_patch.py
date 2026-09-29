from pathlib import Path

p=Path("app/src/main/assets/public/index.html")
h=p.read_text(encoding="utf-8")

# Version labels/storage
h=h.replace("V24","V26")
h=h.replace("rk_v20_","rk_v26_")

# V26 response display: each correct participant contributes +100
start=h.find("function responseTable(s){")
end=h.find("function studentUrl(",start)
if start<0 or end<0:
    raise SystemExit("No se encontró responseTable")
resp="""function responseTable(s){var q=s.question||{options:[]};return '<div class="teamAnswerGrid">'+s.teams.map(function(t){var r=(s.responses||{})[t.id]||{};var total=Number(r.total||0);var ok=Number(r.correctCount||0);var bad=Number(r.incorrectCount||0);var pts=Number(r.points||0);var label=total?total+' respuesta'+(total===1?'':'s'):'Sin respuesta';var detail=s.revealed&&total?' · '+ok+' correcta'+(ok===1?'':'s')+' · '+bad+' incorrecta'+(bad===1?'':'s')+' · +'+pts+' pts':'';var cls='empty';if(s.revealed&&total){cls=ok===0?'wrong':(bad===0?'correct':'partial');}return '<div class="answerTeam '+cls+'"><b>'+t.emoji+' '+RK.esc(t.name)+'</b><span>'+RK.esc(label)+detail+'</span></div>';}).join('')+'</div>';}
"""
h=h[:start]+resp+h[end:]

# Biblioteca docente mobile
library_css="""/* V26 · Biblioteca docente móvil */
.libraryHero{background:linear-gradient(135deg,#eef7ff,#f5f0ff);border:1px solid #cdddf7;border-radius:22px;padding:18px}
.libraryHeroTop{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.libraryHeroTop h3{margin:0 0 6px}.libraryHeroTop p{margin:0;color:#62709a}
.libraryQuick{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:14px}
.libraryQuickBox{background:#fff;border:1px solid #dbe5f4;border-radius:16px;padding:12px;display:grid;gap:5px}
.libraryResources{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:14px}
.libraryResource{background:#fff;border:1px solid #dbe5f4;border-radius:16px;padding:13px}
.libraryResource.primary{border:2px solid #79aefc}.libraryResource h4{margin:7px 0}.libraryResource p{font-size:14px;color:#62709a}
.libraryResource .tag{display:inline-block;padding:4px 8px;border-radius:999px;background:#e8f1ff;color:#1f5eaa;font-size:12px;font-weight:800}
.answerTeam.partial{background:#fff6d9;border-color:#f0c85c}
@media(max-width:1000px){.libraryResources{grid-template-columns:repeat(2,1fr)}.libraryQuick{grid-template-columns:1fr}}
@media(max-width:620px){.libraryResources{grid-template-columns:1fr}}
"""
if "V26 · Biblioteca docente móvil" not in h:
    h=h.replace("</style>",library_css+"\n</style>",1)

teacher_lib="""function teacherLibrary(){return '<div class="libraryHero">'+
  '<div class="libraryHeroTop"><div><h3>📚 Biblioteca docente · Nivel 1 · 7 a 9 años</h3><p>Guía y material de apoyo para planificar y orientar las clases de robótica con ACECode, QD001, QD007, QD020 y ESP32.</p></div><a class="btn purple" href="/biblioteca.html" target="_blank" rel="noopener">Abrir biblioteca completa →</a></div>'+
  '<div class="libraryQuick"><div class="libraryQuickBox"><b>🎯 Enfoque pedagógico</b><span class="muted">Aprender jugando, experimentar, corregir y explicar lo realizado.</span></div><div class="libraryQuickBox"><b>🕒 Plan orientativo</b><span class="muted">8 a 12 clases de 45 a 60 minutos.</span></div><div class="libraryQuickBox"><b>🧩 Ruta de aprendizaje</b><span class="muted">Bloques, movimiento, repeticiones, condicionales, sensores, línea y proyecto final.</span></div></div>'+
  '<div class="libraryResources">'+
    '<div class="libraryResource primary"><div class="tag">Guía principal</div><h4>Manual Docente de Estudios · Nivel 1</h4><p>Secuencia didáctica para niños y niñas de 7 a 9 años.</p></div>'+
    '<div class="libraryResource"><div class="tag">Manual técnico</div><h4>Carro Inteligente ESP32</h4><p>Montaje, programación y escenarios de práctica.</p></div>'+
    '<div class="libraryResource"><div class="tag">Instalación</div><h4>ESP32 en Arduino IDE</h4><p>Instalación del soporte ESP32 y resolución de problemas.</p></div>'+
    '<div class="libraryResource"><div class="tag">Tutorial</div><h4>ACECode para Windows</h4><p>Instalación, conexión, puerto serie y modos de trabajo.</p></div>'+
  '</div></div>';}
"""
if "function teacherLibrary()" not in h:
    pos=h.find("function teacherView(){")
    if pos<0: raise SystemExit("No se encontró teacherView")
    h=h[:pos]+teacher_lib+h[pos:]

# Add library before room exists
old="return RK.brand('Profesor')+'<div class="hero"><small>V26 · Internet + datos móviles + Wi‑Fi</small><h1>Panel del profesor</h1><p>Servidor multidispositivo con acceso LAN o Internet HTTPS.</p></div><div class="card"><h3>Nueva clase</h3><button class="btn" data-ui="create-room">Crear sala</button>'+(roomCode?'<p class="muted">Intentando recuperar sala '+RK.esc(roomCode)+'…</p>':'')+'</div>';"
new="return RK.brand('Profesor')+'<div class="hero"><small>V26 · Android · Wi‑Fi / LAN</small><h1>Panel del profesor</h1><p>Servidor multidispositivo integrado en Android.</p></div><div class="card"><h3>Nueva clase</h3><button class="btn" data-ui="create-room">Crear sala</button>'+(roomCode?'<p class="muted">Intentando recuperar sala '+RK.esc(roomCode)+'…</p>':'')+'</div><div style="margin-top:16px">'+teacherLibrary()+'</div>';"
h=h.replace(old,new,1)

# Add library after mission/turn in active room
needle="""    '<div class="card"><h3>Misión y turno</h3><div class="teacherMissionGrid"><div><label class="muted">Misión</label><select id="missionSelect" class="select">'+missionOpts+'</select></div><div><label class="muted">Equipo en turno físico</label><select id="turnSelect" class="select">'+turnOpts+'</select></div></div><p class="muted" style="margin:10px 0 0">Experiencia activa: <b>'+RK.esc(s.experienceName||'')+'</b></p></div>'+"""
if needle in h and "teacherLibrary()+\n    '<div class="card"><h3>Cartas / pistas" not in h:
    h=h.replace(needle,needle+"\n    teacherLibrary()+",1)

# Explain V26 individual scoring on teacher panel
qneedle="""    '<div class="card"><h3>Pregunta y respuestas</h3>'+RK.question(s.question,null,false)+'<div style="margin-top:14px">'+responseTable(s)+'</div></div>'+"""
qnew="""    '<div class="card"><h3>Pregunta y respuestas</h3><p class="muted">Puntaje V26: cada respuesta correcta suma <b>+100 puntos</b> al equipo del alumno. Las respuestas incorrectas no suman.</p>'+RK.question(s.question,null,false)+'<div style="margin-top:14px">'+responseTable(s)+'</div></div>'+"""
h=h.replace(qneedle,qnew,1)

p.write_text(h,encoding="utf-8")

# Biblioteca móvil offline (contenido de orientación integrado)
b=Path("app/src/main/assets/public/biblioteca.html")
b.write_text("""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Biblioteca Docente · RoboKids LAB V26</title>
<style>body{font-family:Arial,sans-serif;margin:0;background:#f4f8ff;color:#0c285b}.wrap{max-width:1100px;margin:auto;padding:22px}.hero{background:linear-gradient(135deg,#2e6ef7,#8247ef);color:white;padding:24px;border-radius:22px}.card{background:#fff;border:1px solid #dbe5f4;border-radius:18px;padding:18px;margin-top:15px;box-shadow:0 8px 22px #23406c18}.tag{display:inline-block;background:#e8f1ff;color:#1c5aa6;border-radius:999px;padding:5px 9px;font-weight:700;font-size:12px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.btn{display:inline-block;background:#2f74ff;color:white;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:700}.muted{color:#66749a}.topic{padding:8px 0;border-bottom:1px solid #edf1f7}.topic:last-child{border-bottom:0}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style></head>
<body><div class="wrap"><div class="hero"><h1>📚 Biblioteca Docente · Nivel 1</h1><p>Guía móvil de orientación para clases de RoboKids LAB con niños y niñas de 7 a 9 años.</p></div>
<div class="card" id="manual-docente"><span class="tag">Guía principal · 7 a 9 años</span><h2>Manual Docente de Estudios · Nivel 1</h2><p>El enfoque es aprender jugando: explicar una idea, programarla con bloques, probarla físicamente, observar el resultado, corregir y finalmente explicar lo aprendido.</p><p><b>Plan orientativo:</b> 8 a 12 clases de 45 a 60 minutos.</p><div class="grid"><div><h3>Ruta de aprendizaje</h3><div class="topic">1. Objetivo del manual</div><div class="topic">2. Materiales y preparación</div><div class="topic">3. Conocer ACECode</div><div class="topic">4. Conectar ACEBOTT QD001</div><div class="topic">5. Primer programa</div><div class="topic">6. Secuencias y movimientos</div></div><div><h3>Continuación</h3><div class="topic">7. Repeticiones y velocidad</div><div class="topic">8. Condicionales</div><div class="topic">9. Sensor ultrasónico</div><div class="topic">10. Seguidor de línea</div><div class="topic">11. Proyecto final</div><div class="topic">12. Evaluación y cierre</div></div></div><h3>Orientación docente</h3><p>Trabajar en parejas o equipos de tres. Asignar roles de programador, observador y responsable del robot. Antes de encender el equipo verificar batería, cable USB, pista, obstáculos y espacio seguro. Promover preguntas simples, demostración corporal y pruebas cortas.</p></div>
<div class="card" id="carro"><span class="tag">Manual técnico</span><h2>Carro Inteligente ESP32</h2><p>Material de apoyo para el kit QD001 y sus prácticas. La progresión abarca montaje del coche, movimientos básicos, luces y buzzer, evitación de obstáculos, patrulla/seguidor de línea y distintas formas de control.</p><p class="muted">Usar este material como referencia técnica complementaria a las misiones de la plataforma.</p></div>
<div class="card" id="arduino"><span class="tag">Instalación</span><h2>ESP32 en Arduino IDE</h2><p><b>Objetivo:</b> instalar el soporte ESP32 para seleccionar placas y cargar programas.</p><div class="topic">1. Instalar Arduino IDE.</div><div class="topic">2. Abrir Preferences y configurar el gestor de placas.</div><div class="topic">3. Abrir Boards Manager, buscar ESP32 e instalar.</div><div class="topic">4. Reiniciar el IDE y verificar Tools → Board.</div><div class="topic">5. Verificar puerto USB, placa seleccionada y compilación de prueba.</div><p><b>Si falla:</b> revisar conexión, permisos, firewall, cable USB de datos, drivers y versión del paquete ESP32.</p></div>
<div class="card" id="acecode"><span class="tag">Tutorial</span><h2>ACECode para Windows</h2><p>ACECode permite programar mediante bloques gráficos tipo Scratch e incorpora control de robots.</p><div class="topic">Instalar ACECode desde el sitio oficial.</div><div class="topic">Instalar/controlar el driver del puerto serie.</div><div class="topic">Conectar la placa ESP32 por USB y verificar el puerto.</div><div class="topic">Usar modo en línea para depuración o modo de carga para ejecutar el programa desde la placa.</div><p><a class="btn" href="https://acebott.com/acecode/" target="_blank" rel="noopener">Abrir ACECode →</a></p></div>
<div class="card"><h2>Consejo de uso en clase</h2><p>Antes de cada misión: explicar el objetivo en una frase, demostrar físicamente el movimiento, pedir que los alumnos predigan qué ocurrirá, programar con pocos bloques y probar. Después de la prueba, modificar una sola variable por vez.</p></div>
</div></body></html>""",encoding="utf-8")

print("V26 Android web/library patched")
