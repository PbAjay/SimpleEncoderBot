async def parse_progress(pipe):
    block = {}

    async for raw in pipe:
        line = raw.decode().strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        block[key] = value

        if key == "progress":
            yield block
            block = {}
