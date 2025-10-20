# O Farol do Saber — Godot 4 (Skeleton)

Esqueleto inicial de projeto **Godot 4.x (2D)** para a Game Jam FATEC Campinas 2025.

## Como abrir e executar
1. Abra o **Godot 4.x** e importe esta pasta (`farol_do_saber_godot`).
2. Abra a cena principal: `res://scenes/Main.tscn`.
3. Rode o projeto (F5). Use **← →** para mover e **Enter/Espaço** para pular.

> Dica: O projeto usa as ações padrão `ui_left`, `ui_right` e `ui_accept`, já presentes no Godot.

## O que já está pronto
- **Cena principal** com overlay de escuridão que diminui ao coletar itens.
- **Player (CharacterBody2D)** com movimento lateral e pulo.
- **Itens coletáveis (Area2D)** que disparam sinal `collected`.
- **HUD** com contador e barra de progresso.
- **Chão** simples (StaticBody2D) para testes.

## Próximos passos sugeridos
- Adicionar colisões e tileset próprios para cenário.
- Criar artes definitivas (personagem, itens, ambiente).
- Implementar múltiplas fases e tela de vitória/derrota.
- Declarar uso de IA, créditos e licenças conforme regulamento.

## Estrutura
```
farol_do_saber_godot/
├─ project.godot
├─ icon.png
├─ README.md
├─ scenes/
│  ├─ Main.tscn
│  ├─ Player.tscn
│  └─ Item.tscn
├─ scripts/
│  ├─ Game.gd
│  ├─ Player.gd
│  └─ Item.gd
└─ assets/
   └─ placeholder/
      ├─ player.png
      ├─ book.png
      └─ tile_ground.png
```
