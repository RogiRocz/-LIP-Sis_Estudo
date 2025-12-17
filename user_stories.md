ENTIDADE: USUÁRIO

HU01 - CADASTRO DE USUÁRIO
Como estudante gostaria de me cadastrar como usuário do sistema

Critérios de aceitação:
- Informar email
- Informar a senha
- Confirmar a senha
- O email tem que ser válido e único
- Após cadastrar, fazer login automaticamente
- Tema padrão: claro
- Intervalo de revisões padrão: 1-7-14 dias

HU02 - LOGIN NO SISTEMA
Como usuário gostaria de fazer login no sistema

Critérios de aceitação:
- Informar email cadastrado
- Informar senha correta
- Acesso negado para credenciais inválidas
- Redirecionar para o dashboard após login

HU03 - VISUALIZAÇÃO DE PERFIL
Como usuário gostaria de visualizar meu perfil

Critérios de aceitação:
- Exibir email cadastrado
- Exibir data de cadastro
- Exibir quantidade total de disciplinas
- Exibir quantidade total de temas cadastrados por disciplina
- Exibir tema atual do sistema
- Exibir intervalo de revisões configurado

HU04 - EDIÇÃO DE PERFIL
Como usuário gostaria de alterar as informações do meu perfil

Critérios de aceitação:
- Alterar email (com validação de único)
- Alterar senha (com confirmação)
- Alterar intervalo entre revisões
- Alterar tema do sistema: claro ou escuro
- Salvar alterações com confirmação

HU05 - EXCLUSÃO DE CONTA
Como usuário gostaria de excluir meu perfil

Critérios de aceitação:
- Confirmar exclusão por senha
- Excluir todas as disciplinas associadas
- Excluir todos os temas associados
- Excluir todas as revisões associadas
- Redirecionar para página inicial após exclusão

ENTIDADE: DISCIPLINA

HU06 - CADASTRO DE DISCIPLINA
Como usuário gostaria de cadastrar uma disciplina para organizar meus estudos

Critérios de aceitação:
- Informar nome da disciplina
- Informar descrição (opcional)
- Escolher uma cor para identificar a disciplina
- Visualizar lista de disciplinas cadastradas
- Filtrar disciplinas por nome
- Limite máximo de 20 disciplinas por usuário

HU07 - EDIÇÃO DE DISCIPLINA
Como usuário gostaria de editar uma disciplina cadastrada

Critérios de aceitação:
- Selecionar disciplina da lista
- Alterar nome da disciplina
- Alterar descrição
- Alterar cor de identificação
- Salvar as alterações
- Manter todos os temas vinculados

HU08 - EXCLUSÃO DE DISCIPLINA
Como usuário gostaria de excluir uma disciplina cadastrada

Critérios de aceitação:
- Selecionar disciplina da lista
- Confirmar exclusão
- Excluir também todos os temas e revisões relacionados
- Atualizar lista após exclusão
- Mostrar contagem de temas que serão excluídos

ENTIDADE: TEMA

HU09 - CADASTRO DE TEMA
Como usuário gostaria de cadastrar um tema de uma disciplina para poder estudar

Critérios de aceitação:
- Selecionar a disciplina
- Informar o tema de estudo
- Informar descrição do conteúdo (opcional)
- Usar intervalo de revisão padrão do usuário
- Ao registrar, criar cronograma de revisões virtuais para 1, 7 e 14 dias
- Filtrar temas por nome
- Limite máximo de 50 temas por disciplina

HU10 - EDIÇÃO DE TEMA
Como usuário gostaria de editar um tema cadastrado

Critérios de aceitação:
- Selecionar tema da lista
- Alterar nome do tema
- Alterar descrição
- Alterar o intervalo de revisões
- Salvar as alterações
- Atualizar revisões existentes

HU11 - EXCLUSÃO DE TEMA
Como usuário gostaria de excluir um tema cadastrado

Critérios de aceitação:
- Selecionar tema da lista
- Confirmar exclusão
- Excluir também todas as revisões relacionadas
- Atualizar lista após exclusão
- Mostrar contagem de revisões que serão excluídas

ENTIDADE: REVISÃO

HU12 - VISUALIZAÇÃO DE CRONOGRAMA
Como usuário gostaria de visualizar meu cronograma de revisões

Critérios de aceitação:
- Exibir todas as disciplinas cadastradas
- Exibir os temas de cada disciplina
- Exibir calendário com datas de revisão
- Mostrar revisões pendentes em destaque
- Mostrar revisões atrasadas em vermelho
- Filtrar por nome da disciplina
- Filtrar por status da revisão
- Visualizar em formato de lista ou calendário

HU13 - FILTRO DE REVISÕES
Como usuário gostaria de filtrar minhas revisões para me planejar

Critérios de aceitação:
- Filtrar por disciplina
- Filtrar por nome do tema
- Filtrar por status (pendente/concluída/atrasada)
- Filtrar por período (hoje/semana/mês/todos)
- Exibir quantidade de revisões por tipo
- Exibir tempo total dedicado
- Ordenar por data ou prioridade

HU14 - GERENCIamento DE REVISÕES PENDENTES
Como usuário gostaria de gerenciar minhas revisões pendentes

Critérios de aceçaão:
- Visualizar lista de revisões pendentes
- Filtrar revisões por nome do tema
- Marcar revisão como concluída
- Reagendar data de revisão
- Visualizar revisões atrasadas em destaque
- Ver histórico de revisões realizadas
- Agrupar por disciplina

HU15 - REGISTRO DE SESSÃO DE ESTUDO
Como usuário ao terminar de revisar um tema gostaria de registrar quanto tempo levei

Critérios de aceitação:
- Selecionar a disciplina
- Selecionar o tema
- Informar a data (padrão: data atual)
- Informar a hora (padrão: hora atual)
- Informar, em minutos, o tempo dedicado
- Marcar revisão como concluída automaticamente
- Filtrar temas por nome durante a seleção
- Validar tempo mínimo (5 minutos) e máximo (480 minutos)

HU16 - HISTÓRICO DE SESSÕES
Como usuário gostaria de visualizar meu histórico de cronograma

Critérios de aceitação:
- Exibir lista de todas as cronograma
- Filtrar por disciplina
- Filtrar por nome do tema
- Filtrar por data (início e fim)
- Exibir tempo total por período
- Ordenar por data ou tempo

ENTIDADE: RELATÓRIO

HU17 - RELATÓRIOS DE ESTUDO
Como usuário gostaria de ver relatórios dos meus estudos

Critérios de aceitação:
- Exibir tempo total de estudo por disciplina
- Exibir quantidade de revisões realizadas
- Exibir taxa de conclusão de revisões
- Gráfico de distribuição por disciplina
- Filtrar relatórios por período (semana/mês/trimestre/ano)
- Filtrar por nome da disciplina
- Comparar com períodos anteriores
- Exportar relatório em PDF (opcional)

HU18 - ESTATÍSTICAS DE DESEMPENHO
Como usuário gostaria de visualizar estatísticas de desempenho

Critérios de aceitação:
- Exibir tempo médio por sessão de estudo
- Exibir disciplinas mais estudadas
- Exibir temas com mais revisões
- Mostrar comparação entre períodos
- Filtrar por disciplina específica
- Mostrar progresso ao longo do tempo

CRUDS POR ENTIDADE

CRUD USUÁRIO:
- Create: Cadastrar novo usuário (HU01)
- Read: Fazer login, visualizar perfil (HU02, HU03)
- Update: Alterar informações do perfil (HU04)
- Delete: Excluir conta (HU05)

CRUD DISCIPLINA:
- Create: Cadastrar nova disciplina (HU06)
- Read: Listar disciplinas, visualizar detalhes (HU06, HU12)
- Update: Editar disciplina (HU07)
- Delete: Excluir disciplina (HU08)

CRUD TEMA:
- Create: Cadastrar novo tema em disciplina (HU09)
- Read: Listar temas por disciplina (HU09, HU12)
- Update: Editar tema (HU10)
- Delete: Excluir tema (HU11)

CRUD REVISÃO:
- Create: Criada virtualmente ao cadastrar tema (HU09)
- Read: Listar revisões, filtrar, visualizar calendário (HU12, HU13, HU14)
- Update: Marcar como concluída, reagendar data (HU14, HU15)
- Delete: Excluir revisão específica (implícito em HU11)

CRUD CRONOGRAMA:
- Create: Registrar tempo de estudo (HU15)
- Read: Visualizar histórico de estudos (HU16)
- Update: Editar tempo dedicado (implícito)
- Delete: Excluir registro de estudo (implícito)

CRUD RELATÓRIO:
- Read: Visualizar relatórios e estatísticas (HU17, HU18)
- Export: Exportar dados

FILTROS IMPLEMENTADOS

- Filtrar disciplinas por nome (HU06)
- Filtrar temas por nome (HU09, HU13, HU15)
- Filtrar revisões por nome do tema (HU13, HU14)
- Filtrar revisões por disciplina (HU13)
- Filtrar revisões por status (HU13)
- Filtrar revisões por período (HU13)
- Filtrar cronograma por disciplina (HU16)
- Filtrar cronograma por tema (HU16)
- Filtrar cronograma por data (HU16)
- Filtrar relatórios por período (HU17, HU18)
- Filtrar relatórios por disciplina (HU17, HU18)

PRIORIDADES DE IMPLEMENTAÇÃO

ALTA PRIORIDADE (Mínimo testável):
- HU01, HU02, HU06, HU09, HU12, HU15

MÉDIA PRIORIDADE (Funcionalidades Essenciais):
- HU03, HU07, HU10, HU13, HU14, HU16

BAIXA PRIORIDADE (Melhorias):
- HU04, HU05, HU08, HU11, HU17, HU18