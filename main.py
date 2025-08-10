# Arquivo: main.py
import asyncio
from app import game_loop # Importa sua função principal do seu arquivo app.py

# O Pygbag precisa de uma função assíncrona 'main' para iniciar
async def main():
    game_loop()

# Inicia a função main
if __name__ == "__main__":
    asyncio.run(main())