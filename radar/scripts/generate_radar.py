#!/usr/bin/env python3
"""
Script para gerar o Radar da Semana BrillIAnt automaticamente.

Fluxo:
1. Lê o arquivo JSON com as notícias da semana
2. Gera o podcast em MP3 usando Google Cloud TTS
3. Cria os arquivos HTML das matérias
4. Atualiza a página principal com a nova semana
5. Faz commit e push para GitHub
6. Dispara deploy na Vercel
"""

import os
import json
import yaml
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from google.cloud import texttospeech
from jinja2 import Template
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RadarGenerator:
    def __init__(self, config_path="config.yaml"):
        """Inicializar o gerador com configurações."""
        self.config_path = Path(config_path)
        self.project_root = self.config_path.parent
        
        # Carregar configuração
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        logger.info("✅ Configuração carregada")
        
        # Inicializar cliente Google Cloud TTS
        self.tts_client = texttospeech.TextToSpeechClient()
        logger.info("✅ Cliente Google Cloud TTS inicializado")
    
    def carregar_dados_semana(self, data_str=None):
        """
        Carregar dados da semana do arquivo JSON.
        
        Args:
            data_str: Data no formato YYYY-MM-DD (padrão: hoje)
        
        Returns:
            dict: Dados da semana com as 5 notícias
        """
        if not data_str:
            # Usar segunda-feira da semana atual
            hoje = datetime.now()
            dias_atras = (hoje.weekday() - 0) % 7  # 0 = segunda
            segunda = hoje - timedelta(days=dias_atras)
            data_str = segunda.strftime("%Y-%m-%d")
        
        arquivo_json = self.project_root / self.config['github']['pasta_dados'] / f"noticias_{data_str}.json"
        
        if not arquivo_json.exists():
            logger.error(f"❌ Arquivo não encontrado: {arquivo_json}")
            raise FileNotFoundError(f"Arquivo de notícias não encontrado: {arquivo_json}")
        
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        logger.info(f"✅ Dados carregados: {len(dados['noticias'])} notícias")
        return dados
    
    def gerar_roteiro_podcast(self, dados):
        """
        Gerar o roteiro do podcast em SSML.
        
        Args:
            dados: Dados da semana com as notícias
        
        Returns:
            str: Roteiro em formato SSML
        """
        roteiro = f"""<speak>
  <prosody rate="{self.config['podcast']['velocidade']}" pitch="{self.config['podcast']['pitch']}%">
    <s>Olá, este é o Radar da Semana BrillIAnt.</s>
    <break time="500ms"/>
    <s>Trazendo as novidades mais quentes do mundo da inteligência artificial para facilitar a sua rotina.</s>
  </prosody>
  
  <break time="1000ms"/>
"""
        
        # Adicionar cada notícia
        for noticia in dados['noticias']:
            roteiro += f"""  <prosody rate="{self.config['podcast']['velocidade']}" pitch="{self.config['podcast']['pitch']}%">
    <s>{noticia['ferramenta']} · {noticia['empresa']}</s>
    <break time="300ms"/>
    <s>{noticia['titulo']}</s>
    <break time="400ms"/>
    <s>{noticia['resumo']}</s>
  </prosody>
  
  <break time="800ms"/>
"""
        
        # Conclusão
        roteiro += f"""  <prosody rate="{self.config['podcast']['velocidade'] + 0.05}" pitch="{self.config['podcast']['pitch']}%">
    <s>Essas foram as principais novidades da semana.</s>
    <break time="300ms"/>
    <s>BrillIAnt: o seu primeiro passo no mundo da inteligência artificial.</s>
    <break time="300ms"/>
    <s>Coloque a inteligência artificial para trabalhar por você.</s>
  </prosody>
</speak>"""
        
        logger.info("✅ Roteiro do podcast gerado")
        return roteiro
    
    def gerar_podcast_mp3(self, roteiro_ssml, dados):
        """
        Gerar o arquivo MP3 do podcast usando Google Cloud TTS.
        
        Args:
            roteiro_ssml: Roteiro em formato SSML
            dados: Dados da semana (para obter a data)
        
        Returns:
            str: Caminho do arquivo MP3 gerado
        """
        # Preparar request
        synthesis_input = texttospeech.SynthesisInput(ssml=roteiro_ssml)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",
            name=self.config['podcast']['voz'],
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            sample_rate_hertz=self.config['podcast']['sample_rate_hertz'],
        )
        
        # Gerar áudio
        logger.info("🎙️ Gerando áudio via Google Cloud TTS...")
        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        
        # Salvar arquivo
        data_semana = dados['semana']
        pasta_saida = self.project_root / self.config['github']['pasta_radares'] / data_semana
        pasta_saida.mkdir(parents=True, exist_ok=True)
        
        arquivo_mp3 = pasta_saida / "podcast.mp3"
        with open(arquivo_mp3, "wb") as out:
            out.write(response.audio_content)
        
        logger.info(f"✅ Podcast gerado: {arquivo_mp3}")
        return str(arquivo_mp3)
    
    def gerar_html_materia(self, noticia, numero, data_semana):
        """
        Gerar arquivo HTML para uma matéria individual.
        
        Args:
            noticia: Dados da notícia
            numero: Número da notícia (1-5)
            data_semana: Data da semana (YYYY-MM-DD)
        
        Returns:
            str: Caminho do arquivo HTML
        """
        pasta_saida = self.project_root / self.config['github']['pasta_radares'] / data_semana
        pasta_saida.mkdir(parents=True, exist_ok=True)
        
        # Carregar template
        template_path = self.project_root / self.config['estrutura']['template_materia']
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        template = Template(template_str)
        
        # Renderizar
        html = template.render(
            numero=numero,
            ferramenta=noticia['ferramenta'],
            empresa=noticia['empresa'],
            titulo=noticia['titulo'],
            resumo=noticia['resumo'],
            conteudo_completo=noticia['conteudo_completo'],
            highlight=noticia['highlight'],
            data_semana=data_semana,
            proxima_materia=f"materia_{numero + 1}.html" if numero < 5 else "index.html",
            materia_anterior=f"materia_{numero - 1}.html" if numero > 1 else "index.html",
        )
        
        arquivo_html = pasta_saida / f"materia_{numero}.html"
        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Matéria {numero} gerada: {arquivo_html}")
        return str(arquivo_html)
    
    def gerar_html_radar(self, dados):
        """
        Gerar arquivo HTML da página principal do Radar.
        
        Args:
            dados: Dados da semana
        
        Returns:
            str: Caminho do arquivo HTML
        """
        pasta_saida = self.project_root / self.config['github']['pasta_radares'] / dados['semana']
        pasta_saida.mkdir(parents=True, exist_ok=True)
        
        # Carregar template
        template_path = self.project_root / self.config['estrutura']['template_radar']
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        template = Template(template_str)
        
        # Renderizar
        html = template.render(
            data_inicio=dados['data_inicio'],
            data_fim=dados['data_fim'],
            noticias=dados['noticias'],
            semana=dados['semana'],
        )
        
        arquivo_html = pasta_saida / "index.html"
        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Página do Radar gerada: {arquivo_html}")
        return str(arquivo_html)
    
    def atualizar_index_principal(self, dados):
        """
        Atualizar o index.html principal com a nova semana em destaque.
        
        Args:
            dados: Dados da semana
        """
        # Carregar template
        template_path = self.project_root / self.config['estrutura']['template_index']
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        # Listar todas as semanas
        pasta_radares = self.project_root / self.config['github']['pasta_radares']
        semanas = sorted([d.name for d in pasta_radares.iterdir() if d.is_dir()], reverse=True)
        
        template = Template(template_str)
        html = template.render(
            semana_destaque=dados['semana'],
            data_destaque_inicio=dados['data_inicio'],
            data_destaque_fim=dados['data_fim'],
            semanas=semanas,
        )
        
        arquivo_index = self.project_root / "index.html"
        with open(arquivo_index, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"✅ Index principal atualizado: {arquivo_index}")
    
    def fazer_commit_push(self, dados):
        """
        Fazer commit dos arquivos gerados.
        O push será feito pelo GitHub Actions.
        """
        try:
            os.chdir(self.project_root)
            
            # Configurar git
            subprocess.run(['git', 'config', 'user.email', 'radar@brilliant.ai'], check=True)
            subprocess.run(['git', 'config', 'user.name', 'Radar Bot'], check=True)
            
            # Adicionar arquivos
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit
            mensagem = f"🚀 Radar da Semana - {dados['semana']}"
            subprocess.run(['git', 'commit', '-m', mensagem], check=True)
            
            logger.info("✅ Commit realizado com sucesso (push será feito pelo GitHub Actions)")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Erro ao fazer commit: {e}")
            raise
    
    def disparar_deploy_vercel(self):
        """
        Disparar deploy na Vercel via webhook.
        """
        webhook_url = os.getenv('VERCEL_DEPLOY_HOOK')
        
        if not webhook_url:
            logger.warning("⚠️ VERCEL_DEPLOY_HOOK não configurado. Deploy manual necessário.")
            return
        
        try:
            import requests
            response = requests.post(webhook_url)
            if response.status_code == 200:
                logger.info("✅ Deploy na Vercel disparado com sucesso")
            else:
                logger.error(f"❌ Erro ao disparar deploy: {response.status_code}")
        except Exception as e:
            logger.error(f"❌ Erro ao disparar deploy: {e}")
    
    def executar(self):
        """
        Executar o fluxo completo de geração do Radar.
        """
        try:
            logger.info("=" * 60)
            logger.info("🚀 Iniciando geração do Radar da Semana BrillIAnt")
            logger.info("=" * 60)
            
            # 1. Carregar dados
            dados = self.carregar_dados_semana()
            
            # 2. Gerar roteiro do podcast
            roteiro = self.gerar_roteiro_podcast(dados)
            
            # 3. Gerar podcast MP3
            self.gerar_podcast_mp3(roteiro, dados)
            
            # 4. Gerar matérias HTML
            for i, noticia in enumerate(dados['noticias'], 1):
                self.gerar_html_materia(noticia, i, dados['semana'])
            
            # 5. Gerar página do Radar
            self.gerar_html_radar(dados)
            
            # 6. Atualizar index principal
            self.atualizar_index_principal(dados)
            
            # 7. Fazer commit e push
            self.fazer_commit_push(dados)
            
            # 8. Disparar deploy Vercel
            self.disparar_deploy_vercel()
            
            logger.info("=" * 60)
            logger.info("✅ Radar gerado com sucesso!")
            logger.info(f"📍 Link: https://brilliant-radar.vercel.app/radares/{dados['semana']}/")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Erro durante geração: {e}")
            raise

if __name__ == "__main__":
    generator = RadarGenerator()
    generator.executar()
