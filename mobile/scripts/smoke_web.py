"""Smoke público real con Chrome headless existente; sin proveedores ni credenciales."""
import asyncio
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen
from uuid import uuid4
import websockets

ROOT = Path(__file__).resolve().parents[2]
CHROME = Path(os.environ.get("CHROME_BIN", "C:/Program Files/Google/Chrome/Application/chrome.exe"))
OPTIONS = argparse.ArgumentParser(description="Prueba de navegación pública sin Supabase configurado.")
OPTIONS.add_argument("--url", default="http://127.0.0.1:8766")
OPTIONS.add_argument("--timeout", type=int, default=60)
ARGS = OPTIONS.parse_args()
URL = ARGS.url

async def main():
    profile = ROOT / ".browser-smoke" / ("cdp-" + uuid4().hex)
    profile.mkdir(parents=True)
    process = subprocess.Popen([str(CHROME), "--headless", "--disable-gpu",
        "--disable-background-networking", "--no-first-run", "--no-default-browser-check",
        "--remote-debugging-port=0", "--user-data-dir=" + str(profile), "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
    report = []
    try:
        active = profile / "DevToolsActivePort"
        for _ in range(100):
            if active.exists(): break
            await asyncio.sleep(.1)
        port = int(active.read_text().splitlines()[0])
        targets = json.load(urlopen(f"http://127.0.0.1:{port}/json", timeout=5))
        target = next(t for t in targets if t["type"]=="page")
        async with websockets.connect(target["webSocketDebuggerUrl"]) as socket:
            serial = 0
            async def command(method, params=None):
                nonlocal serial
                serial += 1
                current = serial
                await socket.send(json.dumps({"id":current,"method":method,"params":params or {}}))
                while True:
                    result = json.loads(await socket.recv())
                    if result.get("id")==current:
                        if "error" in result: raise RuntimeError(str(result["error"]))
                        return result.get("result",{})
            async def evaluate(source):
                result = await command("Runtime.evaluate", {"expression":source,"returnByValue":True})
                if "exceptionDetails" in result: raise RuntimeError(str(result["exceptionDetails"]))
                return result["result"].get("value")
            async def text_contains(text):
                for _ in range(ARGS.timeout * 10):
                    if await evaluate("document.body.innerText.includes("+json.dumps(text)+")"): return
                    await asyncio.sleep(.1)
                raise AssertionError("No se encontró: "+text)
            async def click(label):
                found = await evaluate("(()=>{const button=[...document.querySelectorAll('[role=button]')].find(b=>b.textContent==="+json.dumps(label)+");if(button){button.click();return true;}return false;})()")
                assert found, label
            await command("Emulation.setDeviceMetricsOverride", {"width":390,"height":844,"deviceScaleFactor":1,"mobile":True})
            await command("Page.navigate", {"url":URL})
            await text_contains("Descubre por dónde se va tu plata.")
            await text_contains("Registrarse")
            assert await evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "Desbordamiento horizontal"
            await asyncio.sleep(.3)
            screenshot = await command("Page.captureScreenshot", {"format":"png","captureBeyondViewport":False})
            (ROOT/"mobile/docs/public-smoke.png").write_bytes(base64.b64decode(screenshot["data"]))
            report.append("Bienvenida pública renderizada a 390×844 sin desbordamiento")
            await click("Registrarse")
            await text_contains("Confirmar contraseña")
            await click("Registrarse")
            await text_contains("El servicio de acceso no está disponible en este entorno.")
            report.append("Registro muestra indisponibilidad explícita sin configuración, sin simular cuenta")
            await click("Volver al inicio")
            await click("Iniciar sesión")
            await text_contains("Olvidé mi contraseña")
            await click("Olvidé mi contraseña")
            await text_contains("Recupera tu acceso")
            report.append("Navegación real a login y recuperación")
            await click("Volver al inicio")
            await text_contains("Descubre por dónde se va tu plata.")
            report.append("Regreso a pantalla pública")
            (ROOT/"mobile/docs/smoke-web.json").write_text(json.dumps({"url":URL,"passed":report,"scope":"Solo pantalla pública y ausencia de configuración; sin Supabase real."},ensure_ascii=False,indent=2),encoding="utf-8")
            print(json.dumps({"passed":report},ensure_ascii=False))
            await command("Browser.close")
    finally:
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.terminate()

if __name__=="__main__":
    asyncio.run(main())
