import asyncio
import websockets
import pymorphy2

async def server(websocket, path):
    print("Client connected")

    async for message in websocket:
        print(f"Received word: {message}")
        
        word = message.strip()  # Assuming only a single word is sent
        
        if word:
            morph = pymorphy2.MorphAnalyzer()
            parsed_word = morph.parse(word)
            
            # Constructing the output with each interpretation on a new line
            output = "\n".join([f"{result.normal_form} {result.tag}" for result in parsed_word])
            
            if not output:
                output = "No interpretations found for the word."

        else:
            output = "No word received."

        await websocket.send(output)
        print(f"Sent: {output}")

start_server = websockets.serve(server, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
