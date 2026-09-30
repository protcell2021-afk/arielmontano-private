from flask import Flask, request, send_from_directory, send_file
import os, glob, datetime, urllib.parse
app = Flask(__name__)
CARPETA = "/sdcard/MONTANO"
CLAVE = "ARM2027"
BASE = os.path.expanduser("~/universidad-offline")
STATIC_DIR = os.path.join(BASE, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

LOGIN = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');*{font-family:Inter,sans-serif}body{margin:0;min-height:100vh;background:radial-gradient(1200px at 10% 10%,#1e3a8a 0%,#0f172a 50%,#020617 100%);display:flex;align-items:center;justify-content:center;color:white}.card{width:90%;max-width:400px;background:rgba(255,255,255,0.06);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);padding:40px;border-radius:32px;text-align:center}.avatar{width:110px;height:110px;border-radius:30px;object-fit:cover;margin:0 auto 20px;display:block}.subtitle{opacity:.6;letter-spacing:3px;font-size:11px;margin:8px 0 30px}input{width:100%;padding:16px;border-radius:16px;border:1px solid rgba(255,255,255,.1);background:rgba(0,0,0,.3);color:white;box-sizing:border-box}button{width:100%;margin-top:16px;padding:16px;border-radius:16px;border:none;background:linear-gradient(135deg,#3b82f6,#2563eb);color:white;font-weight:800}</style></head><body><div class='card'><img src='/avatar' class='avatar'><h1>ARMONTANO</h1><div class='subtitle'>PRIVATE CLOUD</div><form method='post'><input type='password' name='clave' placeholder='Clave'><button>ACCEDER</button></form></div></body></html>"

HEAD = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');*{font-family:Inter,sans-serif}body{margin:0;background:#f1f5f9;padding-bottom:90px}.top{background:#0f172a;color:white;padding:18px 20px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}.top-left{display:flex;align-items:center;gap:12px}.top-left img{width:42px;height:42px;border-radius:12px;object-fit:cover;border:1px solid #3b82f6}.stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;padding:15px}.stat{background:white;border-radius:18px;padding:16px;box-shadow:0 2px 10px rgba(0,0,0,.05)}.upload{background:white;margin:0 15px 15px;border-radius:20px;padding:20px;display:flex;gap:10px;align-items:center;border:2px dashed #cbd5e1}.file-grid{padding:0 15px;display:grid;gap:10px}.file{background:white;border-radius:18px;padding:16px;display:flex;justify-content:space-between;align-items:center}.actions{display:flex;gap:6px}.btn{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;text-decoration:none;color:white;font-size:16px}.btn-dl{background:#f1f5f9;color:#0f172a}.btn-wa{background:#25D366}.btn-fb{background:#1877F2}.btn-tg{background:#26A5E4}.share-bar{position:fixed;bottom:0;left:0;right:0;background:rgba(15,23,42,.95);backdrop-filter:blur(20px);padding:12px 15px;display:flex;justify-content:space-between;align-items:center;color:white;z-index:20}.share-btns{display:flex;gap:8px}.share-btns a{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;text-decoration:none;font-size:20px}</style></head><body>"

@app.route("/", methods=["GET","POST"])
def index():
    if request.form.get("clave")==CLAVE or request.args.get("auth")==CLAVE:
        try: archivos=[f for f in os.listdir(CARPETA) if os.path.isfile(os.path.join(CARPETA,f))]
        except: archivos=[]
        hora=datetime.datetime.now().strftime("%H:%M")
        host=request.host_url.rstrip('/')
        base_share=f"{host}/?auth={CLAVE}"
        enc_base=urllib.parse.quote_plus(f"Entra a mi nube ARMONTANO: {base_share}")
        files_html=""
        for f in archivos:
            file_url=f"{host}/compartido/{urllib.parse.quote(f)}"
            text=urllib.parse.quote_plus(f"Mira {f}: {file_url}")
            files_html+=f"<div class='file'><div><div style='font-weight:600'>{f}</div><small style='opacity:.5'>MONTANO / {f}</small></div><div class='actions'><a class='btn btn-dl' href='/compartido/{urllib.parse.quote(f)}' download><i class='fa-solid fa-download'></i></a><a class='btn btn-wa' href='https://wa.me/?text={text}' target='_blank'><i class='fa-brands fa-whatsapp'></i></a><a class='btn btn-fb' href='https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote_plus(file_url)}' target='_blank'><i class='fa-brands fa-facebook-f'></i></a><a class='btn btn-tg' href='https://t.me/share/url?url={urllib.parse.quote_plus(file_url)}&text={urllib.parse.quote_plus(f)}' target='_blank'><i class='fa-brands fa-telegram'></i></a></div></div>"
        html=HEAD+f"<div class='top'><div class='top-left'><img src='/avatar'><div><h2 style='margin:0;letter-spacing:2px'>ARMONTANO</h2><small style='opacity:.6'>{hora} - {len(archivos)} archivos</small></div></div><small style='background:#10b981;padding:4px 10px;border-radius:20px;font-size:10px'>LIVE</small></div><div class='stats'><div class='stat'><b>{len(archivos)}</b><small>ARCHIVOS</small></div><div class='stat'><b style='color:#3b82f6'>100%</b><small>SEGURO</small></div><div class='stat'><b style='color:#10b981'>ON</b><small>SERVIDOR</small></div></div><form class='upload' method='post' enctype='multipart/form-data' action='/subir'><b>Subir:</b><input type='file' name='file' required style='flex:1'><button style='background:#0f172a;color:white;border:none;padding:12px 20px;border-radius:12px;font-weight:700'>SUBIR</button></form><div class='file-grid'>{files_html}</div><div class='share-bar'><div><b>Compartir mi nube</b><br><small style='opacity:.6'>Invita con un toque</small></div><div class='share-btns'><a style='background:#25D366' href='https://wa.me/?text={enc_base}' target='_blank'><i class='fa-brands fa-whatsapp'></i></a><a style='background:#1877F2' href='https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote_plus(base_share)}' target='_blank'><i class='fa-brands fa-facebook-f'></i></a><a style='background:#26A5E4' href='https://t.me/share/url?url={urllib.parse.quote_plus(base_share)}&text=Mi%20nube%20ARMONTANO' target='_blank'><i class='fa-brands fa-telegram'></i></a></div></div></body></html>"
        return html
    return LOGIN

@app.route("/avatar")
def avatar():
    files=glob.glob(os.path.join(STATIC_DIR,"*"))
    return send_file(files[0]) if files else ("",404)

@app.route("/compartido/<path:n>")
def files_route(n): return send_from_directory(CARPETA, n)

@app.route("/subir", methods=["POST"])
def subir():
    f=request.files["file"]; f.save(os.path.join(CARPETA, f.filename))
    return f"<script>location='/?auth={CLAVE}'</script>"

import os
port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port)
