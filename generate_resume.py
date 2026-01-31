import json
import subprocess
import sys
from matcher import match_resume
from resume_builder import build_docx


def run_analyzer(vaga_url: str):
    """
    Chama o analyzer.py via subprocess e retorna o JSON da vaga
    """
    try:
        result = subprocess.run(
            [
                sys.executable,
                "analyzer.py",
                "--url",
                vaga_url,
                "--json",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Erro ao executar analyzer.py")
        print(e.stderr)
        sys.exit(1)

    except json.JSONDecodeError:
        print("Analyzer não retornou um JSON válido")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("python generate_resume.py <URL_DA_VAGA>")
        sys.exit(1)

    vaga_url = sys.argv[1]

    with open("curriculo.json", encoding="utf-8") as f:
        cv = json.load(f)

    job = run_analyzer(vaga_url)

    match = match_resume(cv, job)

    build_docx(cv, match)

    print("Currículo gerado com sucesso!")
    print("Score de compatibilidade:", match["score"])


if __name__ == "__main__":
    main()
