import os
from aiohttp import web

async def start_keepalive():
    port = int(os.environ.get("PORT", 10000))

    async def handle(request):
        return web.Response(text="OK")

    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"[KeepAlive] Listening on port {port}")
