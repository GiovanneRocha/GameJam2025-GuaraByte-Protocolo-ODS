# 🐺 GuaráByte: Protocolo ODS

<img width="1920" height="1080" alt="Game Jam FATEC Campinas 2025" src="https://github.com/user-attachments/assets/ccdd7a15-6136-4ef0-b1b1-64e01a3b36b4" />

Este é o repositório oficial da equipe **[NOME DA SUA EQUIPE AQUI]** para a **Game Jam FATEC Campinas 2025**.

📜 Este documento serve como o `relatorioFinal` do projeto, detalhando todos os aspectos do desenvolvimento do jogo **"GuaráByte: Protocolo ODS"**.

---

## 👥 1. Equipe e Integrantes

- 👨‍💻 **Giovanne Rocha Vieira** - (GTI, Noturno, 4)
- 👨‍💻 **Gabriel Henrique de Sena** - (GTI, Noturno, 4)
- 👨‍💻 **Danilo Vicentin da Silva** - (GTI, Noturno, 4)
- 👨‍💻 **João Paulo Duarte Pimentel** - (GTI, Noturno, 3)

---

## 🎮 2. Sobre o Projeto

- **Título Oficial:** GuaráByte: Protocolo ODS
- **Ferramenta Escolhida:** 🐍 Pygame
- **Gênero:** ⌨️ Typing Game / Ação
- **Estilo:** 🎨 Pixel Art 2D com temática Cyberpunk/Digital

---

## 🌍 3. Descrição e Tema (ODS)

### 📖 Descrição Geral
"GuaráByte" é um jogo de digitação onde o jogador controla o **G.U.A.R.Á.** (*Guardião Unificado de Ambientes de Rede e Aprendizagem*), um avatar digital do Lobo Guará. A missão é combater um vírus chamado **"A Anomalia"**, que invadiu os servidores da FATEC / CPS.

A mecânica central não é de "destruição", mas de **"depuração"**. Ao digitar as palavras que aparecem nos inimigos (dados corrompidos), o G.U.A.R.Á. "conserta" o código, transformando a ameaça em um dado restaurado e limpo.

### ✅ Abordagem do Tema (Protocolo ODS)

Cada fase representa um Objetivo de Desenvolvimento Sustentável:

1️⃣ **ODS 4 - Educação de Qualidade:** Combate *FakeNews*, *Spam* e *Erros404* no Servidor Acadêmico.
2️⃣ **ODS 9 - Inovação e Infraestrutura:** Corrige *Bugs*, *Glitches* e *Código Obsoleto* no Servidor de Infraestrutura.
3️⃣ **ODS 10 - Redução das Desigualdades:** Derruba *Paywalls* e *Muros Digitais* no Servidor de Acesso.
4️⃣ **ODS 11 - Cidades Sustentáveis:** Enfrenta "A Anomalia" no Core do CPS.

---

## 🛠️ 4. Arquitetura e Tecnologias

- **Linguagem:** Python 3
- **Biblioteca Principal:** Pygame
- **Padrões:**
    - 🔄 Máquina de Estados (Menu, Cutscene, Gameplay, Game Over)
    - 🧩 Classes para `WordEnemy` e `Boss`
    - 📦 Módulo `assets.py` para gerenciamento de recursos
- **Tecnologias Auxiliares:**
    - 🤖 IA Generativa: GitHub Copilot, Gemini Pro
    - 🎥 Vídeo: Pippit
    - 🖼️ Imagens: PixVerse + Canva Pro

---

## ▶️ 5. Instruções de Execução

**Pré-requisitos:**
```
Python 3.10+
pygame==2.5.2
Pillow==10.4.0
opencv-python==4.8.0.76
numpy==1.26.4
moviepy==1.0.3
imageio-ffmpeg==0.4.8
```

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

## 🎥 6. Demonstração

- 👾 Cutscene:

---

## 🏅 7. Créditos e Licenças

### 🔧 Ferramentas Utilizadas
- **Arte, Vídeo e Animação (IA):** [PixVerse](https://app.pixverse.ai/), [Pippit](https://www.pippit.ai/pt-br), [Canva Pro](https://www.canva.com/)
- **Música & Sons:** [Pixabay](https://pixabay.com/pt/music/search/game/)
- **Auxiliares (IA):** [GitHub Copilot](https://github.com/copilot), [Gemini Pro](https://gemini.google.com/?hl=pt-BR)

### 🎨 Assets
- **Sprites e Wallpapers:** Criados com PixVerse e editados no Canva Pro
- **Músicas:** Pixabay (uso livre comercial)

---

📜 Este projeto segue o regulamento da **Game Jam FATEC Campinas 2025**.
