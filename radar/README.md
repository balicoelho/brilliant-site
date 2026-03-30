# 🚀 Radar da Semana BrillIAnt

Automação completa para gerar, publicar e compartilhar o Radar da Semana BrillIAnt — uma curadoria semanal das novidades mais relevantes do mundo da Inteligência Artificial.

## 📋 Visão Geral

O Radar da Semana BrillIAnt é um projeto automatizado que:

1. **Busca notícias** sobre as ferramentas de IA mais relevantes
2. **Gera um podcast narrado** em português com voz feminina profissional
3. **Cria páginas HTML** com as matérias completas
4. **Publica automaticamente** no GitHub e Vercel
5. **Gera um link único** para compartilhar no WhatsApp

Tudo isso acontece **automaticamente toda segunda-feira às 7h da manhã**.

## 🏗️ Estrutura do Projeto

```
brilliant-radar/
├── .github/workflows/
│   └── gerar-radar-semanal.yml      # GitHub Actions (agendamento)
├── scripts/
│   ├── generate_radar.py            # Script principal
│   ├── config.yaml                  # Configurações
│   └── requirements.txt             # Dependências Python
├── templates/
│   ├── radar_template.html          # Template do Radar
│   ├── materia_template.html        # Template das matérias
│   └── index_template.html          # Template da página principal
├── radares/
│   ├── 2026-03-24/                  # Pasta de cada semana
│   │   ├── index.html               # Página do Radar
│   │   ├── podcast.mp3              # Áudio gerado
│   │   ├── materia_1.html           # Matérias
│   │   ├── materia_2.html
│   │   ├── materia_3.html
│   │   ├── materia_4.html
│   │   ├── materia_5.html
│   │   └── dados.json               # Dados estruturados
│   └── 2026-03-17/                  # Semanas anteriores
├── dados_semanais/
│   └── noticias_2026-03-24.json     # Notícias da semana
├── public/
│   ├── css/
│   │   └── style.css                # Estilos compartilhados
│   ├── js/
│   │   └── main.js                  # Scripts compartilhados
│   └── assets/
│       └── logo.png                 # Logo BrillIAnt
├── config.yaml                      # Configuração principal
├── vercel.json                      # Configuração Vercel
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Pré-requisitos

- Python 3.11+
- Conta no Google Cloud (para TTS)
- Conta no GitHub
- Conta na Vercel (opcional, para deploy)

### 2. Configuração Inicial

#### 2.1 Clonar o repositório

```bash
git clone https://github.com/balicoelho/brilliant-site.git
cd brilliant-site
```

#### 2.2 Instalar dependências

```bash
pip install -r scripts/requirements.txt
```

#### 2.3 Configurar Google Cloud

1. Criar um projeto no [Google Cloud Console](https://console.cloud.google.com)
2. Ativar a API "Text-to-Speech"
3. Criar uma chave de serviço (Service Account Key)
4. Baixar o arquivo JSON
5. Adicionar como secret no GitHub: `GOOGLE_CLOUD_KEY`

#### 2.4 Configurar GitHub Actions

Adicione os seguintes secrets no repositório:

- `GOOGLE_CLOUD_KEY`: Conteúdo do arquivo JSON do Google Cloud
- `GITHUB_TOKEN`: Token de acesso do GitHub (padrão)
- `VERCEL_DEPLOY_HOOK`: URL do webhook da Vercel (opcional)

### 3. Usar o Sistema

#### 3.1 Criar arquivo de notícias

Crie um arquivo `dados_semanais/noticias_YYYY-MM-DD.json` com as 5 notícias:

```json
{
  "semana": "2026-03-24",
  "data_inicio": "24 de março",
  "data_fim": "30 de março",
  "noticias": [
    {
      "numero": 1,
      "ferramenta": "ChatGPT",
      "empresa": "OpenAI",
      "titulo": "O ChatGPT agora tem uma gaveta só sua",
      "resumo": "A OpenAI lançou a Library...",
      "highlight": "Use o ChatGPT como seu assistente pessoal...",
      "conteudo_completo": "<p>Conteúdo HTML completo da matéria</p>"
    },
    // ... mais 4 notícias
  ]
}
```

#### 3.2 Rodar o script manualmente

```bash
python scripts/generate_radar.py
```

#### 3.3 Agendamento automático

O GitHub Actions roda automaticamente toda **segunda-feira às 7h da manhã** (horário de Brasília).

Para rodar manualmente:
1. Vá para "Actions" no GitHub
2. Selecione "Gerar Radar da Semana"
3. Clique "Run workflow"

## 📝 Formato do JSON de Notícias

Cada notícia deve ter:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `numero` | int | 1-5 |
| `ferramenta` | string | Nome da ferramenta (ex: ChatGPT) |
| `empresa` | string | Empresa (ex: OpenAI) |
| `titulo` | string | Título da notícia |
| `resumo` | string | Resumo curto (máx 3 linhas) |
| `highlight` | string | O que muda na rotina? |
| `conteudo_completo` | string | HTML com conteúdo completo |

## 🎙️ Configuração de Áudio

O arquivo `config.yaml` controla:

```yaml
podcast:
  voz: "pt-BR-Neural2-C"      # Voz feminina Google Cloud
  velocidade: 0.95            # 95% da velocidade normal
  pitch: 0                    # Sem variação de tom
```

## 🔗 Links Gerados

Após gerar o Radar, você terá:

- **GitHub**: `https://github.com/balicoelho/brilliant-site/tree/main/radares/2026-03-24`
- **Domínio**: `https://brilliant.com.br/radar/2026-03-24/`
- **WhatsApp**: Compartilhe o link do domínio

## 📊 Fluxo de Automação

```
Segunda-feira 7h
    ↓
GitHub Actions dispara
    ↓
Script Python:
  1. Lê noticias_YYYY-MM-DD.json
  2. Gera roteiro SSML
  3. Cria podcast MP3 (Google Cloud TTS)
  4. Gera HTML das matérias
  5. Cria página do Radar
  6. Atualiza index principal
    ↓
Commit e Push para GitHub
    ↓
Webhook dispara deploy na Vercel
    ↓
Link público disponível para compartilhar
```

## 💰 Economia de Créditos

| Serviço | Custo | Notas |
|---------|-------|-------|
| Google Cloud TTS | ~$0.50-1.00/semana | 52 segundos de áudio |
| GitHub Actions | Gratuito | Até 2000 min/mês |
| Vercel | Gratuito | Plano estático |
| **Total mensal** | ~$2-4 | Praticamente nada! |

## 🔧 Troubleshooting

### Erro: "GOOGLE_APPLICATION_CREDENTIALS not found"

Verifique se o secret `GOOGLE_CLOUD_KEY` está configurado no GitHub.

### Erro: "File not found: noticias_YYYY-MM-DD.json"

Crie o arquivo JSON na pasta `dados_semanais/` com a data correta.

### Podcast não gerado

Verifique:
1. Google Cloud TTS está ativado
2. Credenciais estão corretas
3. Quota não foi excedida

### Deploy não dispara na Vercel

Verifique se o secret `VERCEL_DEPLOY_HOOK` está configurado.

## 📚 Documentação Adicional

- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Vercel Deployment](https://vercel.com/docs)

## 🤝 Contribuindo

Para sugerir melhorias ou reportar bugs, abra uma issue no repositório.

## 📄 Licença

MIT

## 👋 Suporte

Para dúvidas ou problemas, entre em contato com a equipe BrillIAnt.

---

**Última atualização**: 30 de março de 2026
