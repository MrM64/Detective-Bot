import json
import os
import random
import unicodedata
from pathlib import Path

import discord
from discord.ext import commands

# Lê o arquivo .env (se existir) para carregar o DISCORD_TOKEN
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from casos import CASOS, PISTAS_FALSAS

# ============================================================
# DETECTIVEBOT - Bot de investigação individual para Discord
# Prefixo: $
# ============================================================

TOKEN = os.getenv("DISCORD_TOKEN")  # o NOME da variável, nunca o token em si
ARQUIVO_DADOS = Path(__file__).resolve().parent / "jogadores.json"
MAX_ERROS = 3  # acusações erradas permitidas por partida

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)


# ------------------------------------------------------------
# Utilitários e persistência
# ------------------------------------------------------------
def normalizar(texto):
    """Remove acentos e padroniza o texto para comparar entradas."""
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace(" ", "_").replace("-", "_")


def carregar_dados():
    if not ARQUIVO_DADOS.exists():
        return {"jogadores": {}}
    try:
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as f:
            dados = json.load(f)
        dados.setdefault("jogadores", {})
        return dados
    except (json.JSONDecodeError, OSError):
        return {"jogadores": {}}


def salvar_dados():
    temporario = ARQUIVO_DADOS.with_suffix(".tmp")
    with temporario.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    temporario.replace(ARQUIVO_DADOS)


dados = carregar_dados()


def obter_jogador(user_id):
    chave = str(user_id)
    jogador = dados["jogadores"].setdefault(chave, {})
    jogador.setdefault("historico_culpados", {})
    jogador.setdefault("partida", None)
    jogador.setdefault("pontos", 0)
    jogador.setdefault("casos_resolvidos", 0)
    return jogador


def obter_partida(user_id):
    return obter_jogador(user_id)["partida"]


def sortear_culpado(user_id, caso_id):
    """Evita repetir o culpado desse caso até esgotar as opções."""
    jogador = obter_jogador(user_id)
    historico = jogador["historico_culpados"].get(caso_id, [])
    suspeitos = list(CASOS[caso_id]["suspeitos"].keys())
    disponiveis = [s for s in suspeitos if s not in historico]
    if not disponiveis:
        historico = []
        disponiveis = suspeitos
    culpado = random.choice(disponiveis)
    historico.append(culpado)
    jogador["historico_culpados"][caso_id] = historico
    return culpado


def encontrar_suspeito(caso, entrada):
    busca = normalizar(entrada)
    for chave, info in caso["suspeitos"].items():
        if busca in (normalizar(chave), normalizar(info["nome"])):
            return chave
    for chave, info in caso["suspeitos"].items():
        if busca in normalizar(info["nome"]):
            return chave
    return None


def encontrar_local(caso, entrada):
    busca = normalizar(entrada)
    for local in caso["locais"]:
        if normalizar(local) == busca:
            return local
    return None


def nome_local(local):
    return local.replace("_", " ").title()


# ------------------------------------------------------------
# Menu de casos
# ------------------------------------------------------------
def montar_menu_embed():
    embed = discord.Embed(
        title="🕵️ DETECTIVEBOT — Central de Investigações",
        description=(
            "Escolha um caso no menu abaixo para iniciar uma investigação individual.\n\n"
            "Cada partida sorteia um culpado diferente. Cuidado: nem toda pista "
            "aponta para o verdadeiro culpado!"
        ),
        color=discord.Color.dark_blue(),
    )
    for numero, caso in CASOS.items():
        embed.add_field(
            name=f"Caso {numero}: {caso['titulo']}",
            value=f"**Estilo:** {caso['estilo']}\n**Investigador:** {caso['investigador']}",
            inline=False,
        )
    embed.set_footer(text="Use $ajuda para ver os comandos.")
    return embed


class MenuCasos(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.message = None
        opcoes = [
            discord.SelectOption(
                label=f"Caso {numero}: {caso['titulo']}"[:100],
                description=f"{caso['estilo']} — {caso['investigador']}"[:100],
                value=numero,
                emoji=caso.get("emoji"),
            )
            for numero, caso in CASOS.items()
        ]
        self.selecao = discord.ui.Select(
            placeholder="Escolha qual caso deseja investigar...",
            options=opcoes,
        )
        self.selecao.callback = self.selecionar_caso
        self.add_item(self.selecao)

    async def selecionar_caso(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "Este menu pertence a outra pessoa. Digite `$menu` para abrir o seu.",
                ephemeral=True,
            )
            return

        caso_id = self.selecao.values[0]
        caso = CASOS[caso_id]
        culpado = sortear_culpado(interaction.user.id, caso_id)

        jogador = obter_jogador(interaction.user.id)
        jogador["partida"] = {
            "caso_id": caso_id,
            "culpado": culpado,
            "locais_investigados": [],
            "pistas": [],
            "interrogados": [],
            "erros": 0,
            "encerrada": False,
            "vitoria": False,
        }
        salvar_dados()

        embed = discord.Embed(
            title=f"📁 Caso {caso_id}: {caso['titulo']}",
            description=(
                f"**Investigador:** {caso['investigador']}\n"
                f"**Especialidade:** {caso['especialidade']}\n\n"
                f"{caso['introducao']}\n\n"
                "**Sua missão:** descobrir quem é o culpado. Compare as pistas com os "
                "depoimentos e procure contradições."
            ),
            color=discord.Color.dark_red(),
        )
        embed.add_field(
            name="📍 Locais disponíveis",
            value=", ".join(f"`{l}`" for l in caso["locais"]),
            inline=False,
        )
        embed.add_field(
            name="🧭 Próximos passos",
            value="Use `$suspeitos`, `$investigar <local>` e `$interrogar <nome>`.",
            inline=False,
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


# ------------------------------------------------------------
# Eventos e comandos
# ------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"DetectiveBot conectado como {bot.user}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} está online!")

    canal = bot.get_channel(1565141240788291668)

    if canal:
        await canal.send(
            "🕵️ **DetetiveBot está online!**\n\n"
            "Olá, detetive! Estou pronto para investigar.\n"
            "🔎 Digite **`$ajuda`** para descobrir todos os comandos "
            "disponíveis e aprender como jogar!\n\n"
            "Boa investigação! 🕵️"
        )

@bot.command(name="menu")
async def menu(ctx):
    """Abre o menu de seleção de casos."""
    view = MenuCasos(ctx.author.id)
    view.message = await ctx.send(embed=montar_menu_embed(), view=view)


@bot.command(name="ajuda")
async def ajuda(ctx):
    texto = (
        "**🕵️ Comandos do DetectiveBot**\n\n"
        "`$menu` — escolher um dos casos.\n"
        "`$caso` — mostra o caso ativo.\n"
        "`$suspeitos` — lista os suspeitos.\n"
        "`$investigar <local>` — investiga um local (ex.: `$investigar escritorio`).\n"
        "`$interrogar <nome>` — ouve o depoimento de um suspeito.\n"
        "`$pistas` — mostra as evidências encontradas.\n"
        "`$relatorio` — mostra o progresso.\n"
        f"`$acusar <nome>` — acusação final (você tem {MAX_ERROS} tentativas).\n"
        "`$desistir` — encerra e revela a solução.\n"
        "`$ranking` — melhores detetives.\n\n"
        "Atenção: algumas pistas são enganosas. Procure quem **contradiz o próprio depoimento**."
    )
    await ctx.send(texto)


@bot.command(name="caso")
async def caso_atual(ctx):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Você ainda não iniciou um caso. Digite `$menu` para escolher.")
        return
    caso = CASOS[partida["caso_id"]]
    estado = "encerrada" if partida["encerrada"] else "em andamento"
    embed = discord.Embed(
        title=f"📁 {caso['titulo']}",
        description=f"**Investigador:** {caso['investigador']}\n**Estado:** {estado}\n\n{caso['introducao']}",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Evidências", value=str(len(partida["pistas"])), inline=True)
    embed.add_field(name="Interrogados", value=str(len(partida["interrogados"])), inline=True)
    embed.add_field(name="Acusações restantes", value=str(MAX_ERROS - partida["erros"]), inline=True)
    await ctx.send(embed=embed)


@bot.command(name="suspeitos")
async def listar_suspeitos(ctx):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para iniciar uma investigação.")
        return
    caso = CASOS[partida["caso_id"]]
    embed = discord.Embed(title="🧍 Suspeitos", color=discord.Color.gold())
    for info in caso["suspeitos"].values():
        embed.add_field(name=info["nome"], value=info["perfil"], inline=False)
    await ctx.send(embed=embed)


@bot.command(name="investigar")
async def investigar(ctx, *, local: str = None):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para escolher um caso.")
        return
    if partida["encerrada"]:
        await ctx.send("Sua investigação já foi encerrada. Digite `$menu` para iniciar outra.")
        return

    caso = CASOS[partida["caso_id"]]
    opcoes = ", ".join(f"`{x}`" for x in caso["locais"])
    if not local:
        await ctx.send(f"Informe um local. Opções: {opcoes}")
        return

    chave_local = encontrar_local(caso, local)
    if chave_local is None:
        await ctx.send(f"Não reconheci esse local. Opções: {opcoes}")
        return
    if chave_local in partida["locais_investigados"]:
        await ctx.send("Você já investigou esse local. Use `$pistas` para rever as evidências.")
        return

    # Cada local rende uma pista real (sobre o culpado) e uma pista enganosa (sobre um inocente)
    culpado = partida["culpado"]
    pista_real = caso["pistas_por_culpado"][culpado][chave_local]
    inocentes = [k for k in caso["suspeitos"] if k != culpado]
    inocente = random.choice(inocentes)
    pista_falsa = random.choice(PISTAS_FALSAS).format(nome=caso["suspeitos"][inocente]["nome"])

    novas = [pista_real, pista_falsa]
    random.shuffle(novas)  # o jogador não sabe qual é qual

    partida["locais_investigados"].append(chave_local)
    for texto in novas:
        partida["pistas"].append({"local": chave_local, "texto": texto})
    salvar_dados()

    embed = discord.Embed(
        title=f"🔎 Local investigado: {nome_local(chave_local)}",
        description=(
            caso["locais"][chave_local]
            + "\n\n**Novas evidências:**\n"
            + "\n".join(f"• {t}" for t in novas)
        ),
        color=discord.Color.green(),
    )
    embed.set_footer(text="Nem toda evidência é conclusiva. Use $pistas para consultar.")
    await ctx.send(embed=embed)


@bot.command(name="interrogar")
async def interrogar(ctx, *, nome: str = None):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para iniciar uma investigação.")
        return
    if partida["encerrada"]:
        await ctx.send("Sua investigação já foi encerrada. Digite `$menu` para iniciar outra.")
        return
    if not nome:
        await ctx.send("Informe o nome do suspeito. Use `$suspeitos` para ver a lista.")
        return

    caso = CASOS[partida["caso_id"]]
    chave = encontrar_suspeito(caso, nome)
    if not chave:
        await ctx.send("Não encontrei esse suspeito. Use `$suspeitos` para ver os nomes.")
        return

    info = caso["suspeitos"][chave]
    if chave not in partida["interrogados"]:
        partida["interrogados"].append(chave)
        salvar_dados()

    # Mesma resposta para todos: o tom do depoimento não entrega o culpado.
    embed = discord.Embed(
        title=f"🗣️ Interrogatório: {info['nome']}",
        description=f"\"{info['depoimento']}\"\n\n*{caso['investigador']} anota o depoimento para comparar com as evidências.*",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Possível motivo", value=info["motivo"], inline=False)
    embed.set_footer(text="Compare o depoimento com as pistas. Nervosismo não é prova.")
    await ctx.send(embed=embed)


@bot.command(name="pistas")
async def listar_pistas(ctx):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para iniciar uma investigação.")
        return
    if not partida["pistas"]:
        await ctx.send("Você ainda não encontrou pistas. Use `$investigar <local>`.")
        return
    embed = discord.Embed(title="🧾 Inventário de evidências", color=discord.Color.teal())
    for numero, pista in enumerate(partida["pistas"], start=1):
        embed.add_field(
            name=f"#{numero} — {nome_local(pista['local'])}",
            value=pista["texto"],
            inline=False,
        )
    await ctx.send(embed=embed)


@bot.command(name="relatorio")
async def relatorio(ctx):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para iniciar uma investigação.")
        return
    caso = CASOS[partida["caso_id"]]
    embed = discord.Embed(title="📋 Relatório da investigação", color=discord.Color.blurple())
    embed.add_field(name="Caso", value=caso["titulo"], inline=False)
    embed.add_field(
        name="Locais investigados",
        value=", ".join(nome_local(l) for l in partida["locais_investigados"]) or "Nenhum",
        inline=False,
    )
    embed.add_field(
        name="Suspeitos interrogados",
        value=", ".join(caso["suspeitos"][x]["nome"] for x in partida["interrogados"]) or "Nenhum",
        inline=False,
    )
    embed.add_field(name="Evidências", value=str(len(partida["pistas"])), inline=True)
    embed.add_field(name="Acusações erradas", value=f"{partida['erros']}/{MAX_ERROS}", inline=True)
    embed.add_field(name="Estado", value="Encerrada" if partida["encerrada"] else "Em andamento", inline=True)
    await ctx.send(embed=embed)


async def encerrar_partida(ctx, partida, venceu, desistiu=False):
    caso = CASOS[partida["caso_id"]]
    culpado = partida["culpado"]
    nome_culpado = caso["suspeitos"][culpado]["nome"]
    partida["encerrada"] = True
    partida["vitoria"] = venceu
    jogador = obter_jogador(ctx.author.id)

    if venceu:
        pontos = max(25, 100 - partida["erros"] * 30)
        jogador["pontos"] += pontos
        jogador["casos_resolvidos"] += 1
        titulo = "✅ Caso resolvido!"
        descricao = f"Você identificou **{nome_culpado}** e ganhou **{pontos} pontos**."
        cor = discord.Color.green()
    elif desistiu:
        titulo = "📁 Investigação encerrada"
        descricao = "Você encerrou a investigação sem resolver o caso."
        cor = discord.Color.orange()
    else:
        jogador["pontos"] = max(0, jogador["pontos"] - 10)
        titulo = "❌ Fim das tentativas"
        descricao = "Você esgotou suas acusações e perdeu 10 pontos."
        cor = discord.Color.red()

    descricao += f"\n\n**Solução:** {nome_culpado} era o culpado.\n{caso['desfechos'][culpado]}"
    embed = discord.Embed(title=titulo, description=descricao, color=cor)
    embed.set_footer(text="Digite $menu para iniciar uma nova partida.")
    salvar_dados()
    await ctx.send(embed=embed)


@bot.command(name="acusar")
async def acusar(ctx, *, nome: str = None):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Digite `$menu` para iniciar uma investigação.")
        return
    if partida["encerrada"]:
        await ctx.send("Essa partida já foi encerrada. Digite `$menu` para jogar novamente.")
        return
    if not nome:
        await ctx.send("Informe o nome de um suspeito. Exemplo: `$acusar Laura Vasconcelos`.")
        return

    caso = CASOS[partida["caso_id"]]
    chave = encontrar_suspeito(caso, nome)
    if not chave:
        await ctx.send("Não encontrei esse suspeito. Use `$suspeitos` para ver os nomes.")
        return

    if chave == partida["culpado"]:
        await encerrar_partida(ctx, partida, True)
        return

    partida["erros"] += 1
    if partida["erros"] >= MAX_ERROS:
        await encerrar_partida(ctx, partida, False)
    else:
        salvar_dados()
        restantes = MAX_ERROS - partida["erros"]
        await ctx.send(
            f"❌ **{caso['suspeitos'][chave]['nome']}** não é o culpado. "
            f"Você ainda tem **{restantes}** tentativa(s). Reveja as pistas e os depoimentos."
        )


@bot.command(name="desistir")
async def desistir(ctx):
    partida = obter_partida(ctx.author.id)
    if not partida:
        await ctx.send("Você não tem uma investigação ativa. Digite `$menu`.")
        return
    if partida["encerrada"]:
        await ctx.send("Essa investigação já foi encerrada.")
        return
    await encerrar_partida(ctx, partida, False, desistiu=True)


@bot.command(name="ranking")
async def ranking(ctx):
    jogadores = {k: v for k, v in dados["jogadores"].items() if v.get("pontos", 0) > 0}
    if not jogadores:
        await ctx.send("Ainda não há pontuações registradas.")
        return
    ordenados = sorted(jogadores.items(), key=lambda i: i[1]["pontos"], reverse=True)[:10]
    linhas = []
    for posicao, (user_id, info) in enumerate(ordenados, start=1):
        membro = ctx.guild.get_member(int(user_id)) if ctx.guild else None
        nome = membro.display_name if membro else f"Detetive {user_id[-4:]}"
        linhas.append(
            f"**{posicao}.** {nome} — {info['pontos']} pontos "
            f"({info.get('casos_resolvidos', 0)} casos resolvidos)"
        )
    embed = discord.Embed(
        title="🏆 Ranking dos Detetives",
        description="\n".join(linhas),
        color=discord.Color.gold(),
    )
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltou uma informação no comando. Digite `$ajuda` para ver exemplos.")
        return
    print(f"Erro no comando {ctx.command}: {error}")
    await ctx.send("Ocorreu um erro ao executar o comando. Confira o terminal para mais detalhes.")


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError(
            "Token não encontrado. Crie um arquivo .env com a linha DISCORD_TOKEN=seu_token "
            "ou rode: export DISCORD_TOKEN='seu_token'"
        )
    bot.run(TOKEN)
