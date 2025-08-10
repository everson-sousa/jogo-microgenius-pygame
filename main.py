import asyncio

print("[DEBUG] main.py EXECUTADO") # <-- ADICIONE ESTA LINHA

# O ideal é importar o app.py aqui dentro, não no topo
# from app import game_loop 

async def main():
    print("[DEBUG] Entrando na função main()") # <-- ADICIONE ESTA LINHA
    from app import game_loop # Importa a função principal do seu arquivo app.py
    game_loop()
    print("[DEBUG] Saindo da função main()") # <-- ADICIONE ESTA LINHA


# Inicia a função main
if __name__ == "__main__":
    print("[DEBUG] Bloco __main__ alcançado") # <-- ADICIONE ESTA LINHA
    asyncio.run(main())