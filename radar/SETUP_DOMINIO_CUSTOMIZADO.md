# 🚀 Setup: Radar BrillIAnt com Domínio Customizado

## Visão Geral

Este guia é específico para publicar o Radar no seu domínio: **`brilliant.com.br/radar`**

Você já tem hospedagem configurada no Manus, então o processo é mais simples!

---

## 📋 Checklist Rápido

- [x] Repositório GitHub: `balicoelho/brilliant-site`
- [x] Domínio: `brilliant.com.br/radar`
- [x] Hospedagem: Configurada no Manus
- [x] Automação: GitHub Actions toda segunda-feira 7h

---

## PASSO 1: Preparar o Repositório GitHub

### 1.1 Clonar seu repositório

```bash
git clone https://github.com/balicoelho/brilliant-site.git
cd brilliant-site
```

### 1.2 Criar pasta para o Radar

```bash
mkdir -p radar
cd radar
```

### 1.3 Copiar todos os arquivos

Copie todos os arquivos de `/home/ubuntu/brilliant-radar-github/` para a pasta `radar/` do seu repositório:

```
brilliant-site/
├── radar/
│   ├── .github/
│   │   └── workflows/
│   │       └── gerar-radar-semanal.yml
│   ├── scripts/
│   │   ├── generate_radar.py
│   │   ├── config.yaml
│   │   └── requirements.txt
│   ├── templates/
│   │   ├── radar_template.html
│   │   ├── materia_template.html
│   │   └── index_template.html
│   ├── radares/
│   │   └── 2026-03-24/
│   ├── dados_semanais/
│   │   └── noticias_2026-03-24.json
│   ├── public/
│   │   └── css/
│   │       └── style.css
│   ├── config.yaml
│   ├── README.md
│   └── PROMPT_TAREFA_AGENDADA_MANUS.md
```

### 1.4 Fazer commit e push

```bash
git add .
git commit -m "🚀 Adicionar Radar da Semana BrillIAnt"
git push origin main
```

---

## PASSO 2: Configurar Google Cloud TTS

### 2.1 Criar projeto no Google Cloud

1. Acesse [console.cloud.google.com](https://console.cloud.google.com)
2. Clique no dropdown de projeto (canto superior esquerdo)
3. Clique "NEW PROJECT"
4. Nome: `Radar BrillIAnt`
5. Clique "CREATE"

### 2.2 Ativar API Text-to-Speech

1. No console, procure por "Text-to-Speech"
2. Clique na API
3. Clique "ENABLE"

### 2.3 Criar Service Account

1. Vá para "APIs & Services" → "Credentials"
2. Clique "Create Credentials" → "Service Account"
3. Preencha:
   - **Service account name**: `radar-bot`
4. Clique "CREATE AND CONTINUE"
5. Clique "CONTINUE" (sem adicionar roles)
6. Clique "DONE"

### 2.4 Criar chave JSON

1. Na página de Credentials, clique em "Service Accounts"
2. Clique na conta `radar-bot@...`
3. Vá para aba "KEYS"
4. Clique "Add Key" → "Create new key"
5. Selecione "JSON"
6. Clique "CREATE"
7. Um arquivo será baixado

### 2.5 Adicionar role de TTS

1. Volte para o projeto no Google Cloud Console
2. Vá para "IAM & Admin" → "IAM"
3. Clique no email da service account
4. Clique "Edit principal"
5. Clique "Add another role"
6. Procure por "Text-to-Speech"
7. Selecione "Cloud Text-to-Speech API User"
8. Clique "SAVE"

---

## PASSO 3: Configurar GitHub Actions

### 3.1 Adicionar secrets no GitHub

1. Vá para seu repositório: `https://github.com/balicoelho/brilliant-site`
2. Clique "Settings" → "Secrets and variables" → "Actions"
3. Clique "New repository secret"

#### Secret 1: GOOGLE_CLOUD_KEY

1. Abra o arquivo JSON que você baixou do Google Cloud
2. Copie **TODO** o conteúdo
3. Crie um secret chamado `GOOGLE_CLOUD_KEY`
4. Cole o conteúdo JSON

#### Secret 2: GITHUB_TOKEN

1. Vá para [github.com/settings/tokens](https://github.com/settings/tokens)
2. Clique "Generate new token" → "Generate new token (classic)"
3. Nome: `Radar Bot Token`
4. Selecione escopos:
   - ✅ `repo`
   - ✅ `workflow`
5. Clique "Generate token"
6. Copie o token
7. Crie um secret chamado `GITHUB_TOKEN` no seu repositório

### 3.2 Testar GitHub Actions

1. Vá para "Actions" no seu repositório
2. Clique "Gerar Radar da Semana"
3. Clique "Run workflow" → "Run workflow"
4. Aguarde ~10 minutos

Se tudo correr bem, você verá ✅ em verde.

---

## PASSO 4: Configurar Hospedagem no Manus

Como você já tem hospedagem configurada no Manus, você precisa:

### 4.1 Apontar para a pasta `radar/`

Na configuração do seu site no Manus:
- **Root Directory**: `radar/`
- **Build Command**: `npm run build` (ou deixe em branco se for HTML estático)
- **Output Directory**: `radares/`

### 4.2 Configurar redirecionamento de URLs

Para que as URLs fiquem limpas (sem `.html`), configure:

```
/radar/2026-03-24/ → /radar/radares/2026-03-24/index.html
/radar/2026-03-24/materia_1.html → /radar/radares/2026-03-24/materia_1.html
```

Isso depende do seu hosting. Se estiver usando Manus, verifique a documentação de rewrite de URLs.

---

## PASSO 5: Testar Fluxo Completo

### 5.1 Criar arquivo de teste

1. Vá para seu repositório no GitHub
2. Vá para `radar/dados_semanais/`
3. Clique "Add file" → "Create new file"
4. Nome: `noticias_2026-03-30.json`
5. Cole o conteúdo de exemplo (veja abaixo)
6. Clique "Commit changes"

**Conteúdo de exemplo:**

```json
{
  "semana": "2026-03-30",
  "data_inicio": "30 de março",
  "data_fim": "5 de abril",
  "noticias": [
    {
      "numero": 1,
      "ferramenta": "ChatGPT",
      "empresa": "OpenAI",
      "titulo": "O ChatGPT agora tem uma gaveta só sua",
      "resumo": "A OpenAI lançou a Library: um espaço seguro onde todos os seus arquivos ficam salvos automaticamente.",
      "highlight": "Use o ChatGPT como seu assistente pessoal de arquivos.",
      "conteudo_completo": "<p>A OpenAI lançou a <strong>Library</strong>...</p>"
    },
    {
      "numero": 2,
      "ferramenta": "Gemini",
      "empresa": "Google",
      "titulo": "Mudando de IA sem perder a memória",
      "resumo": "O Google Gemini agora permite importar histórico de conversas.",
      "highlight": "Quer testar o Gemini? Agora você traz sua bagagem em segundos.",
      "conteudo_completo": "<p>O Google Gemini agora permite importar...</p>"
    },
    {
      "numero": 3,
      "ferramenta": "Claude",
      "empresa": "Anthropic",
      "titulo": "O Claude agora mexe no seu mouse e teclado",
      "resumo": "A Anthropic liberou o Computer Use.",
      "highlight": "Aquela tarefa repetitiva? Peça para o Claude fazer.",
      "conteudo_completo": "<p>A Anthropic liberou o Computer Use...</p>"
    },
    {
      "numero": 4,
      "ferramenta": "NotebookLM",
      "empresa": "Google",
      "titulo": "Seus resumos chatos viraram vídeos de cinema",
      "resumo": "NotebookLM transforma documentos em vídeos cinemáticos.",
      "highlight": "Precisa apresentar um relatório? Transforme em vídeo.",
      "conteudo_completo": "<p>O NotebookLM do Google acaba de ganhar superpoderes...</p>"
    },
    {
      "numero": 5,
      "ferramenta": "Suno",
      "empresa": "v5.5",
      "titulo": "Crie músicas incríveis usando a sua voz",
      "resumo": "Suno 5.5 com Voices: grave um áudio e a IA cria uma música.",
      "highlight": "Quer criar um jingle? A IA afina e produz tudo.",
      "conteudo_completo": "<p>O Suno lançou a versão 5.5 com a função Voices...</p>"
    }
  ]
}
```

### 5.2 Disparar GitHub Actions manualmente

1. Vá para "Actions" no seu repositório
2. Clique "Gerar Radar da Semana"
3. Clique "Run workflow" → "Run workflow"
4. Aguarde ~10 minutos

### 5.3 Verificar resultado

Se tudo correr bem:

1. ✅ GitHub Actions completou com sucesso
2. ✅ Novo commit foi feito em `radar/radares/2026-03-30/`
3. ✅ Seu site foi atualizado
4. ✅ Acesse `https://brilliant.com.br/radar/2026-03-30/`

---

## PASSO 6: Agendar Tarefa do Manus

### 6.1 Criar tarefa agendada

1. Abra o Manus
2. Clique "Schedule Task"
3. Configure:
   - **Name**: "Buscar Notícias BrillIAnt"
   - **Type**: `cron`
   - **Cron**: `0 6 * * 0` (Domingo 6h UTC = Domingo 3h Brasília)
   - **Timezone**: `America/Recife`
   - **Repeat**: `true`

4. **Prompt**: Cole o conteúdo do arquivo `PROMPT_TAREFA_AGENDADA_MANUS.md`

5. Clique "Schedule"

### 6.2 Testar tarefa

1. Vá para "Scheduled Tasks"
2. Clique em "Buscar Notícias BrillIAnt"
3. Clique "Run Now"
4. Aguarde ~5 minutos
5. Verifique se o arquivo JSON foi criado no GitHub

---

## PASSO 7: Automação Completa

Após configurar tudo, seu fluxo será:

| Dia | Hora | O que acontece |
|-----|------|----------------|
| Domingo | 6h (Brasília) | Manus busca notícias e salva JSON no GitHub |
| Segunda | 7h (Brasília) | GitHub Actions lê JSON e gera Radar |
| Segunda | 7h:15 (Brasília) | Seu site é atualizado |
| Segunda | 7h:30 (Brasília) | Link pronto para compartilhar no WhatsApp |

---

## 📍 URLs Finais

Após tudo configurado:

- **Página principal**: `https://brilliant.com.br/radar/`
- **Radar da semana**: `https://brilliant.com.br/radar/2026-03-24/`
- **Matérias**: `https://brilliant.com.br/radar/2026-03-24/materia_1.html`
- **Compartilhar**: `https://brilliant.com.br/radar/2026-03-24/`

---

## 🔧 Customizações

### Mudar horário de agendamento

Edite `.github/workflows/gerar-radar-semanal.yml`:

```yaml
schedule:
  - cron: '0 10 * * 1'  # Mude para seu horário
```

### Mudar velocidade do podcast

Edite `config.yaml`:

```yaml
podcast:
  velocidade: 0.90  # Mais lento
```

### Adicionar mais ferramentas

Edite `PROMPT_TAREFA_AGENDADA_MANUS.md` e adicione na lista.

---

## ❌ Troubleshooting

### Erro: "GOOGLE_CLOUD_KEY not found"

Verifique se o secret foi adicionado corretamente no GitHub.

### Erro: "File not found: noticias_YYYY-MM-DD.json"

Verifique se o arquivo JSON está em `radar/dados_semanais/` com a data correta.

### GitHub Actions falha

Clique em "Actions" → Clique no workflow que falhou → Veja os logs.

### Site não atualiza

Verifique se o Manus está configurado para fazer rebuild automático.

---

## ✅ Checklist Final

- [ ] Repositório GitHub clonado e arquivos copiados
- [ ] Google Cloud TTS configurado
- [ ] Secrets adicionados no GitHub
- [ ] GitHub Actions testado manualmente
- [ ] Hospedagem no Manus configurada
- [ ] URLs reescritas corretamente
- [ ] Tarefa do Manus agendada
- [ ] Fluxo completo testado

---

**Pronto! Seu Radar está 100% automatizado! 🚀**

Toda segunda-feira, um novo Radar será publicado em `https://brilliant.com.br/radar/`

---

**Última atualização**: 30 de março de 2026
