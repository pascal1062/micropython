import uasyncio as asyncio

#fonction basique
async def simple_print(msg):
    print(msg)

#si on apelle cette fonction avec tout simplement:
simple_print('Hello')
  <generator object 'simple' at 3ffe5f40>
#ça retourne pas de résulat! ça retourne l'objet seulement ***un objet coroutine***

#pour exécuter il faut faire:
await simple_print('Hello') ***attention marche pas en repl...doit être dans une fonction***
OU
asyncio.run(simple_print('Hello')) ***ça marche....***
OU
loop = asyncio.new_event_loop()
loop.run_until_complete(simple_print('Hello'))
#aussi loop.run_forever....
