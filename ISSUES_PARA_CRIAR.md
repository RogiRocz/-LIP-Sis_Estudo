# Backlog de Issues para o Projeto Sis_Estudo

Aqui está uma lista completa de issues prontas para serem criadas no seu sistema de gerenciamento de projetos.

---

## Bloco 1: Funcionalidades Essenciais

### Issue: Gerenciamento de Disciplinas (CRUD)

**Descrição**

Como usuário, gostaria de poder cadastrar, editar e excluir minhas disciplinas para poder organizar meus temas de estudo de forma estruturada.

**Critérios de Aceite**

- [ ] A tela principal (ou uma tela de "Disciplinas") deve listar todas as disciplinas cadastradas.
- [ ] Um botão "Nova Disciplina" deve estar disponível para abrir um formulário de cadastro.
- [ ] O formulário deve permitir inserir o nome da disciplina, uma cor de identificação e uma descrição (opcional).
- [ ] Cada disciplina na lista deve ter opções para "Editar" e "Excluir".
- [ ] A ação de "Excluir" deve exibir um alerta de confirmação, informando que todos os temas e revisões associados também serão removidos.

---

### Issue: Gerenciamento de Temas de Estudo

**Descrição**

Como usuário, gostaria de poder adicionar, editar e remover os temas de estudo de cada uma das minhas disciplinas para manter meu material organizado e atualizado.

**Critérios de Aceite**

- [ ] A tela de detalhes da disciplina deve listar todos os temas cadastrados para ela.
- [ ] Deve existir um botão para "Adicionar Tema" que abre um formulário (em um modal ou em uma nova página).
- [ ] O formulário de adição deve permitir inserir, no mínimo, o nome do tema e uma descrição (opcional).
- [ ] Cada tema na lista deve ter uma opção visível para "Editar", que abre o mesmo formulário, porém pré-preenchido com os dados do tema.
- [ ] Cada tema na lista deve ter uma opção visível para "Excluir".
- [ ] Ao clicar em "Excluir", o sistema deve pedir uma confirmação antes de remover permanentemente o tema.

---

### Issue: Gerenciamento de Revisões no Calendário

**Descrição**

Como usuário, ao visualizar uma revisão no meu cronograma, gostaria de poder marcá-la como concluída ou reagendá-la para outra data, de forma rápida e intuitiva.

**Critérios de Aceite**

- [ ] Ao clicar em uma revisão no calendário, um modal com os detalhes da revisão deve ser exibido.
- [ ] O modal deve ter uma ação clara para "Concluir Revisão".
- [ ] Ao concluir, o usuário deve obrigatoriamente informar o tempo em minutos que levou para estudar (`tempo_minutos`).
- [ ] Após a conclusão, a revisão deve ser marcada como "REALIZADA" e sua aparência no calendário deve mudar (ex: cor diferente, ícone de "check").
- [ ] O modal deve ter uma ação para "Reagendar", que permite ao usuário escolher uma nova data futura para a revisão.
- [ ] Após o reagendamento, a revisão deve ser movida para a nova data no calendário.

---

### Issue: Filtros no Cronograma de Revisões

**Descrição**

Como usuário, gostaria de poder filtrar meu cronograma de revisões por disciplina e por status, para que eu possa focar meus estudos em tarefas específicas ou ver apenas o que está pendente.

**Critérios de Aceite**

- [ ] Na tela do calendário/cronograma, deve existir um campo de filtro (ex: dropdown) para selecionar uma disciplina específica.
- [ ] Ao selecionar uma disciplina, o cronograma deve ser atualizado para exibir apenas as revisões daquela disciplina.
- [ ] Devem existir opções (ex: botões, abas) para filtrar as revisões por status: "Pendentes", "Concluídas" e "Atrasadas".
- [ ] Os filtros de disciplina e status devem poder ser combinados (ex: mostrar revisões "Atrasadas" da disciplina "Cálculo").
- [ ] **[Backend Task]** O endpoint `GET /revisoes` deve ser modificado para aceitar parâmetros de query para `disciplina_id` e `status`.

---

## Bloco 2: Relatórios e Perfil

### Issue: Visualização de Relatórios de Desempenho

**Descrição**

Como usuário, gostaria de ver relatórios e estatísticas dos meus estudos para entender meu progresso, ver onde estou dedicando mais tempo e identificar minhas disciplinas mais fortes e fracas.

**Critérios de Aceite**

- [ ] Uma nova tela de "Relatórios" deve ser criada no sistema.
- [ ] A tela deve exibir, no mínimo, o tempo total de estudo (soma de todos os `tempo_minutos`) por disciplina.
- [ ] A tela deve mostrar a quantidade total de revisões realizadas versus o total de revisões pendentes/atrasadas.
- [ ] A tela deve incluir um filtro que permita ao usuário selecionar o período do relatório (ex: última semana, último mês, período customizado).
- [ ] **[Backend Task]** Um endpoint (`GET /relatorios/desempenho`) deve ser criado para fornecer os dados já calculados e agregados.
- [ ] **[Frontend Task]** A interface deve consumir os dados do novo endpoint e exibi-los em formato de tabela e/ou gráficos.

---

### Issue: Exportação de Relatório para PDF

**Descrição**

Como usuário, gostaria de poder exportar meu relatório de desempenho para um arquivo PDF, para poder salvá-lo, imprimi-lo ou compartilhá-lo.

**Critérios de Aceite**

- [ ] Na tela de "Relatórios", deve haver um botão "Exportar para PDF".
- [ ] Ao clicar no botão, o relatório referente ao período atualmente selecionado no filtro deve ser gerado em formato PDF.
- [ ] O navegador deve iniciar o download automático do arquivo PDF gerado.
- [ ] **[Backend Task]** Um endpoint (`GET /relatorios/exportar/pdf`) deve ser criado para receber a requisição e gerar o arquivo PDF.
- [ ] **[Frontend Task]** O clique no botão deve chamar o endpoint do backend, passando os filtros de data, e gerenciar o download.

---

### Issue: Visualização e Edição de Perfil de Usuário

**Descrição**

Como usuário, gostaria de poder visualizar e editar as informações do meu perfil, como e-mail, senha e preferências de estudo, para manter minha conta segura e personalizada.

**Critérios de Aceite**

- [ ] Uma tela de "Perfil" ou "Configurações" deve ser acessível no sistema.
- [ ] A tela deve exibir informações do usuário, como o e-mail de cadastro e a data de criação da conta.
- [ ] A tela deve permitir a alteração do e-mail do usuário (com validação de e-mail único).
- [ ] A tela deve permitir a alteração da senha (com campos para senha atual, nova senha e confirmação da nova senha).
- [ ] A tela deve permitir que o usuário altere suas preferências, como o intervalo de revisões padrão e o tema da interface (claro/escuro).

---

## Bloco 3: Melhorias de Usabilidade (UI/UX)

### Issue: Feedback Visual para Ações do Usuário

**Descrição**

Como usuário, gostaria de receber uma notificação visual clara sempre que eu realizar uma ação importante (como salvar, editar ou excluir algo), para que eu tenha certeza de que a ação foi concluída com sucesso ou se ocorreu um erro.

**Critérios de Aceite**

- [ ] Após uma operação bem-sucedida (ex: "Disciplina criada com sucesso"), uma notificação "toast" de sucesso deve aparecer brevemente na tela.
- [ ] Se uma operação falhar por qualquer motivo (ex: erro de validação, falha na API), uma notificação de erro deve aparecer, informando o problema.
- [ ] A implementação deve ser genérica o suficiente para ser reutilizada em todos os formulários e ações do sistema.

---

### Issue: Indicadores de Carregamento (Loading)

**Descrição**

Como usuário, quando uma página precisa carregar dados do servidor, gostaria de ver um indicador visual de carregamento (como um "spinner" ou "skeleton screen") para saber que o sistema está processando minha solicitação e não está travado.

**Critérios de Aceite**

- [ ] Sempre que uma chamada de API for iniciada para buscar dados (ex: carregar a lista de disciplinas ou as revisões do calendário), um indicador de carregamento deve ser exibido.
- [ ] O indicador de carregamento deve desaparecer assim que os dados forem carregados e exibidos na tela.
- [ ] Em caso de erro na chamada da API, o indicador de carregamento também deve desaparecer e uma mensagem de erro deve ser mostrada.

---

## Bloco 4: Tarefas Técnicas e de Qualidade

### Issue: [Técnica] Criação de Dados de Teste Realistas

**Descrição**

Como desenvolvedor, gostaria de um script que popule o banco de dados com dados de teste realistas para poder desenvolver e testar as funcionalidades de calendário e relatórios de forma eficaz, simulando um ambiente de uso real.

**Critérios de Aceite**

- [ ] O script deve ser capaz de criar múltiplos usuários, cada um com seu próprio conjunto de disciplinas e temas.
- [ ] O script deve gerar um cronograma de revisões que se estenda por vários meses (ex: de Dezembro de 2024 até a data atual).
- [ ] As revisões geradas devem ter status variados e bem distribuídos (REALIZADA, PENDENTE, ATRASADA).
- [ ] As revisões com status "REALIZADA" devem ter o campo `tempo_minutos` preenchido com valores aleatórios e realistas.
- [ ] O script deve poder ser executado várias vezes sem criar dados duplicados (deve ser idempotente).

---

### Issue: [Técnica] Configurar Base de Testes para o Backend (API)

**Descrição**

Como desenvolvedor, gostaria de configurar uma estrutura de testes automatizados para a API do backend, para garantir a estabilidade do sistema, evitar regressões futuras e validar a lógica de negócio.

**Critérios de Aceite**

- [ ] A biblioteca `pytest` deve ser adicionada como dependência de desenvolvimento no backend.
- [ ] Uma estrutura de pastas para os testes (ex: `/tests`) deve ser criada.
- [ ] Pelo menos um teste de API inicial deve ser escrito para um endpoint crítico (ex: login ou criação de disciplina), utilizando o `TestClient` do FastAPI.

---

### Issue: [Técnica] Configurar Base de Testes para o Frontend (Unitário)

**Descrição**

Como desenvolvedor, gostaria de configurar uma estrutura de testes unitários para o frontend, para garantir que a lógica de componentes, stores (Pinia) e funções utilitárias funcione como esperado.

**Critérios de Aceite**

- [ ] A biblioteca `Vitest` (ou outra de sua preferência) deve ser adicionada como dependência de desenvolvimento no frontend.
- [ ] A configuração necessária para executar os testes no ambiente Vite deve ser criada.
- [ ] Pelo menos um teste unitário inicial deve ser escrito para uma função simples (ex: uma action de um store Pinia ou uma função utilitária de formatação de data).
