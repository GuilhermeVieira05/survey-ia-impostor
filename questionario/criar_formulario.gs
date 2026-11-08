/**
 * Cria os formulários da pesquisa "IA e síndrome do impostor" (questionário v0.2).
 * Fonte do texto: questionario/questionario.md (se mudar um, mude o outro).
 *
 * COMO USAR
 *  1. Entre em https://script.google.com com a conta do grupo e crie um "Novo projeto".
 *  2. Apague o código de exemplo, cole TODO este arquivo e troque EMAIL_GRUPO abaixo.
 *  3. Selecione a função  criarFormularios  e clique em Executar.
 *  4. Autorize o acesso quando o Google pedir (Formulários e Planilhas da própria conta).
 *  5. Abra Execuções / Registro de execução: os links aparecem lá.
 *
 * O QUE ELE CRIA (dois formulários separados, cada um com sua planilha de respostas)
 *  - "[PRÉ-TESTE] ..."  → ABERTO para respostas. É o que você manda para as 3–5 pessoas do pré-teste.
 *  - "Pesquisa: ..."    → FECHADO ("Aceitando respostas" desligado). Só abrir DEPOIS da entrega de 13/Nov.
 *
 * Rode UMA vez. Rodar de novo cria formulários duplicados.
 */

var VERSAO = '0.2';
var EMAIL_GRUPO = 'carlosdybala.fig@gmail.com'; // e-mail de contato exibido no consentimento

var TCLE =
  'Esta pesquisa faz parte de um trabalho da disciplina Medição em Engenharia de Software. ' +
  'Queremos entender como o uso de assistentes de IA (ChatGPT, GitHub Copilot, Claude, Gemini, Cursor etc.) ' +
  'se relaciona com a forma como desenvolvedores percebem a própria competência.\n\n' +
  '• Participação voluntária. Você pode desistir a qualquer momento, simplesmente fechando a página.\n' +
  '• Anônima. Não pedimos nome, e-mail ou qualquer dado que identifique você. Os resultados serão apresentados apenas de forma agregada.\n' +
  '• Duração: cerca de 4 minutos.\n' +
  '• Uso dos dados: exclusivamente acadêmico (análise estatística e apresentação em sala).\n' +
  '• Desconforto: algumas perguntas tratam de sentimentos sobre o próprio desempenho profissional. ' +
  'Se você se sentir incomodado(a), pode parar. Se precisar de apoio emocional, o CVV atende 24h pelo telefone 188.\n' +
  '• Dúvidas: __EMAIL__\n\n' +
  'Não há respostas certas ou erradas.';

var MSG_FINAL =
  'Obrigado(a) por participar! Suas respostas foram registradas de forma anônima. ' +
  'Se quiser ajudar, compartilhe a pesquisa com outros desenvolvedores. ' +
  'Se algum tema desta pesquisa te afetou, o CVV atende 24h pelo telefone 188 (ligação gratuita).';

var MSG_FECHADO =
  'Esta pesquisa ainda não está recebendo respostas. Obrigado pelo interesse!';

var TAREFAS = [
  // ATENÇÃO: nenhuma opção pode ter vírgula. O Google Forms grava as marcadas de B3 separadas por vírgula.
  'Gerar código novo (funções ou trechos de código)',
  'Completar ou refatorar código existente',
  'Depurar / corrigir bugs',
  'Escrever testes automatizados',
  'Escrever ou revisar documentação (README e comentários)',
  'Buscar informação / tirar dúvidas conceituais (substituindo busca na web)',
  'Entender ou explicar código existente'
];

var ITENS_LIS = [
  'C1. Às vezes fico assustado(a)/com medo de que serei descoberto(a) por quem eu realmente sou.',
  'C2. Eu costumo me sentir um(a) falso(a).',
  'C3. Tenho medo das pessoas que são importantes para mim, talvez descubram que não sou tão capaz como eles pensam que sou.',
  'C4. Em algumas situações me sinto como impostor(a).',
  'C5. Às vezes eu temo que outros descubram o quanto de conhecimento ou habilidade realmente me faltam.',
  'C6. Em algumas situações sinto-me como “um falso/impostor”; isto é, eu não sou tão genuíno(a) quanto as pessoas pensam que realmente eu sou.',
  'C7. Em algumas situações eu ajo como um impostor(a).'
];

function criarFormularios() {
  if (EMAIL_GRUPO.indexOf('PREENCHER') === 0) {
    throw new Error('Troque EMAIL_GRUPO no topo do script pelo e-mail de contato do grupo antes de rodar.');
  }
  var pre = construirFormulario_('[PRÉ-TESTE] Pesquisa: IA e síndrome do impostor (v' + VERSAO + ')', true);
  var oficial = construirFormulario_('Pesquisa: IA e síndrome do impostor', false);

  Logger.log('=== PRÉ-TESTE (aberto) ===');
  Logger.log('Link para responder: ' + pre.form.getPublishedUrl());
  Logger.log('Link para editar:    ' + pre.form.getEditUrl());
  Logger.log('Planilha:            ' + pre.ss.getUrl());
  Logger.log('=== OFICIAL (FECHADO até 13/Nov) ===');
  Logger.log('Link para responder: ' + oficial.form.getPublishedUrl());
  Logger.log('Link para editar:    ' + oficial.form.getEditUrl());
  Logger.log('Planilha:            ' + oficial.ss.getUrl());
}

function construirFormulario_(titulo, aceitandoRespostas) {
  var form = FormApp.create(titulo);
  form.setDescription(TCLE.replace('__EMAIL__', EMAIL_GRUPO));
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false); // exigiria login e quebraria o anonimato
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(MSG_FINAL);

  // ---------- Página 1: consentimento ----------
  var z1 = form.addMultipleChoiceItem();
  z1.setTitle('Z1. Li as informações acima e concordo em participar.').setRequired(true);
  z1.setChoices([
    z1.createChoice('Sim, concordo em participar', FormApp.PageNavigationType.CONTINUE),
    z1.createChoice('Não concordo', FormApp.PageNavigationType.SUBMIT)
  ]);

  // ---------- Página 2: A1 ----------
  form.addPageBreakItem().setTitle('Elegibilidade');
  var a1 = form.addMultipleChoiceItem();
  a1.setTitle('A1. Você tem 18 anos ou mais?').setRequired(true);
  a1.setChoices([
    a1.createChoice('Sim', FormApp.PageNavigationType.CONTINUE),
    a1.createChoice('Não', FormApp.PageNavigationType.SUBMIT)
  ]);

  // ---------- Página 3: A2 ----------
  form.addPageBreakItem().setTitle('Elegibilidade');
  var a2 = form.addMultipleChoiceItem();
  a2.setTitle('A2. Você atua (ou atuou nos últimos 12 meses) com desenvolvimento de software, seja em emprego, ' +
    'estágio, freelance ou projetos próprios remunerados?').setRequired(true);
  a2.setChoices([
    a2.createChoice('Sim', FormApp.PageNavigationType.CONTINUE),
    a2.createChoice('Não', FormApp.PageNavigationType.SUBMIT)
  ]);

  // ---------- Página 4: B1 ----------
  var paginaB1 = form.addPageBreakItem();
  paginaB1.setTitle('Uso de assistentes de IA');
  paginaB1.setHelpText('Considere assistentes de IA como ChatGPT, GitHub Copilot, Claude, Gemini, Cursor, entre outros, ' +
    'usados em atividades de desenvolvimento de software.');
  var b1 = form.addMultipleChoiceItem();
  b1.setTitle('B1. Nos últimos 3 meses, com que frequência você usou assistentes de IA nas suas atividades de desenvolvimento?')
    .setRequired(true);
  // as escolhas de B1 são definidas depois, quando a página da Seção C já existir

  // ---------- Página 5: B2, B3, B4 (só quem usa IA) ----------
  form.addPageBreakItem().setTitle('Uso de assistentes de IA (continuação)');

  var b2 = form.addMultipleChoiceItem();
  b2.setTitle('B2. Há quanto tempo você usa assistentes de IA no desenvolvimento?').setRequired(true);
  b2.setChoiceValues([
    'Menos de 6 meses',
    'De 6 meses a menos de 1 ano',
    'De 1 a 2 anos',
    'Mais de 2 anos'
  ]);

  var b3 = form.addCheckboxItem();
  b3.setTitle('B3. Para quais tarefas você usa assistentes de IA?').setRequired(true);
  b3.setHelpText('Marque todas que se aplicam.');
  b3.setChoiceValues(TAREFAS);
  b3.showOtherOption(true);

  var b4 = form.addMultipleChoiceItem();
  b4.setTitle('B4. Dentre as tarefas marcadas, qual você mais realiza com IA?').setRequired(true);
  b4.setHelpText('Escolha uma.');
  b4.setChoiceValues(TAREFAS.concat(['Outra tarefa (a que informei na pergunta anterior)']));

  // ---------- Página 6: Seção C (escala LIS) ----------
  var paginaC = form.addPageBreakItem();
  paginaC.setTitle('Como você se sente no trabalho');
  paginaC.setHelpText('Indique com que frequência cada afirmação descreve você, pensando em como se sente no seu ' +
    'trabalho com desenvolvimento de software.');

  var grade = form.addGridItem();
  grade.setTitle('Com que frequência cada afirmação descreve você?').setRequired(true);
  grade.setRows(ITENS_LIS);
  grade.setColumns(['1 - Nunca', '2', '3', '4', '5 - Quase sempre']);

  // ---------- Página 7: perfil ----------
  form.addPageBreakItem().setTitle('Perfil');

  var d1 = form.addMultipleChoiceItem();
  d1.setTitle('D1. Qual é o seu tempo total de experiência profissional com desenvolvimento de software?').setRequired(true);
  d1.setChoiceValues([
    'Menos de 1 ano',
    'De 1 a menos de 3 anos',
    'De 3 a menos de 5 anos',
    'De 5 a menos de 10 anos',
    '10 anos ou mais'
  ]);

  var d2 = form.addMultipleChoiceItem();
  d2.setTitle('D2. Qual é a sua faixa etária? (opcional)').setRequired(false);
  d2.setChoiceValues(['18 a 24', '25 a 34', '35 a 44', '45 ou mais', 'Prefiro não informar']);

  var d3 = form.addMultipleChoiceItem();
  d3.setTitle('D3. Qual é o seu gênero? (opcional)').setRequired(false);
  d3.setChoiceValues(['Feminino', 'Masculino', 'Outro', 'Prefiro não informar']);

  var d4 = form.addMultipleChoiceItem();
  d4.setTitle('D4. Como você ficou sabendo desta pesquisa?').setRequired(true);
  d4.setChoiceValues([
    'Grupo de WhatsApp / Telegram',
    'LinkedIn',
    'Discord / Slack / comunidade online',
    'Colega, amigo(a) ou professor(a)',
    'Outro'
  ]);

  // ---------- B1: "Nunca usei" pula B2–B4 e vai direto para a Seção C ----------
  b1.setChoices([
    b1.createChoice('Nunca usei', paginaC),
    b1.createChoice('Menos de uma vez por mês', FormApp.PageNavigationType.CONTINUE),
    b1.createChoice('Algumas vezes por mês', FormApp.PageNavigationType.CONTINUE),
    b1.createChoice('Algumas vezes por semana', FormApp.PageNavigationType.CONTINUE),
    b1.createChoice('Diariamente', FormApp.PageNavigationType.CONTINUE)
  ]);

  // ---------- Planilha de respostas (traz o "Carimbo de data/hora") ----------
  var ss = SpreadsheetApp.create('Respostas - ' + titulo);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // ---------- Aberto ou fechado ----------
  if (!aceitandoRespostas) {
    form.setCustomClosedFormMessage(MSG_FECHADO);
  }
  form.setAcceptingResponses(aceitandoRespostas);

  return { form: form, ss: ss };
}
