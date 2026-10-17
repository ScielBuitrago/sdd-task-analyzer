# Regras de contexto

Este documento estabelece as diretrizes obrigatórias e as proibições estritas para a geração automatizada de código do módulo **TaskAnalyzer**. O agente de IA deve seguir rigorosamente todos os pontos abaixo.

---

## Diretrizes Arquiteturais (Obrigatórias)

- Python 3.11+ como versão mínima obrigatória
- Utilizar **type hints** (anotações de tipo) em todas as funções e métodos.
- Seguir o princípio **Single Responsability** (SRP) e código limpo (PEP 8).
- Documentação formal no padrão Google style docstrings para módulos, classes, funções e parâmetros.
- Funções devem ser pequenas, coesas e com um único propósito.
- Tratamento de exceções especifico e com mensagens claras.
- Logs estruturados utilizando o módulo padrão **logging**.
- Código deve ser legível, manutenível e com nomes de variáveis e funções descritivos.

---

## Proibições Explícitas (Regras Restritivas)

- Não utilizar bibliotecas externas não autorizadas.
- Não alterar, remover ou adaptar os cenários de teste fornecidos.
- Não modificar a estrutura de pastas definida nesta especificação.
- Não persistir dados em arquivos ou banco de dados.
- Não alterar a assinatura (nome e parâmetros) das funções públicas sem autorização.
- Não gerar código sem testes correspondentes para as novas funcionalidades.
- Não inserir código duplicado ou sem necessidade.
- Não assumir comportamentos não especificados no contrato de negócio.

# Regras de interação com IA

- Fornecer sempre o contexto completo antes da solitação.
- Validar se a IA compreendeu o contrato antes de gerar o código.
- Solicitar explicações quando houver dúvidas na solução.
- Revisar criticamente todo código gerado.
- Rejeitar respostas que violem as proibições ou o contrato

 
