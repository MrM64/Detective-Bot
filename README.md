# 🕵️ DetectiveBot

Bot de minijogo de detetive para Discord. O jogador escolhe um caso, investiga locais, interroga suspeitos, junta pistas e tenta descobrir quem é o culpado.

Projeto final de Python, desenvolvido por **Heitor Mayer**.

---

## Funcionalidades

- **4 casos de mistério**, cada um com estilo e investigador próprios:
  1. A Última Testemunha (investigação policial)
  2. O Enigma do Quadro Desaparecido (mistério clássico)
  3. O Segredo da Mansão Blackwood (suspense e terror psicológico)
  4. O Sorriso do Mentiroso (mistério psicológico)
- **Culpado sorteado a cada partida.** O bot lembra quem já foi culpado para cada jogador e evita repetir até esgotar todas as opções do caso.
- **Pistas reais e pistas enganosas.** Cada local investigado revela uma evidência sobre o culpado e outra sobre um inocente, em ordem aleatória.
- **Interrogatórios** com depoimentos e possíveis motivos.
- **3 tentativas de acusação** por partida.
- **Pontuação e ranking** de detetives.
- **Progresso individual salvo** em arquivo JSON.

---

## Estrutura do projeto

```
DetectiveBot/
├── main.py            # lógica do bot e comandos
├── casos.py           # conteúdo do jogo (casos, suspeitos, pistas)
├── requirements.txt   # dependências
├── .env.example       # modelo do arquivo com o token
├── .gitignore         # arquivos que não devem ir para o GitHub
└── README.md
```

O arquivo `jogadores.json` é criado automaticamente quando o bot roda pela primeira vez.

---

## Como instalar e rodar

### Requisitos

- Python 3.9 ou superior
- Uma conta no Discord e um servidor onde você possa adicionar bots

### 1. Instalar as dependências

No Terminal, dentro da pasta do projeto:

```bash
python3 -m pip install -r requirements.txt
```

Se aparecer o erro `externally-managed-environment`, use um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Com o ambiente virtual, é preciso rodar `source venv/bin/activate` toda vez que abrir um terminal novo.

### 2. Criar o bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications) e clique em **New Application**.
2. Na aba **Bot**, clique em **Reset Token** e copie o token.
3. Ainda na aba **Bot**, ative **Message Content Intent**.
4. Na aba **OAuth2 → URL Generator**, marque os escopos `bot` e as permissões *Send Messages* e *Embed Links*. Abra o link gerado para adicionar o bot ao servidor.

### 3. Configurar o token

Copie o arquivo de exemplo e edite:

```bash
cp .env.example .env
```

Abra o `.env` e coloque o token, sem aspas:

```
DISCORD_TOKEN=seu_token_aqui
```

> ⚠️ **Nunca** coloque o token dentro do código, envie para colegas ou publique no GitHub. Quem tem o token controla o bot. Se ele vazar, gere um novo em **Reset Token**.

### 4. Executar

```bash
python3 main.py
```

Quando aparecer `DetectiveBot conectado como ...`, o bot está online.

---

## Comandos

O prefixo é `$`.

| Comando | O que faz |
|---|---|
| `$menu` | Abre o menu para escolher um caso |
| `$ajuda` | Lista todos os comandos |
| `$caso` | Mostra o caso ativo |
| `$suspeitos` | Lista os suspeitos e seus perfis |
| `$investigar <local>` | Investiga um local e revela evidências |
| `$interrogar <nome>` | Ouve o depoimento de um suspeito |
| `$pistas` | Mostra todas as evidências coletadas |
| `$relatorio` | Mostra o progresso da investigação |
| `$acusar <nome>` | Faz uma acusação final |
| `$desistir` | Encerra a partida e revela a solução |
| `$ranking` | Mostra os 10 melhores detetives |

Os nomes aceitam entrada sem acento e parcial. Por exemplo, `$interrogar laura` funciona.

---

## Como jogar

1. Digite `$menu` e escolha um caso.
2. Use `$suspeitos` para conhecer os envolvidos.
3. Use `$investigar <local>` em cada local disponível.
4. Use `$interrogar <nome>` para ouvir cada suspeito.
5. Compare as evidências com os depoimentos. O culpado é quem **se contradiz**, mas cuidado: nem toda pista aponta para a pessoa certa.
6. Quando tiver certeza, use `$acusar <nome>`.

### Pontuação

- **Acertou:** 100 pontos, menos 30 por cada acusação errada anterior (mínimo de 25).
- **Errou as 3 tentativas:** perde 10 pontos.
- **Desistiu:** não ganha nem perde pontos.

---

## Como adicionar um novo caso

Todo o conteúdo fica em `casos.py`. Para criar um caso, copie um bloco existente em `CASOS`, use um novo número como chave e preencha:

- `titulo`, `estilo`, `investigador`, `especialidade`, `emoji`, `introducao`
- `locais`: nome do local e sua descrição
- `suspeitos`: nome, perfil, motivo e depoimento de cada um
- `pistas_por_culpado`: para **cada suspeito**, uma pista em **cada local**
- `desfechos`: o texto da solução para cada suspeito

O menu e o sorteio passam a incluir o novo caso automaticamente. Use nomes de locais sem espaços e sem acentos (por exemplo `sala_seguranca`).

---

## Solução de problemas

| Problema | Solução |
|---|---|
| `ModuleNotFoundError: No module named 'discord'` | Rode `python3 -m pip install -r requirements.txt` |
| `Token não encontrado` | Confira se o arquivo `.env` existe e contém `DISCORD_TOKEN=...` |
| O bot entra online, mas não responde aos comandos | Ative **Message Content Intent** no Developer Portal |
| `LoginFailure: Improper token` | O token está errado ou foi resetado. Gere e cole outro |
| Erros estranhos depois de atualizar o código | Apague o `jogadores.json` antigo |

---

## Tecnologias

- Python 3
- [discord.py](https://discordpy.readthedocs.io/) 2.x
- python-dotenv
