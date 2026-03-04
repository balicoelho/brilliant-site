# BrillIAnt — Site Oficial

> **Workshop "IA na Prática"** — Coloque a IA para trabalhar por você.

Site oficial da **BrillIAnt**, hospedado na Vercel em [brilliant.ia.br](https://brilliant.ia.br).

---

## Sobre o Projeto

A BrillIAnt oferece workshops presenciais de Inteligência Artificial para profissionais que querem usar IA no dia a dia — sem precisar saber programar. O workshop **"IA na Prática"** é um encontro hands-on com ferramentas reais, estratégias de prompt e aplicações práticas para o perfil de cada turma.

---

## Estrutura de Arquivos

```
brilliant-site/
├── index.html              # Site principal
├── feedback/
│   └── index.html          # Formulário de feedback das turmas
├── turma1.webp             # Foto da Turma 1 (02/03/2026)
├── vercel.json             # Configuração de roteamento da Vercel
├── .gitignore
└── README.md
```

---

## Páginas

### Site Principal — `/`

**URL:** [brilliant.ia.br](https://brilliant.ia.br)

O site apresenta o workshop e contém as seguintes seções:

| Seção | Descrição |
|---|---|
| **Hero** | Apresentação principal com chamada para ação |
| **Workshop** | Conteúdo do workshop "IA na Prática" e o que o aluno aprende |
| **Turmas** | Cards das turmas realizadas e abertura de inscrições |
| **Depoimentos** | Avaliações de participantes |
| **FAQ** | Perguntas frequentes |
| **Rodapé** | Links e contato |

**Seção de Turmas:**
- **Turma 1** — Realizada em 02 de Março de 2026 (Segunda-feira)
- **Turma 2** — Em breve (Março 2026) — com formulário de lista de espera integrado ao Google Sheets

### Formulário de Feedback — `/feedback`

**URL:** [brilliant.ia.br/feedback](https://brilliant.ia.br/feedback)

Formulário de avaliação pós-workshop com as seguintes perguntas:

- NPS (0–10) — Probabilidade de indicação
- Avaliação geral da experiência (1–5)
- Ferramentas favoritas utilizadas no workshop
- O que mais gostou
- O que poderia melhorar
- Sugestões / o que faltou
- Depoimento (com autorização de uso)
- Próximos passos de interesse
- Nome e e-mail (opcionais)

As respostas são enviadas via **Google Apps Script** e salvas automaticamente na planilha **"BrillIAnt — Feedback Workshop"** no Google Drive.

---

## Integrações

| Integração | Finalidade |
|---|---|
| **Google Sheets** | Lista de espera da Turma 2 e respostas do formulário de feedback |
| **Google Apps Script** | Web App que recebe os dados dos formulários e grava na planilha |
| **Vercel** | Hospedagem e deploy contínuo |

---

## Deploy

O site é hospedado na **Vercel** com domínio customizado `brilliant.ia.br`.

Para fazer um novo deploy:

```bash
vercel deploy --prod --token <VERCEL_TOKEN>
```

O arquivo `vercel.json` configura o roteamento para que `/feedback` sirva corretamente o formulário:

```json
{
  "rewrites": [
    { "source": "/feedback", "destination": "/feedback/index.html" },
    { "source": "/feedback/", "destination": "/feedback/index.html" }
  ]
}
```

---

## Contato

- **Instagram:** [@brilliant.ia.br](https://instagram.com/brilliant.ia.br)
- **Site:** [brilliant.ia.br](https://brilliant.ia.br)
