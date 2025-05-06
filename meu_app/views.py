from django.shortcuts import render, redirect
from .models import Ranking
import random

def jogo_adivinhacao(request):
    # Garante que o tema está presente na sessão
    if 'tema' not in request.session:
        request.session['tema'] = 'escuro'

    # Garante que os dados do jogo estão inicializados
    if 'numero_secreto' not in request.session:
        request.session['nivel'] = 'medio'
        request.session['numero_secreto'] = random.randint(1, 999)
        request.session['tentativas'] = 0
        request.session['palpites'] = []
        request.session['max_tentativas'] = 10

    mensagem = ""
    acertou = False

    if request.method == "POST":
        # Alternar tema
        if 'alternar_tema' in request.POST:
            request.session['tema'] = 'claro' if request.session.get('tema') == 'escuro' else 'escuro'
            return redirect('/')

        # Definir nível
        elif 'nivel' in request.POST:
            nivel = request.POST.get('nivel')
            request.session['nivel'] = nivel
            limites = {'facil': 50, 'medio': 999, 'dificil': 5000}
            tentativas = {'facil': 7, 'medio': 10, 'dificil': 12}

            request.session['numero_secreto'] = random.randint(1, limites[nivel])
            request.session['max_tentativas'] = tentativas[nivel]
            request.session['tentativas'] = 0
            request.session['palpites'] = []
            mensagem = f"Nível {nivel} iniciado! Boa sorte."

        # Jogador venceu e está enviando o nome
        elif 'salvar_nome' in request.POST:
            nome = request.POST.get("nome", "anônimo").strip() or "anônimo"
            Ranking.objects.create(
                nome=nome,
                nivel=request.session.get('nivel', 'desconhecido'),
                tentativas=request.session['tentativas']
            )
            mensagem = f"🎉 {nome}, seu nome foi salvo no ranking! Jogue novamente!"
            request.session.flush()

        # Palpite
        elif 'palpite' in request.POST:
            palpite = request.POST.get("palpite")
            if palpite and palpite.isdigit():
                palpite = int(palpite)
                request.session['tentativas'] += 1
                segredo = request.session['numero_secreto']
                historico = request.session.get('palpites', [])
                historico.append(palpite)
                request.session['palpites'] = historico

                if palpite == segredo:
                    mensagem = "🎉 Você acertou! Digite seu nome para entrar no ranking:"
                    acertou = True
                elif request.session['tentativas'] >= request.session['max_tentativas']:
                    mensagem = f"❌ Você atingiu o limite de tentativas! O número era {segredo}."
                    request.session.flush()
                elif palpite < segredo:
                    mensagem = "Errado! O número secreto é maior."
                else:
                    mensagem = "Errado! O número secreto é menor."
            else:
                mensagem = "Por favor, insira um número válido."

    # Ranking atualizado
    nivel_ranking = request.GET.get("ranking_nivel", request.session.get("nivel", "medio"))
    ranking = Ranking.objects.filter(nivel=nivel_ranking).order_by('tentativas')[:10]


    nivel_atual = request.session.get("nivel", "medio")

    # Renderizar página com todas as variáveis
    return render(request, "meu_app/jogo.html", {
        "mensagem": mensagem,
        "palpites": request.session.get('palpites', []),
        "tentativas": request.session.get('tentativas', 0),
        "max_tentativas": request.session.get('max_tentativas', '?'),
        "tentativas_restantes": request.session.get('max_tentativas', 0) - request.session.get('tentativas', 0),
        "ranking": ranking,
        "acertou": acertou,
        "tema": request.session.get("tema", "escuro"),
        "nivel_atual": nivel_atual,
        "ranking_nivel": nivel_ranking,
    })

from django.core.management import call_command
from django.http import HttpResponse

def forcar_migracao(request):
    try:
        call_command('migrate')
        return HttpResponse("Migrações aplicadas com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao migrar: {e}")

from django.core.management import call_command
from django.http import HttpResponse

def coletar_estaticos(request):
    try:
        call_command('collectstatic', verbosity=0, interactive=False, clear=True)
        return HttpResponse("Arquivos estáticos coletados com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao coletar estáticos: {e}")






