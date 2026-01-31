import re
from collections import Counter
from bs4 import BeautifulSoup
import json


STOPWORDS = {
    "com", "para", "uma", "que", "por", "em", "de", "da", "do", "e", "ou", 
    "na", "no", "as", "os", "um", "uns", "umas", "pelo", "pela", "aos", 
    "nas", "nos", "com", "sob", "sobre", "entre", "através", "ao", "seu", 
    "sua", "seus", "suas", "como", "mais", "mas", "bem", "muito", "gupy", "cookies", "portal", "aviso", "copiar", "link",
    "vaga", "etapa", "uso", "sicredi", "linkedin", "vagas", "trabalhar", "empresa", "privacidade", "termos", "aceitar", "clique",
    "site", "descrição", "remoto", "híbrido", "presencial", "benefícios", "requisitos", "responsabilidades"
}

HARD_SKILLS = [
    "python", "sql", "machine learning", "deep learning", "llm", "nlp", 
    "estatística", "pandas", "numpy", "java", "javascript", "typescript", 
    "react", "node.js", "c#", "go", "rust", "api rest", "microservices", 
    "nosql", "mongodb", "postgresql", "html", "css", "etl", "spark", 
    "tableau", "power bi", "testes unitários", "automação", "tdd", "bdd",
    "prompt engineering", "rva", "rag", "vector databases", "fine-tuning", "mlops", "devops",
    "data engineering", "big data", "pyspark", "cloud computing", "serverless", "fastapi",
    "django", "flask", "pytorch", "tensorflow", "keras", "opencv", "dbt", "airflow"
]

SOFT_SKILLS = [
    "comunicação", "trabalho em equipe", "proatividade", "pensamento analítico",
    "resolução de problemas", "adaptabilidade", "liderança", "gestão de tempo",
    "pensamento crítico", "aprendizado contínuo", "metodologias ágeis", 
    "empatia", "resiliência", "inteligência emocional", "mentoria",
    "colaboração", "curiosidade intelectual", "ética em ia", "storytelling de dados",
    "autogestão", "comunicação assertiva", "orientação a resultados", "scrum", "kanban"
]

TOOLS = [
    "docker", "git", "aws", "gcp", "azure", "pytorch", "tensorflow", 
    "scikit-learn", "kubernetes", "terraform", "jenkins", "github actions", 
    "langchain", "hugging face", "databricks", "selenium", "cypress", 
    "playwright", "pytest", "postman", "jira", "confluence", "tableau", "power bi",
    "pinecone", "chromadb", "milvus", "openai api", "anthropic api", "llama-index",
    "snowflake", "redshift", "bigquery", "kafka", "rabbitmq", "prometheus", "grafana",
    "wandb", "mlflow", "circleci", "gitlab ci", "bitbucket"
]
def clean_text(text):
    
    # 2. Garante que é string (caso venha um número ou outro objeto)
    text = str(text)

    # 3. Executa a limpeza
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_job_title(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")

    # 1️⃣ H1 — fonte principal
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
        if len(title) > 3:
            return title

    # 2️⃣ og:title — fallback simples
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].split("|")[0].strip()

    # 3️⃣ Title tag — último recurso
    if soup.title and soup.title.string:
        return soup.title.string.split("|")[-1].strip()

    return None


def extract_from_json_ld(soup):
    """
    Tenta extrair do padrão schema.org (JobPosting).
    É o método mais preciso para Gupy, Greenhouse, Lever, etc.
    """
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            if not script.string: continue
            data = json.loads(script.string)
            
            # Às vezes o JSON-LD é uma lista
            if isinstance(data, list):
                for item in data:
                    if item.get('@type') == 'JobPosting':
                        return item.get('title')
            
            # Ou um objeto único
            elif isinstance(data, dict):
                if data.get('@type') == 'JobPosting':
                    return data.get('title')
                # Às vezes está dentro de @graph
                if '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') == 'JobPosting':
                            return item.get('title')
        except:
            continue
    return None



def extract_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return clean_text(soup.get_text(" "))



def find_matches(text, vocab):
    return [v for v in vocab if v in text]


def extract_experience(text):
    return re.findall(r"\d+\+?\s+anos?\s+de\s+experiência", text)


def extract_keywords(text, top_n=15):
    words = re.findall(r"\b[a-zà-ú]{3,}\b", text)
    words = [w for w in words if w not in STOPWORDS]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(top_n)]


def extract_requirements(raw_input: str, is_html=True):
    if is_html:
        html = raw_input
        text = extract_from_html(raw_input.lower())
        title = extract_job_title(html)
    else:
        text = clean_text(raw_input)
        title = None

    return {
        "title": title,
        "hard_skills": find_matches(text, HARD_SKILLS),
        "soft_skills": find_matches(text, SOFT_SKILLS),
        "tools": find_matches(text, TOOLS),
        "experience": extract_experience(text),
        "education": find_matches(text, ["graduação", "mestrado", "doutorado"]),
        "keywords": extract_keywords(text),
    }
