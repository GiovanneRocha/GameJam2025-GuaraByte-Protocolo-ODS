# GuaráByte: Protocolo ODS

<img width="1920" height="1080" alt="game jam fatec campinas 2025" src="https://github.com/user-attachments/assets/ccdd7a15-6136-4ef0-b1b1-64e01a3b36b4" />

Este é o repositório oficial da equipe **[NOME DA SUA EQUIPE AQUI]** para a **Game Jam FATEC Campinas 2025**.

Este documento serve como o `relatorioFinal` do projeto, detalhando todos os aspectos do desenvolvimento do jogo "GuaráByte: Protocolo ODS".

---

## 1. Equipe e Integrantes

* **Giovanne Rocha Vieira** - (GTI, Noturno, 4)
* **Gabriel Henrique de Sena** - (GTI, Noturno, 4)
* **Danilo Vicentin da Silva** - (GTI, Noturno, 4)
* **João Paulo Duarte Pimentel** - (GTI, Noturno, 3)

---

## 2. Sobre o Projeto

* **Título Oficial:** GuaráByte: Protocolo ODS
* **Ferramenta Escolhida:** Pygame
* **Gênero:** Typing Game (Jogo de Digitação) / Ação
* **Estilo:** Pixel Art 2D com temática Cyberpunk/Digital

---

## 3. Descrição e Tema (ODS)

### Descrição Geral
"GuaráByte" é um jogo de digitação onde o jogador controla o **G.U.A.R.Á.** (Guardião Unificado de Ambientes de Rede e Aprendizagem), um avatar digital do Lobo Guará. A missão é combater um vírus chamado "A Anomalia", que invadiu os servidores da FATEC / CPS.

A mecânica central não é de "destruição", mas de "depuração". Ao digitar as palavras que aparecem nos inimigos (dados corrompidos), o G.U.A.R.Á. "conserta" o código, transformando a ameaça em um dado restaurado e limpo.

### Abordagem do Tema (Protocolo ODS)

O tema foi abordado transformando os 4 Servidores-Núcleo do jogo em representações das ODS (Objetivos de Desenvolvimento Sustentável):

* **Fase 1 (ODS 4: Educação de Qualidade):** O G.U.A.R.Á. combate *FakeNews*, *Spam* e *Erros404* no Servidor Acadêmico.
* **Fase 2 (ODS 9: Inovação e Infraestrutura):** O G.U.A.R.Á. conserta *Bugs*, *Glitches* e *Código Obsoleto* no Servidor de Infraestrutura.
* **Fase 3 (ODS 10: Redução das Desigualdades):** O G.U.A.R.Á. destrói *Paywalls*, *Muros Digitais* e *Acesso Negado* no Servidor de Acesso.
* **Fase 4 (ODS 11: Cidades e Comunidades Sustentáveis):** O G.U.A.R.Á. enfrenta "A Anomalia" no Core do CPS, impedindo a "poluição digital" de derrubar a comunidade conectada.

---

## 4. Arquitetura e Tecnologias

* **Linguagem:** Python 3
* **Biblioteca Principal:** Pygame (para a lógica central, renderização e eventos)
* **Padrões:**
    * **Máquina de Estados:** O jogo é controlado por uma máquina de estados principal (Menu, Cutscene, Playing, Game Over, Victory).
    * **Gerenciamento de Entidades:** Classes separadas para `WordEnemy` e `Boss`, que encapsulam seu próprio estado (posição, velocidade, palavra, vida).
    * **Módulos de Assets:** Um módulo `assets.py` centralizado para carregar e cachear todas as imagens, sons e músicas, evitando acessos repetidos ao disco.
* **Tecnologias Auxiliares:**
    * **IA Generativa:** Usamos Git Copilot e Gemini Pro para auxiliar na criação e correção do codigo. Pippit para a criação do vídeo, PixVerse para a criação das imagens usadas

---

## 5. Instruções de Execução

**Pré-requisitos:**
* Python 3.10 (ou superior)
* pygame==2.5.2
* Pillow==10.4.0
* Opencv-python==4.8.0.76
* Numpy==1.26.4
* Moviepy==1.0.3
* Imageio-ffmpeg==0.4.8

**Passo-a-passo para rodar:**

1.  Clone este repositório:
    ```bash
    git clone [URL_DO_SEU_FORK]
    cd [NOME_DO_REPOSITORIO]
    ```
2.  (Recomendado) Crie um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # (Linux/macOS)
    .\venv\Scripts\activate   # (Windows)
    ```
3.  Instale as dependências:
    ```bash
    python -m pip install opencv-python moviepy imageio-ffmpeg numpy pygame Pillow
    ```
4.  Execute o jogo:
    ```bash
    python main.py
    ```

---

## 6. Mudanças desde o Relatório Inicial

| Relatório Inicial (Ideathon) | Produto Final (Relatório Final) |
| :--- | :--- |
| A ideia era um jogo de plataforma simples. | Mudamos o gênero para "Typing Game" para focar na mecânica de "depuração" (digitar). |
| O G.U.A.R.Á. iria "pular" nos inimigos. | O G.U.A.R.Á. agora mira e o jogador digita as palavras associadas aos inimigos. |
| O tema ODS seria apenas visual. | O tema ODS foi integrado à mecânica e à narrativa de cada fase. |
| [Adicione outras mudanças que vocês fizeram...] | [Adicione outras mudanças...] |

---

## 7. Demonstração (GIFs e Vídeos)

Aqui estão as principais funcionalidades do jogo em ação:

### Menu Inicial e Cutscene
*(Insira aqui um GIF ou link de vídeo do menu e da cutscene)*

### Gameplay - Fase 1 (ODS 4)
*(Insira aqui um GIF ou link de vídeo do G.U.A.R.Á. "depurando" inimigos na Fase 1)*

### Gameplay - Batalha do Chefe (ODS 11)
*(Insira aqui um GIF ou link de vídeo da batalha contra o Boss)*

### Tela de Vitória
*(Insira aqui uma captura de tela ou GIF da tela de vitória)*

---

## 8. Créditos e Licenças (Assets)

* **Músicas e Efeitos Sonoros:** Musicas do Site pixabay: https://pixabay.com/pt/music/search/game
* **Fontes:** 
* **Arte (IA):** Todos os *sprites* de personagens e *wallpapers* de fundo foram gerados usando [Nome da Ferramenta de IA] e finalizados/editados pela equipe.
* **Regulamento da Game Jam:** Este projeto usa o template de `README.md` fornecido pela organização da Game Jam FATEC Campinas 2025.
