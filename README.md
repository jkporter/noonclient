# NoonClient

A Python client for Noon Lighting System.

## Sample Usage
```Python
import asyncio
from typing import Tuple
from noonclient import NoonClient
from noonclient.alaska.model import NoonLine, NoonChange, NoonSpace

async def main():
    async with NoonClient("example@example.com", "<password>") as client:
        model = await client.fetch_model()
        lines = dict[str, Tuple[NoonSpace, NoonLine]]()

        def line_change(change: NoonChange) -> None:
            if change.guid not in lines:
                return
                
            space, line = lines[change.guid]
            for field in change.fields:
                setattr(line, field.name, field.value)
            print('{} - {}: {}, level: {}%'.format(space.name, line.display_name, line.line_state, line.dimming_level))

        for space in model.leases[0].structure.spaces:
            print(space.name)
            for line in space.lines:
                lines[line.guid] = (space, line)
                print('    {}: {}, level: {}%'.format(line.display_name, line.line_state, line.dimming_level))
            print()

        print('Listening for changes...')
        print()
        async for change in client.listen():
            line_change(change)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_until_complete(asyncio.sleep(1))
loop.close()
```