# ============================================================
# casos.py - Todo o conteúdo do jogo (casos, suspeitos, pistas)
# Para criar um caso novo, basta copiar um bloco e editar.
# ============================================================

# Pistas falsas: aparecem em cada local apontando para um INOCENTE.
# {nome} é trocado pelo nome do suspeito sorteado.
PISTAS_FALSAS = [
    "O nome de {nome} aparece nos registros deste local, mas nada indica que tenha ligação direta com o crime.",
    "Há uma anotação envolvendo {nome}. Ela parece antiga e pode não ter relação com o caso.",
    "Um objeto pessoal de {nome} foi encontrado aqui, mas ninguém sabe dizer desde quando estava no local.",
    "Uma testemunha lembra de ter visto {nome} por perto, porém não tem certeza do horário.",
    "Uma mensagem de {nome} parece suspeita à primeira vista, mas o conteúdo é vago e pode ser algo comum.",
]

CASOS = {
    "1": {
        "titulo": "A Última Testemunha",
        "estilo": "Investigação policial",
        "investigador": "Mariana Torres",
        "especialidade": "análise de depoimentos e comportamento",
        "emoji": "🔎",
        "introducao": (
            "O empresário Augusto Ferraz foi encontrado morto em seu escritório "
            "depois de uma reunião privada. Não há sinais claros de invasão. "
            "Cinco pessoas estavam no prédio naquela noite, e todas escondem "
            "alguma informação."
        ),
        "locais": {
            "escritorio": "Você examina a mesa, a janela e os documentos deixados pela vítima.",
            "recepcao": "O livro de visitas e o relógio da recepção podem ajudar a reconstruir os horários.",
            "sala_seguranca": "Os registros de acesso mostram quem entrou em áreas restritas.",
            "arquivo": "Entre contratos e pastas antigas, você encontra documentos que explicam possíveis conflitos.",
        },
        "suspeitos": {
            "ricardo": {"nome": "Ricardo Mendes", "perfil": "Sócio da vítima. Poderia perder muito dinheiro se um contrato fosse cancelado.", "motivo": "disputa financeira", "depoimento": "Eu estava na sala de reuniões. Augusto e eu discutimos negócios, mas saí antes das dez."},
            "laura": {"nome": "Laura Vasconcelos", "perfil": "Secretária de Augusto. Conhecia a agenda e a rotina do escritório.", "motivo": "medo de perder o emprego", "depoimento": "Organizei os documentos e depois fui embora. Não entrei no escritório novamente."},
            "eduardo": {"nome": "Eduardo Nunes", "perfil": "Funcionário que havia discutido com Augusto naquela semana.", "motivo": "ressentimento profissional", "depoimento": "Eu estava no depósito conferindo materiais. Não tinha razão para falar com Augusto naquela noite."},
            "patricia": {"nome": "Patrícia Almeida", "perfil": "Esposa de Augusto. O relacionamento passava por dificuldades.", "motivo": "conflito pessoal", "depoimento": "Vim buscar alguns pertences. A conversa foi breve e não houve discussão."},
            "felipe": {"nome": "Felipe Rocha", "perfil": "Segurança do edifício. Tinha acesso aos registros de entrada.", "motivo": "possível envolvimento em uma irregularidade", "depoimento": "Fiquei na recepção durante todo o turno e segui o protocolo de segurança."},
        },
        "pistas_por_culpado": {
            "ricardo": {
                "escritorio": "Um rascunho de contrato mostra que Ricardo perderia uma grande quantia se Augusto assinasse um documento no dia seguinte.",
                "recepcao": "O registro indica que Ricardo afirmou ter saído às 21h40, mas seu carro deixou o estacionamento mais tarde.",
                "sala_seguranca": "O registro de acesso confirma que o cartão de Ricardo foi usado perto do escritório no horário crítico.",
                "arquivo": "Um e-mail impresso mostra que Ricardo sabia da reunião privada e tentou impedir a assinatura do contrato.",
            },
            "laura": {
                "escritorio": "Uma anotação na agenda mostra que Laura conhecia um detalhe da sala que não havia sido divulgado aos funcionários.",
                "recepcao": "O livro de visitas registra que Laura voltou ao andar depois do horário em que disse ter ido embora.",
                "sala_seguranca": "O registro mostra uma entrada de Laura em uma área restrita durante o intervalo investigado.",
                "arquivo": "Uma cópia de mensagem mostra que Laura temia ser responsabilizada por documentos desaparecidos.",
            },
            "eduardo": {
                "escritorio": "Um memorando revela que Augusto pretendia demitir Eduardo na manhã seguinte.",
                "recepcao": "Uma testemunha anotou um horário que contradiz parte do relato de Eduardo.",
                "sala_seguranca": "O registro de acesso coloca Eduardo no corredor do escritório durante o período investigado.",
                "arquivo": "Uma reclamação assinada por Eduardo demonstra que o conflito profissional era mais grave do que ele admitiu.",
            },
            "patricia": {
                "escritorio": "Uma carta encontrada na gaveta indica que Augusto e Patrícia discutiam uma decisão pessoal importante.",
                "recepcao": "O registro mostra que Patrícia permaneceu no prédio mais tempo do que afirmou.",
                "sala_seguranca": "Uma entrada registrada coloca Patrícia perto do corredor do escritório no horário relevante.",
                "arquivo": "Um documento revela que Patrícia sabia que Augusto faria um anúncio que mudaria a vida dos dois.",
            },
            "felipe": {
                "escritorio": "Um relatório de segurança foi alterado manualmente, e a alteração não foi explicada.",
                "recepcao": "O livro de turnos mostra um intervalo sem registro justamente no período crítico.",
                "sala_seguranca": "O sistema registra uma ação administrativa feita com credenciais de segurança durante o intervalo investigado.",
                "arquivo": "Um relatório antigo sugere que Felipe poderia ser responsabilizado por uma falha de segurança.",
            },
        },
        "desfechos": {
            "ricardo": "Ricardo tentou impedir que Augusto assinasse o contrato que destruiria seu negócio. As evidências de acesso e o conflito financeiro apontam para ele.",
            "laura": "Laura voltou ao andar e aproveitou seu conhecimento da rotina do escritório. O registro de acesso contradiz seu depoimento.",
            "eduardo": "Eduardo agiu depois de descobrir que seria demitido. O memorando e os registros contradizem sua versão.",
            "patricia": "Patrícia escondeu a duração de sua visita e tinha um conflito pessoal importante com Augusto.",
            "felipe": "Felipe usou seu acesso aos sistemas de segurança para esconder sua presença. Os registros alterados revelam a contradição.",
        },
    },
    "2": {
        "titulo": "O Enigma do Quadro Desaparecido",
        "estilo": "Mistério clássico",
        "investigador": "Augusto Valença",
        "especialidade": "dedução lógica e análise de objetos",
        "emoji": "🧩",
        "introducao": (
            "Uma pintura valiosa desapareceu de uma galeria particular durante uma recepção. "
            "As portas pareciam trancadas e ninguém foi visto carregando a obra. "
            "O inventário pode não contar toda a verdade."
        ),
        "locais": {
            "galeria": "Você examina o suporte vazio, as molduras e a disposição das obras.",
            "deposito": "Caixas, materiais de embalagem e ferramentas estão guardados aqui.",
            "escritorio": "Contratos e documentos revelam a história recente da pintura.",
            "corredor": "O corredor liga a galeria às salas de serviço e à saída lateral.",
        },
        "suspeitos": {
            "beatriz": {"nome": "Beatriz Monteiro", "perfil": "Curadora responsável pela organização da exposição.", "motivo": "pressão profissional", "depoimento": "A pintura estava no lugar quando conferi a galeria. Depois, fiquei recebendo convidados."},
            "henrique": {"nome": "Henrique Prado", "perfil": "Colecionador que tentou comprar a obra.", "motivo": "desejo de possuir a pintura", "depoimento": "Eu queria comprar a obra, mas aceitei a recusa do proprietário."},
            "samuel": {"nome": "Samuel Costa", "perfil": "Restaurador que trabalhou na pintura.", "motivo": "conhecimento técnico e possível disputa", "depoimento": "Terminei a restauração dias atrás e não toquei mais na pintura."},
            "isabela": {"nome": "Isabela Duarte", "perfil": "Herdeira do dono da galeria.", "motivo": "disputa sobre herança", "depoimento": "Não concordo com todas as decisões da família, mas não roubei a obra."},
            "otavio": {"nome": "Otávio Ferraz", "perfil": "Funcionário responsável pelo inventário.", "motivo": "pressão por uma falha nos registros", "depoimento": "Os registros estavam corretos quando fiz a última conferência."},
        },
        "pistas_por_culpado": {
            "beatriz": {"galeria": "Uma anotação de montagem mostra que Beatriz pediu para reposicionar a obra pouco antes da recepção.", "deposito": "Materiais de embalagem foram separados com uma etiqueta escrita pela curadora.", "escritorio": "Uma mensagem indica que Beatriz sabia que uma conferência oficial ocorreria na manhã seguinte.", "corredor": "Um registro de serviço coloca Beatriz perto da saída lateral depois do horário que declarou."},
            "henrique": {"galeria": "Há marcas recentes de manuseio na moldura, apesar de Henrique afirmar que não se aproximou dela.", "deposito": "Um recibo de transporte está ligado a uma empresa contratada por Henrique.", "escritorio": "Uma carta mostra que Henrique fez uma oferta muito maior do que admitiu.", "corredor": "Uma testemunha descreve alguém com a mesma bolsa de Henrique perto da saída lateral."},
            "samuel": {"galeria": "A pintura foi retirada com cuidado suficiente para não danificar uma área restaurada por Samuel.", "deposito": "Uma ferramenta especializada, emprestada a Samuel, foi encontrada fora do lugar.", "escritorio": "O relatório de restauração contém uma página ausente assinada por Samuel.", "corredor": "O registro indica que Samuel voltou à galeria depois do encerramento."},
            "isabela": {"galeria": "Uma fotografia antiga mostra que Isabela conhecia um compartimento atrás de uma parede decorativa.", "deposito": "Um objeto pessoal de Isabela foi encontrado entre os materiais preparados para transporte.", "escritorio": "Um documento revela uma disputa de herança que ela minimizou.", "corredor": "Uma anotação coloca Isabela perto da passagem de serviço no horário relevante."},
            "otavio": {"galeria": "O inventário foi atualizado antes do horário registrado, criando uma janela sem conferência.", "deposito": "Uma etiqueta de transporte foi impressa com a conta de Otávio.", "escritorio": "Uma planilha mostra que Otávio alterou uma linha do inventário sem justificativa.", "corredor": "O registro de acesso contradiz a afirmação de Otávio de que não deixou a recepção."},
        },
        "desfechos": {
            "beatriz": "Beatriz controlava a montagem e usou essa responsabilidade para preparar a retirada da obra.",
            "henrique": "Henrique não aceitou perder a pintura e deixou rastros ligados ao transporte.",
            "samuel": "Samuel aproveitou seu conhecimento técnico para retirar a obra sem danificá-la.",
            "isabela": "Isabela conhecia a estrutura da galeria e tinha um motivo familiar para esconder a pintura.",
            "otavio": "Otávio manipulou o inventário para criar uma janela em que o desaparecimento passasse despercebido.",
        },
    },
    "3": {
        "titulo": "O Segredo da Mansão Blackwood",
        "estilo": "Suspense e terror psicológico",
        "investigador": "Helena Duarte",
        "especialidade": "reconstrução de acontecimentos e análise de padrões",
        "emoji": "🌑",
        "introducao": (
            "Durante uma tempestade, uma pessoa desaparece de um quarto que parecia trancado por dentro. "
            "Os moradores falam de passos inexplicáveis e de uma antiga maldição. "
            "Helena procura uma explicação baseada em evidências."
        ),
        "locais": {
            "quarto": "O quarto parece intacto, mas pequenos detalhes não combinam com a história contada.",
            "biblioteca": "Diários e livros antigos revelam conflitos da família Blackwood.",
            "porao": "O porão tem corredores estreitos e objetos guardados há décadas.",
            "hall": "O hall principal permite reconstruir quem circulou pela mansão durante a tempestade.",
        },
        "suspeitos": {
            "alvaro": {"nome": "Álvaro Blackwood", "perfil": "Proprietário da mansão e guardião dos segredos familiares.", "motivo": "proteger a reputação da família", "depoimento": "Fiquei no salão. A história de uma maldição é antiga, mas não acredito que explique tudo."},
            "cecilia": {"nome": "Cecília Moura", "perfil": "Governanta que conhece cada cômodo da propriedade.", "motivo": "lealdade dividida", "depoimento": "Ouvi barulhos, mas não entrei no quarto. Estava preparando a casa para a tempestade."},
            "tomas": {"nome": "Tomás Vieira", "perfil": "Pesquisador da história da mansão.", "motivo": "descobrir um segredo histórico", "depoimento": "Eu estava lendo na biblioteca. Não tenho interesse em assustar ninguém."},
            "elisa": {"nome": "Elisa Blackwood", "perfil": "Herdeira que deseja vender a propriedade.", "motivo": "romper com o passado familiar", "depoimento": "Quero sair desta casa, mas não faria alguém desaparecer."},
            "marcos": {"nome": "Marcos Leal", "perfil": "Médico convidado para passar o fim de semana.", "motivo": "proteger um antigo paciente", "depoimento": "Fiquei no quarto de hóspedes quando a tempestade ficou mais forte."},
        },
        "pistas_por_culpado": {
            "alvaro": {"quarto": "A posição de um móvel indica que alguém conhecia uma passagem escondida da propriedade.", "biblioteca": "Um diário revela que Álvaro tentou ocultar um episódio da história da família.", "porao": "Uma lanterna recente foi deixada perto de uma passagem que Álvaro disse desconhecer.", "hall": "O relógio do hall mostra que Álvaro não poderia ter permanecido no salão durante todo o período."},
            "cecilia": {"quarto": "A fechadura apresenta sinais de um mecanismo conhecido por quem cuida da manutenção da mansão.", "biblioteca": "Um registro antigo mostra que Cecília conhece a planta original da casa.", "porao": "Um molho de chaves de serviço foi escondido atrás de caixas organizadas por Cecília.", "hall": "Uma testemunha ouviu Cecília dizer que não havia passado pelo corredor, embora um objeto seu tenha sido encontrado ali."},
            "tomas": {"quarto": "Anotações de pesquisa mostram que Tomás estudou como criar a aparência de um quarto trancado.", "biblioteca": "Uma página foi removida de um livro que Tomás consultou naquela noite.", "porao": "O caderno de Tomás contém um esboço de uma passagem subterrânea.", "hall": "O registro de visitas contradiz o horário que Tomás informou."},
            "elisa": {"quarto": "Um bilhete mostra que Elisa conhecia um detalhe do quarto que não era conhecido pelos convidados.", "biblioteca": "Uma carta revela que Elisa planejava uma mudança antes do desaparecimento.", "porao": "Uma mala foi preparada perto de uma passagem pouco usada.", "hall": "Uma anotação mostra que Elisa esteve no hall no horário em que afirmou estar no andar superior."},
            "marcos": {"quarto": "Um frasco médico foi encontrado fora do quarto de hóspedes, apesar de Marcos afirmar que não saiu dali.", "biblioteca": "Uma carta revela que Marcos conhecia a pessoa desaparecida antes da visita.", "porao": "Uma pegada recente corresponde ao calçado descrito por uma testemunha.", "hall": "O relato de Marcos sobre a tempestade contradiz o horário registrado no relógio do hall."},
        },
        "desfechos": {
            "alvaro": "Álvaro tentou proteger a família e usou seu conhecimento da mansão para encobrir o desaparecimento.",
            "cecilia": "Cecília conhecia os mecanismos e as passagens da casa melhor do que qualquer outro suspeito.",
            "tomas": "Tomás transformou sua pesquisa histórica em um plano para simular um desaparecimento impossível.",
            "elisa": "Elisa tinha um plano para deixar a mansão e ocultou informações importantes sobre aquela noite.",
            "marcos": "Marcos conhecia a pessoa desaparecida e usou essa relação para esconder o que realmente ocorreu.",
        },
    },
    "4": {
        "titulo": "O Sorriso do Mentiroso",
        "estilo": "Mistério psicológico",
        "investigador": "Gabriel Montenegro",
        "especialidade": "observação, perfis e contradições",
        "emoji": "🃏",
        "introducao": (
            "Um consultor que ajudava a polícia a resolver casos desaparece após enviar uma mensagem enigmática. "
            "Em seu escritório há fotografias, símbolos e registros de investigações antigas. "
            "Alguém está tentando conduzir a investigação para uma conclusão errada."
        ),
        "locais": {
            "escritorio": "Fotografias e anotações parecem formar um padrão, mas algumas foram colocadas fora de ordem.",
            "cafeteria": "Funcionários lembram de conversas e encontros próximos ao desaparecimento.",
            "arquivo": "Relatórios antigos conectam o consultor a pessoas que negam conhecê-lo.",
            "estacionamento": "Marcas e registros de entrada ajudam a reconstruir os últimos movimentos.",
        },
        "suspeitos": {
            "renato": {"nome": "Renato Silveira", "perfil": "Antigo parceiro profissional do consultor.", "motivo": "rivalidade profissional", "depoimento": "Nossa parceria terminou há meses. Não sei por que ele me envolveria nisso."},
            "mirela": {"nome": "Mirela Campos", "perfil": "Jornalista que investigava os métodos do consultor.", "motivo": "obter uma grande reportagem", "depoimento": "Eu queria entrevistá-lo, não fazê-lo desaparecer."},
            "andre": {"nome": "André Vasconcelos", "perfil": "Empresário exposto por uma investigação anterior.", "motivo": "vingança e reputação", "depoimento": "Não tive contato com ele desde que a reportagem foi publicada."},
            "bianca": {"nome": "Bianca Freire", "perfil": "Assistente que conhecia a agenda e os hábitos do consultor.", "motivo": "medo de que um segredo fosse revelado", "depoimento": "Eu apenas organizava os compromissos. Não conhecia todos os assuntos dele."},
            "davi": {"nome": "Davi Moreira", "perfil": "Investigador que trabalhou em um caso relacionado ao consultor.", "motivo": "proteger uma investigação antiga", "depoimento": "Meu trabalho naquele caso terminou. Não tenho motivo para interferir agora."},
        },
        "pistas_por_culpado": {
            "renato": {"escritorio": "Duas fotografias foram reorganizadas para sugerir uma sequência falsa; as anotações usam o método de Renato.", "cafeteria": "Um atendente lembra de uma conversa em que Renato pediu para não ser registrado como visitante.", "arquivo": "Um relatório antigo mostra que Renato e o consultor discordaram sobre uma prova importante.", "estacionamento": "O registro de entrada coloca o veículo de Renato perto do prédio no horário em que ele disse estar longe."},
            "mirela": {"escritorio": "Uma anotação de entrevista contém perguntas que Mirela afirmou nunca ter recebido.", "cafeteria": "Um recibo mostra que Mirela esteve no local mais cedo do que declarou.", "arquivo": "Rascunhos de uma reportagem mostram que Mirela tinha acesso a informações confidenciais.", "estacionamento": "Uma testemunha descreve alguém carregando equipamento semelhante ao de Mirela."},
            "andre": {"escritorio": "Uma carta ameaça revelar um novo documento ligado à investigação que expôs André.", "cafeteria": "Um funcionário reconhece André, apesar de ele negar ter visitado o bairro.", "arquivo": "Um relatório mostra que André tentou descobrir onde o consultor guardava provas.", "estacionamento": "O registro de uma cancela contradiz o álibi apresentado por André."},
            "bianca": {"escritorio": "A agenda foi alterada usando informações que apenas Bianca administrava.", "cafeteria": "Uma mensagem mostra que Bianca marcou um encontro sem registrá-lo na agenda oficial.", "arquivo": "Uma cópia de documento indica que Bianca conhecia o segredo que o consultor pretendia revelar.", "estacionamento": "O registro mostra uma saída no horário em que Bianca afirmou já estar em casa."},
            "davi": {"escritorio": "Uma anotação menciona um detalhe de uma investigação que deveria estar sob acesso restrito.", "cafeteria": "Uma testemunha ouviu Davi discutir com o consultor sobre um caso antigo.", "arquivo": "Um relatório foi retirado do arquivo usando credenciais ligadas à equipe de Davi.", "estacionamento": "O registro de acesso contradiz o horário que Davi informou aos colegas."},
        },
        "desfechos": {
            "renato": "Renato tentou controlar a narrativa e reorganizou evidências para criar uma sequência enganosa.",
            "mirela": "Mirela tinha acesso a informações confidenciais e tentou transformar o desaparecimento em uma história exclusiva.",
            "andre": "André queria impedir que novas provas sobre sua conduta viessem à tona.",
            "bianca": "Bianca conhecia a agenda e o segredo do consultor, o que lhe permitiu preparar o desaparecimento.",
            "davi": "Davi tentou proteger uma investigação antiga e usou seu acesso a registros restritos.",
        },
    },
}
