import subprocess
import json
import re

def adapt_summary(
    cv: dict,
    match: dict,
    model: str = "llama3.1:8b"
) -> str:
    """
    Adapta o resumo profissional para a vaga.
    """

    prompt = f"""
Você é um especialista em ATS.

Reescreva o RESUMO PROFISSIONAL para a vaga abaixo
usando APENAS as informações fornecidas.

Regras:
- Não invente experiências
- Não crie tecnologias novas
- Linguagem profissional e objetiva
- Máx. 5 linhas
- Priorize as competências relevantes para a vaga

Cargo da vaga:
{match.get("title")}

Competências técnicas relevantes:
{", ".join(match.get("hard_skills", []))}

Ferramentas relevantes:
{", ".join(match.get("tools", []))}

Resumo atual do candidato:
{cv.get("summary")}

Responda APENAS em JSON válido:
{{ "summary": "..." }}
"""

    output = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    ).stdout

    match = re.search(r"\{.*\}", output, re.S)
    if not match:
        raise ValueError("Resumo inválido retornado pela LLM")

    return json.loads(match.group())["summary"]


def adapt_objective(
    cv: dict,
    match: dict,
    model: str = "llama3.1:8b"
) -> str:
    """
    Adapta o objetivo profissional para a vaga.
    """

    prompt = f"""
Você é um especialista em recrutamento.

Reescreva o OBJETIVO PROFISSIONAL para a vaga abaixo
usando APENAS as informações fornecidas.

Regras:
- Não invente experiências
- Não criar novas tecnologias
- Texto curto (2–3 linhas)
- Alinhado ao cargo e senioridade

Cargo da vaga:
{match.get("title")}

Soft skills valorizadas:
{", ".join(match.get("soft_skills", []))}

Objetivo atual do candidato:
{cv.get("objective")}

Responda APENAS em JSON válido:
{{ "objective": "..." }}
"""

    output = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True
    ).stdout

    match = re.search(r"\{.*\}", output, re.S)
    if not match:
        raise ValueError("Objetivo inválido retornado pela LLM")

    return json.loads(match.group())["objective"]

