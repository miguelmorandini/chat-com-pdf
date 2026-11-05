# Roteiro da Apresentação Técnica: Chat com PDF & Databricks RAG

> **Duração Total:** 10 minutos cravados  
> **Apresentador:** Miguel Miranda Morandini  
> **Tema:** Sistemas de Retrieval-Augmented Generation (RAG) com Google Gemini, Mitigação Estrita de Alucinação e Ingestão Incremental CI/CD.  
> **Como Abrir a Apresentação:** Execute `python open_presentation.py` na raiz ou dê duplo clique em `presentation/open_presentation.bat`.

---

## Painel de Atalhos do Orador (Slide Deck)
| Tecla | Função |
| :---: | :--- |
| `→` ou `Espaço` | Próximo slide |
| `←` ou `Backspace` | Slide anterior |
| `N` | Abrir / Fechar gaveta de notas do orador (roteiro verbal) |
| `O` | Visão geral dos 9 slides em grade simétrica |
| `F` | Alternar modo de tela cheia |
| `T` | Iniciar / Pausar cronômetro integrado de 10 minutos |
| `Clique na Imagem` | Abre o modal de zoom em alta resolução |

---

## Pacing & Divisão de Tempo por Slide

```
[00:00 - 01:00] Slide 01: Capa Minimalista — O Desafio da IA Confiável
[01:00 - 02:00] Slide 02: A Inspiração — O Abismo da Confiança nos LLMs
[02:00 - 03:15] Slide 03: A Ideia Consolidada — Sua Base Técnica sem Alucinações
[03:15 - 04:30] Slide 04: Tecnologias & Conceitos — Arquitetura Enxuta
[04:30 - 05:45] Slide 05: O Desafio da Experiência Real — Como Construir Confiança
[05:45 - 07:00] Slide 06: Biomecânica / Inteligência do Domínio — Ingestão SHA-256
[07:00 - 08:15] Slide 07: Experimente Agora — Acesso Imediato & Código Aberto
[08:15 - 09:00] Slide 08: Metodologia de Engenharia (SDD / Qualidade)
[09:00 - 10:00] Slide 09: Encerramento ("Obrigado!") & Demonstração ao Vivo
```

---

## Roteiro Falado Slide a Slide (Em 1ª Pessoa, com Marcações de Palco)

### Slide 01: Capa Minimalista (0:00 - 1:00)
- **Marcação de Palco:** Postura ereta, olhar nos olhos dos avaliadores, sorriso tranquilo. Não toque no teclado logo de início; deixe a logo centralizada preencher a tela.
- **Roteiro Falado:**
  > *"Boa tarde a todos os presentes! Meu nome é Miguel e hoje quero apresentar a vocês o projeto **Chat com PDF & Databricks RAG**.*  
  > *A Inteligência Artificial Generativa virou manchete no mundo inteiro, mas quando nós saímos do mundo dos protótipos e tentamos aplicar esses modelos em ambientes de Engenharia, Finanças e Operações críticas, nós nos deparamos com uma barreira gigantesca: a falta de confiabilidade.*  
  > *O objetivo central deste projeto foi criar um sistema de ponta a ponta que conecta o poder cognitivo do Google Gemini a documentos corporativos densos, garantindo auditoria página por página e zero alucinação.*  
  > *Nas próximas telas, vou mostrar como estruturamos essa jornada técnica em duas etapas complementares e como resolvemos desafios de latência, escala e custo de API."*

---

### Slide 02: A Inspiração / O Problema Antigo (1:00 - 2:00)
- **Marcação de Palco:** Pressione `→`. [Gesto: apontar para a imagem na tela].
- **Roteiro Falado:**
  > *"A nossa faísca para este projeto nasceu de uma dor diária vivida por qualquer time de engenharia.*  
  > *De um lado, temos o velho e bom 'Ctrl + F'. Ele é útil, mas ele é puramente sintético: se você buscar por uma palavra-chave, ele acha 50 ocorrências soltas, mas não sintetiza uma explicação, não resume um capítulo e te obriga a ler um PDF de 500 páginas na unha.*  
  > *Do outro lado, temos o hype dos LLMs puros sem aterramento. Se você jogar um manual técnico para um modelo genérico, ele vai responder com um tom incrivelmente seguro... mas se ele não tiver certeza, ele inventa fatos com a maior tranquilidade do mundo — o que chamamos de alucinação.*  
  > *E no nosso mercado, uma instrução errada sobre transação ACID ou governança pode corromper tabelas de dados inteiras.*  
  > *A nossa provocação foi: e se pudéssemos unir a velocidade da busca vetorial à capacidade de síntese do Gemini, forçando o modelo a citar a fonte e proibindo qualquer invenção?"*

---

### Slide 03: A Ideia Consolidada (2:00 - 3:15)
- **Marcação de Palco:** Pressione `→`. [Gesto: abrir o modal de zoom clicando na imagem para mostrar a interface do Gradio e fechar com ESC ou clique].
- **Roteiro Falado:**
  > *"Foi aí que nasceu a nossa solução. Esta é uma captura real da nossa aplicação Gradio em execução.*  
  > *A proposta é elegante e sem atrito: o engenheiro faz upload de qualquer documento — aqui estamos analisando o eBook oficial da Databricks sobre Delta Lake — e conversa com o arquivo como se estivesse conversando com o autor do livro.*  
  > *Vejam o exemplo na tela: perguntamos o que é o Delta Lake e como ele traz confiabilidade. Em menos de 1.2 segundos, o sistema extrai o trecho exato, sintetiza os conceitos de Log de Transações e Parquet, e audita a resposta no rodapé citando as Páginas 3 e 8.*  
  > *E reparem no detalhe abaixo: quando fizemos uma pergunta deliberadamente fora de contexto — 'quem foi o campeão de futebol em 2002?' —, o assistente não tentou inventar uma metáfora; ele respondeu estritamente com a nossa frase de recusa padronizada: 'Não encontrei essa informação no documento.'.*  
  > *Desenvolvemos isso em duas camadas: uma leve em memória para PDFs avulsos e uma corporativa conectada ao sitemap oficial da Databricks."*

---

### Slide 04: Tecnologias & Conceitos (3:15 - 4:30)
- **Marcação de Palco:** Pressione `→`. [Gesto: percorrer com a mão a fileira horizontal dos 5 logos vetoriais].
- **Roteiro Falado:**
  > *"Para tornar essa experiência veloz, barata e sem atrito, desenhamos uma stack desacoplada de 5 pilares.*  
  > *No núcleo de engenharia, usamos **Python 3.12** com PyPDF2 para mapeamento estruturado de páginas físicas.*  
  > *O coração generativo é o **Google Gemini 3.5 Flash-Lite**, que escolhemos por aliar latência abaixo de um segundo a uma janela de contexto generosa e custo por milhão de tokens praticamente insignificante.*  
  > *Para a camada vetorial densa, utilizamos o modelo **gemini-embedding-001** de 768 dimensões com o **ChromaDB** para persistência em disco, somado a uma matriz esparsa TF-IDF em memória para buscas ad-hoc instantâneas.*  
  > *A interface interativa é em **Gradio**, permitindo que qualquer pessoa suba um PDF e comece o chat pelo navegador.*  
  > *E na ponta de automação, plugamos o **GitHub Actions** para rodar a varredura semanal da documentação oficial da Databricks a custo zero de servidor."*

---

### Slide 05: O Desafio da Experiência Real (4:30 - 5:45)
- **Marcação de Palco:** Pressione `→`. [Tom mais calmo e reflexivo: colocar-se no lugar do avaliador].
- **Roteiro Falado:**
  > *"Quando colocamos esse protótipo na mão de especialistas, nos deparamos com o maior desafio humano do projeto: como fazer um engenheiro sênior confiar na resposta da máquina?*  
  > *Nenhum profissional sério toma uma decisão técnica baseado em 'a inteligência artificial me disse'. Ele precisa da auditoria da fonte.*  
  > *Resolvemos essa fricção construindo o que chamamos de 'Prompt Shield'.*  
  > *Ele funciona em três camadas:*  
  > *Primeiro: no pré-processamento, limpamos capas e páginas sem densidade textual para evitar que ruído contamine a similaridade.*  
  > *Segundo: forçamos a injeção da etiqueta [Página X] em 100% dos blocos recuperados, obrigando o LLM a declarar a página correspondente.*  
  > *E terceiro: implementamos uma regra negativa intransponível. Se a similaridade for baixa ou o assunto não constar no arquivo, o modelo é bloqueado de usar seu conhecimento pré-treinado e é obrigado a emitir o escape padrão.*  
  > *Isso transforma a IA de um gerador de palpites em uma ferramenta de consulta formal auditável."*

---

### Slide 06: Biomecânica / Inteligência do Domínio (5:45 - 7:00)
- **Marcação de Palco:** Pressione `→`. [Tom entusiasta de quem resolveu um problema real de arquitetura de dados e custos].
- **Roteiro Falado:**
  > *"Quando expandimos o projeto para a base de conhecimento completa da Databricks, nos deparamos com o desafio de escala. A documentação oficial tem milhares de páginas e é atualizada continuamente.*  
  > *Se fôssemos reindexar todas as páginas toda semana, nós estouraríamos cotas de API, geraríamos latência e desperdiçaríamos dinheiro convertendo textos que não sofreram nenhuma alteração.*  
  > *Como resolvemos isso com inteligência de engenharia? Criamos um pipeline de ingestão incremental com hashing criptográfico SHA-256.*  
  > *O algoritmo baixa o sitemap oficial, filtra os tópicos de dados — como Lakehouse, Delta Lake, Unity Catalog e PySpark — e calcula o hash do conteúdo textual de cada página.*  
  > *Em seguida, ele compara esse hash com o nosso arquivo de estado em data/ingestion_state.json. Se o hash for idêntico, a página é ignorada imediatamente. Isso gera zero consumo de tokens!*  
  > *Apenas páginas novas ou alteradas são segmentadas em chunks e enviadas em lotes para a API de embeddings. E o GitHub Actions roda esse ciclo de forma autônoma todo domingo às 03:00 UTC, salvando o banco atualizado no repositório."*

---

### Slide 07: Experimente Agora (7:00 - 8:15)
- **Marcação de Palco:** Pressione `→`. [Convidar abertamente a banca: 'podem pegar seus smartphones e apontar para a tela agora mesmo'].
- **Roteiro Falado:**
  > *"Um dos nossos maiores compromissos foi com a reprodutibilidade imediata.*  
  > *Qualquer pessoa pode testar essa solução agora mesmo. Vocês podem apontar a câmera do celular para este QR Code ou acessar github.com/miguelmorandini/chat-com-pdf.*  
  > *No topo do README, nós disponibilizamos badges oficiais para abrir os notebooks no Google Colab com 1 clique.*  
  > *Você não precisa ter Python instalado, não precisa clonar repositório e não precisa configurar ambiente: basta abrir o Colab na nuvem, colar a sua chave gratuita do Google AI Studio e executar.*  
  > *E para quem quiser rodar localmente na máquina, basta clonar o repositório, executar 'python app.py' e a interface do Gradio sobe localmente em menos de 2 segundos."*

---

### Slide 08: Metodologia de Engenharia (SDD / Qualidade) (8:15 - 9:00)
- **Marcação de Palco:** Pressione `→`. [Postura técnica sênior, destacar os testes automatizados].
- **Roteiro Falado:**
  > *"Uma pergunta indispensável para qualquer banca técnica é: 'como vocês garantiram que essa arquitetura é sólida e livre de código descartável?'.*  
  > *A nossa resposta é a metodologia SDD: Spec-Driven Development.*  
  > *Em vez de sair programando no improviso em um notebook monolítico, nós especificamos os requisitos de cada etapa antes de escrever uma única linha.*  
  > *Definimos o contrato de chunking em 800 caracteres com 150 de overlap para preservar ideias completas, isolamos a lógica de ingestão na pasta src/ e criamos uma suíte de testes unitários contínuos no arquivo tests/test_incremental.py.*  
  > *Nossos testes validam a integridade dos metadados de URL, a divisão correta de blocos e o determinismo do cálculo de hash SHA-256. Cada linha de código no repositório atende a um propósito real validado por testes."*

---

### Slide 09: Encerramento ("Obrigado!") & Demonstração (9:00 - 10:00)
- **Marcação de Palco:** Pressione `→`. [Sorriso sincero, respirar fundo, olhar para todos da banca].
- **Roteiro Falado:**
  > *"Chegamos ao final da apresentação. Muito obrigado a todos pela atenção e pelo tempo!*  
  > *O projeto Chat com PDF & Databricks RAG prova que a Inteligência Artificial Generativa se torna verdadeiramente útil quando ancorada em boas práticas de engenharia de software, aterramento factual rigoroso e arquiteturas econômicas.*  
  > *Tivemos 100% de aprovação nos critérios do desafio, zero alucinações e uma esteira automatizada em produção.*  
  > *Estou totalmente à disposição para as perguntas da banca e podemos testar agora mesmo o Gradio com qualquer novo PDF que vocês queiram subir! Muito obrigado!"*

---

## Dicas Finais para o Sucesso da Apresentação
1. **Controle de Tempo Discreto:** Clique no botão `▶` ou pressione `T` assim que começar a falar no Slide 1. O cronômetro fica no canto superior direito e mudará para dourado aos 9 minutos.
2. **Uso das Teclas de Atalho:** Pratique navegar apenas com as setas do teclado para transmitir total domínio técnico.
3. **Se a Banca Pedir Demonstração:** Mantenha um terminal aberto em segundo plano com `python app.py` rodando. Se pedirem para ver ao vivo, dê um simples `Alt + Tab` para o navegador com o Gradio ativo.
