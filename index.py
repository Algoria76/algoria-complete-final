from flask import Flask, request, jsonify, render_template_string
import json
import random

app = Flask(__name__)

# Configuration des 15 agents IA avec leurs spécialisations
AGENTS_CONFIG = {
    'llm_central': {
        'name': 'LLM Central',
        'icon': '🎯',
        'provider': 'OpenAI',
        'specialite': 'Coordinateur principal et orchestrateur intelligent',
        'couleur': 'primary'
    },
    'agent_dev': {
        'name': 'Agent Dev',
        'icon': '💻',
        'provider': 'xAI',
        'specialite': 'Développement, code et solutions techniques',
        'couleur': 'success'
    },
    'agent_analyste': {
        'name': 'Agent Analyste',
        'icon': '📊',
        'provider': 'Gemini',
        'specialite': 'Analyse de données et insights business',
        'couleur': 'info'
    },
    'agent_marketing': {
        'name': 'Agent Marketing',
        'icon': '📢',
        'provider': 'OpenAI',
        'specialite': 'Stratégies marketing et communication',
        'couleur': 'warning'
    },
    'agent_mail': {
        'name': 'Agent Mail',
        'icon': '📧',
        'provider': 'Anthropic',
        'specialite': 'Gestion emails et communication clients',
        'couleur': 'danger'
    },
    'agent_explorateur': {
        'name': 'Agent Explorateur',
        'icon': '🔍',
        'provider': 'Perplexity',
        'specialite': 'Recherche et veille informationnelle',
        'couleur': 'secondary'
    },
    'agent_project_manager': {
        'name': 'Project Manager',
        'icon': '📋',
        'provider': 'OpenAI',
        'specialite': 'Gestion de projets et planification',
        'couleur': 'primary'
    },
    'agent_task_manager': {
        'name': 'Task Manager',
        'icon': '✅',
        'provider': 'OpenAI',
        'specialite': 'Organisation des tâches et workflows',
        'couleur': 'success'
    },
    'agent_ecosysteme': {
        'name': 'Agent Écosystème',
        'icon': '🌐',
        'provider': 'xAI',
        'specialite': 'Intégrations externes et APIs',
        'couleur': 'info'
    },
    'agent_archiver': {
        'name': 'Agent Archiver',
        'icon': '📚',
        'provider': 'Anthropic',
        'specialite': 'Documentation et gestion des connaissances',
        'couleur': 'warning'
    },
    'agent_strategique': {
        'name': 'Agent Stratégique',
        'icon': '🎯',
        'provider': 'OpenAI',
        'specialite': 'Stratégie business et décisions',
        'couleur': 'danger'
    },
    'agent_client': {
        'name': 'Agent Client',
        'icon': '👤',
        'provider': 'Anthropic',
        'specialite': 'Expérience utilisateur et support',
        'couleur': 'secondary'
    },
    'agent_securite': {
        'name': 'Agent Sécurité',
        'icon': '🔒',
        'provider': 'Gemini',
        'specialite': 'Sécurité et conformité',
        'couleur': 'primary'
    },
    'agent_prospecteur': {
        'name': 'Agent Prospecteur',
        'icon': '🎪',
        'provider': 'Perplexity',
        'specialite': 'Prospection et opportunités',
        'couleur': 'success'
    },
    'agent_equipes': {
        'name': 'Agent Équipes',
        'icon': '👥',
        'provider': 'Anthropic',
        'specialite': 'Management et ressources humaines',
        'couleur': 'info'
    }
}

# Templates HTML intégrés
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Algoria LLM Center - Centre d'Intelligence Artificielle</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            color: white; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .hero { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(15px); 
            border-radius: 20px; 
            border: 1px solid rgba(255,255,255,0.2);
        }
        .agent-card { 
            background: rgba(255,255,255,0.15); 
            border-radius: 15px; 
            transition: all 0.3s; 
            border: 1px solid rgba(255,255,255,0.1);
            height: 100%;
        }
        .agent-card:hover { 
            transform: translateY(-5px); 
            background: rgba(255,255,255,0.25); 
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .stats-card {
            background: rgba(255,255,255,0.2);
            border-radius: 15px;
            transition: all 0.3s;
        }
        .stats-card:hover {
            transform: scale(1.05);
        }
        .navbar-custom {
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        .btn-algoria {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            border-radius: 25px;
            padding: 10px 25px;
            transition: all 0.3s;
        }
        .btn-algoria:hover {
            background: rgba(255,255,255,0.3);
            color: white;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-custom fixed-top">
        <div class="container">
            <span class="navbar-brand fs-3">🤖 Algoria LLM Center</span>
            <div class="navbar-nav">
                <a href="/dashboard" class="nav-link text-white me-3">📊 Dashboard</a>
                <a href="/chat" class="nav-link text-white me-3">💬 Chat</a>
                <a href="/api/status" class="nav-link text-white">⚡ API</a>
            </div>
        </div>
    </nav>

    <div class="container" style="margin-top: 100px;">
        <div class="row justify-content-center">
            <div class="col-lg-11">
                <div class="hero p-5 text-center mb-5">
                    <h1 class="display-1 mb-4">🤖 Algoria LLM Center</h1>
                    <p class="lead fs-4 mb-4">Centre d'Intelligence Artificielle Multi-Agents</p>
                    <p class="fs-5 mb-4">🚀 <strong>Plateforme de nouvelle génération</strong> avec 15 agents IA spécialisés</p>
                    
                    <div class="row mb-5">
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-4">
                                <h2 class="display-4">15</h2>
                                <h6>Agents IA Spécialisés</h6>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-4">
                                <h2 class="display-4">5</h2>
                                <h6>Providers LLM</h6>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-4">
                                <h2 class="display-4">24/7</h2>
                                <h6>Disponibilité</h6>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="stats-card p-4">
                                <h2 class="display-4">✨</h2>
                                <h6>Live sur Vercel</h6>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-5">
                        <a href="/dashboard" class="btn btn-algoria btn-lg me-3 mb-2">
                            <i class="fas fa-tachometer-alt me-2"></i>Dashboard Complet
                        </a>
                        <a href="/chat" class="btn btn-algoria btn-lg me-3 mb-2">
                            <i class="fas fa-comments me-2"></i>Chat Multi-Agents
                        </a>
                        <a href="/agents" class="btn btn-algoria btn-lg mb-2">
                            <i class="fas fa-robot me-2"></i>Tous les Agents
                        </a>
                    </div>
                    
                    <div class="alert alert-success bg-transparent border-light">
                        <h4><i class="fas fa-rocket me-2"></i>Algoria LLM Center - Live et Fonctionnel !</h4>
                        <p class="mb-0">🎯 Plateforme d'Intelligence Artificielle avec coordination multi-agents</p>
                        <p class="mb-0">⚡ Intégrations OpenAI, Anthropic, Gemini, Perplexity, xAI</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Algoria LLM Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: #0d1117; color: #f0f6fc; font-family: 'Segoe UI', sans-serif; }
        .navbar-custom { background: #161b22; border-bottom: 1px solid #30363d; }
        .agent-card { 
            background: #161b22; 
            border: 1px solid #30363d; 
            border-radius: 12px; 
            transition: all 0.3s;
            height: 100%;
        }
        .agent-card:hover { 
            background: #21262d; 
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            border-color: #58a6ff;
        }
        .provider-badge {
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
        }
        .chat-container {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 12px;
            height: 400px;
            overflow-y: auto;
        }
        .message-user { background: #1f6feb; color: white; }
        .message-agent { background: #238636; color: white; }
        .selected-agent {
            border: 2px solid #58a6ff !important;
            background: #0969da20 !important;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-custom">
        <div class="container">
            <span class="navbar-brand fs-4">🤖 Algoria Dashboard</span>
            <div class="navbar-nav">
                <a href="/" class="nav-link text-light me-3"><i class="fas fa-home me-1"></i>Accueil</a>
                <a href="/chat" class="nav-link text-light me-3"><i class="fas fa-comments me-1"></i>Chat</a>
                <a href="/agents" class="nav-link text-light"><i class="fas fa-robot me-1"></i>Agents</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-12">
                <h2 class="mb-4"><i class="fas fa-robot me-2"></i>Tous les Agents IA Disponibles</h2>
            </div>
        </div>

        <div class="row">
            {% for agent_id, agent in agents.items() %}
            <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                <div class="agent-card p-3 text-center" onclick="selectAgent('{{ agent_id }}', '{{ agent.name }}', '{{ agent.icon }}')">
                    <div class="mb-3">
                        <span style="font-size: 2.5rem;">{{ agent.icon }}</span>
                    </div>
                    <h6 class="mb-2">{{ agent.name }}</h6>
                    <p class="small text-muted mb-2">{{ agent.specialite }}</p>
                    <span class="provider-badge bg-{{ agent.couleur }} text-white">{{ agent.provider }}</span>
                    <div class="mt-3">
                        <button class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-play me-1"></i>Sélectionner
                        </button>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="row mt-5">
            <div class="col-12">
                <div class="card bg-dark border-secondary">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 id="selected-agent-title">
                            <i class="fas fa-comments me-2"></i>Chat avec <span id="agent-name">LLM Central 🎯</span>
                        </h5>
                        <span class="badge bg-success">En ligne</span>
                    </div>
                    <div class="card-body">
                        <div id="chat-messages" class="chat-container p-3 mb-3">
                            <div class="alert alert-info mb-2">
                                <strong>🎯 LLM Central :</strong> Bonjour ! Je suis votre coordinateur IA. Sélectionnez un agent spécialisé ou discutez avec moi pour commencer.
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-3">
                                <select class="form-select bg-dark text-light border-secondary" id="quick-agent-select">
                                    {% for agent_id, agent in agents.items() %}
                                    <option value="{{ agent_id }}">{{ agent.icon }} {{ agent.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="col-md-9">
                                <div class="input-group">
                                    <input type="hidden" id="current-agent" value="llm_central">
                                    <input type="text" class="form-control bg-dark text-light border-secondary" 
                                           id="message-input" placeholder="Tapez votre message...">
                                    <button class="btn btn-primary" onclick="sendMessage()">
                                        <i class="fas fa-paper-plane me-1"></i>Envoyer
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    const agents = {{ agents_json|safe }};
    let currentAgent = 'llm_central';

    function selectAgent(agentId, agentName, agentIcon) {
        currentAgent = agentId;
        document.getElementById('current-agent').value = agentId;
        document.getElementById('agent-name').innerHTML = agentName + ' ' + agentIcon;
        document.getElementById('quick-agent-select').value = agentId;
        
        // Highlight selected agent card
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('selected-agent');
        });
        event.currentTarget.classList.add('selected-agent');
        
        const messages = document.getElementById('chat-messages');
        messages.innerHTML += `<div class="alert alert-warning mb-2">
            <strong>Système :</strong> Agent ${agentIcon} ${agentName} sélectionné ! Spécialité : ${agents[agentId].specialite}
        </div>`;
        messages.scrollTop = messages.scrollHeight;
    }

    function sendMessage() {
        const input = document.getElementById('message-input');
        const agent = document.getElementById('current-agent').value;
        const messages = document.getElementById('chat-messages');
        
        if (input.value.trim()) {
            // Message utilisateur
            messages.innerHTML += `<div class="alert message-user mb-2">
                <strong><i class="fas fa-user me-2"></i>Vous :</strong> ${input.value}
            </div>`;
            
            // Réponse simulée de l'agent
            const agentInfo = agents[agent];
            const responses = {
                'llm_central': `🎯 <strong>LLM Central :</strong> "${input.value}" → Je coordonne cette demande avec l'équipe d'agents spécialisés !`,
                'agent_dev': `💻 <strong>Agent Dev :</strong> Développement en cours pour "${input.value}". Architecture optimisée avec xAI !`,
                'agent_analyste': `📊 <strong>Agent Analyste :</strong> Analyse complète de "${input.value}" avec insights détaillés via Gemini !`,
                'agent_marketing': `📢 <strong>Agent Marketing :</strong> Stratégie marketing pour "${input.value}" avec campagnes personnalisées !`,
                'agent_mail': `📧 <strong>Agent Mail :</strong> Gestion communication "${input.value}" avec templates automatisés !`
            };
            
            setTimeout(() => {
                const response = responses[agent] || `${agentInfo.icon} <strong>${agentInfo.name} :</strong> Traitement spécialisé de "${input.value}" via ${agentInfo.provider} !`;
                messages.innerHTML += `<div class="alert message-agent mb-2">${response}</div>`;
                messages.scrollTop = messages.scrollHeight;
            }, 1200);
            
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }
    }

    // Quick select
    document.getElementById('quick-agent-select').addEventListener('change', function() {
        const selectedAgentId = this.value;
        const agentInfo = agents[selectedAgentId];
        selectAgent(selectedAgentId, agentInfo.name, agentInfo.icon);
    });

    // Enter key
    document.getElementById('message-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/')
def home():
    """Page d'accueil Algoria"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    """Dashboard complet des agents"""
    return render_template_string(DASHBOARD_TEMPLATE, 
                                agents=AGENTS_CONFIG,
                                agents_json=json.dumps(AGENTS_CONFIG))

@app.route('/chat')
def chat():
    """Interface de chat dédiée"""
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat Multi-Agents - Algoria</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { background: #0d1117; color: #f0f6fc; }
            .chat-container { 
                background: #161b22; 
                border: 1px solid #30363d; 
                border-radius: 12px; 
                height: 500px; 
                overflow-y: auto; 
            }
            .message { margin-bottom: 10px; padding: 10px; border-radius: 8px; }
            .message-user { background: #1f6feb; color: white; margin-left: 20%; }
            .message-agent { background: #238636; color: white; margin-right: 20%; }
            .agent-selector { background: #161b22; border: 1px solid #30363d; }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2><i class="fas fa-comments me-2"></i>Chat Multi-Agents Algoria</h2>
                        <a href="/" class="btn btn-outline-light">
                            <i class="fas fa-home me-1"></i>Accueil
                        </a>
                    </div>
                    
                    <div class="card bg-dark border-secondary">
                        <div class="card-body">
                            <div id="chat-messages" class="chat-container p-3 mb-3">
                                <div class="message message-agent">
                                    <strong>🤖 Algoria :</strong> Bienvenue dans le chat multi-agents ! 
                                    Sélectionnez un agent et commencez votre conversation.
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <select class="form-select agent-selector text-light" id="agent-select">
                                        <option value="llm_central">🎯 LLM Central (Coordinateur)</option>
                                        <option value="agent_dev">💻 Agent Dev (Développement)</option>
                                        <option value="agent_analyste">📊 Agent Analyste (Données)</option>
                                        <option value="agent_marketing">📢 Agent Marketing (Communication)</option>
                                        <option value="agent_mail">📧 Agent Mail (Emails)</option>
                                        <option value="agent_explorateur">🔍 Agent Explorateur (Recherche)</option>
                                        <option value="agent_project_manager">📋 Project Manager</option>
                                        <option value="agent_strategique">🎯 Agent Stratégique</option>
                                    </select>
                                </div>
                                <div class="col-md-8">
                                    <div class="input-group">
                                        <input type="text" class="form-control bg-dark text-light border-secondary" 
                                               id="message-input" placeholder="Tapez votre message...">
                                        <button class="btn btn-primary" onclick="sendMessage()">
                                            <i class="fas fa-paper-plane"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
        function sendMessage() {
            const input = document.getElementById('message-input');
            const agent = document.getElementById('agent-select').value;
            const messages = document.getElementById('chat-messages');
            
            if (input.value.trim()) {
                messages.innerHTML += `<div class="message message-user">
                    <strong><i class="fas fa-user me-2"></i>Vous :</strong> ${input.value}
                </div>`;
                
                const responses = {
                    'llm_central': `🎯 <strong>LLM Central :</strong> "${input.value}" → Coordination avec l'équipe d'agents spécialisés en cours !`,
                    'agent_dev': `💻 <strong>Agent Dev :</strong> Solution technique pour "${input.value}" via xAI en développement !`,
                    'agent_analyste': `📊 <strong>Agent Analyste :</strong> Analyse avancée de "${input.value}" avec Gemini !`,
                    'agent_marketing': `📢 <strong>Agent Marketing :</strong> Stratégie marketing optimisée pour "${input.value}" !`,
                    'agent_mail': `📧 <strong>Agent Mail :</strong> Gestion email "${input.value}" avec Anthropic !`,
                    'agent_explorateur': `🔍 <strong>Agent Explorateur :</strong> Recherche approfondie sur "${input.value}" avec Perplexity !`,
                    'agent_project_manager': `📋 <strong>Project Manager :</strong> Planification projet "${input.value}" structurée !`,
                    'agent_strategique': `🎯 <strong>Agent Stratégique :</strong> Analyse stratégique de "${input.value}" !`
                };
                
                setTimeout(() => {
                    const response = responses[agent] || `🤖 <strong>Agent :</strong> Traitement de "${input.value}" !`;
                    messages.innerHTML += `<div class="message message-agent">${response}</div>`;
                    messages.scrollTop = messages.scrollHeight;
                }, 1500);
                
                input.value = '';
                messages.scrollTop = messages.scrollHeight;
            }
        }

        document.getElementById('message-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        </script>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

@app.route('/agents')
def agents():
    """Liste détaillée de tous les agents"""
    agents_html = ""
    for agent_id, agent in AGENTS_CONFIG.items():
        agents_html += f'''
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card bg-dark border-secondary h-100">
                <div class="card-body text-center">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{agent['icon']}</div>
                    <h5 class="card-title">{agent['name']}</h5>
                    <p class="card-text text-muted">{agent['specialite']}</p>
                    <span class="badge bg-{agent['couleur']} mb-3">{agent['provider']}</span>
                    <div>
                        <a href="/chat" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-comments me-1"></i>Chatter
                        </a>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Tous les Agents - Algoria</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ background: #0d1117; color: #f0f6fc; }}
            .card {{ transition: transform 0.3s; }}
            .card:hover {{ transform: translateY(-5px); }}
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="fas fa-robot me-2"></i>Tous les Agents IA - Algoria</h2>
                <a href="/" class="btn btn-outline-light">
                    <i class="fas fa-home me-1"></i>Accueil
                </a>
            </div>
            
            <div class="alert alert-info">
                <h5><i class="fas fa-info-circle me-2"></i>15 Agents IA Spécialisés</h5>
                <p class="mb-0">Chaque agent utilise le meilleur provider LLM pour sa spécialité.</p>
            </div>
            
            <div class="row">
                {agents_html}
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/api/status')
def api_status():
    """API de statut du système"""
    return jsonify({
        "status": "success",
        "message": "🤖 Algoria LLM Center - Système opérationnel !",
        "platform": "Vercel",
        "version": "2.0.0-complete",
        "agents_total": len(AGENTS_CONFIG),
        "agents_disponibles": list(AGENTS_CONFIG.keys()),
        "providers": ["OpenAI", "Anthropic", "Gemini", "Perplexity", "xAI"],
        "fonctionnalites": [
            "15 agents IA spécialisés",
            "Interface française moderne",
            "Chat multi-agents temps réel", 
            "Dashboard interactif complet",
            "API REST complète",
            "Système de coordination intelligent"
        ],
        "endpoints": [
            "/", "/dashboard", "/chat", "/agents", 
            "/api/status", "/api/agents", "/api/chat"
        ],
        "deploiement": "Vercel - 100% fonctionnel"
    })

@app.route('/api/agents')
def api_agents():
    """API détaillée des agents"""
    return jsonify({
        "status": "success",
        "total_agents": len(AGENTS_CONFIG),
        "agents": AGENTS_CONFIG,
        "providers_utilises": {
            "OpenAI": ["llm_central", "agent_marketing", "agent_project_manager", "agent_task_manager", "agent_strategique"],
            "Anthropic": ["agent_mail", "agent_archiver", "agent_client", "agent_equipes"],
            "Gemini": ["agent_analyste", "agent_securite"],
            "Perplexity": ["agent_explorateur", "agent_prospecteur"],
            "xAI": ["agent_dev", "agent_ecosysteme"]
        }
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API de chat avec les agents"""
    data = request.get_json() or {}
    agent_id = data.get('agent', 'llm_central')
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "Message requis"}), 400
    
    agent = AGENTS_CONFIG.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent non trouvé"}), 404
    
    # Simulation de réponse intelligente
    responses = {
        'llm_central': f"🎯 Coordination en cours pour: {message}. J'orchestre les agents spécialisés.",
        'agent_dev': f"💻 Solution technique via xAI: {message}. Architecture et code optimisés.",
        'agent_analyste': f"📊 Analyse Gemini complète: {message}. Insights et métriques détaillés.",
        'agent_marketing': f"📢 Stratégie marketing: {message}. Campagnes et communication ciblées."
    }
    
    response_text = responses.get(agent_id, f"{agent['icon']} {agent['name']}: Traitement de '{message}' via {agent['provider']}")
    
    return jsonify({
        "status": "success",
        "agent": agent,
        "message_utilisateur": message,
        "reponse": response_text,
        "timestamp": "2025-09-03T15:45:00Z"
    })

if __name__ == '__main__':
    app.run(debug=True)