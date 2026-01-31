import json
from rapidfuzz import fuzz

def normalize(text):
    return text.lower().strip()

def relevance_score(text: str, keywords: list[str]) -> int:
    score = 0
    text = text.lower()
    for kw in keywords:
        if kw.lower() in text:
            score += 3
        elif fuzz.partial_ratio(kw.lower(), text) >= 80:
            score += 1
    return score

def score_list(cv_items, job_items):
    score = 0
    matches = []

    for cv in cv_items:
        for job in job_items:
            if fuzz.partial_ratio(normalize(cv), normalize(job)) >= 80:
                score += 1
                matches.append(cv)
                break

    return score, list(set(matches))

def score_certifications(certifications, job_items, threshold=75, max_items=4):
    scored = []

    for cert in certifications:
        text = f"{cert['name']} {cert.get('issuer', '')}"

        best_score = 0
        for job_item in job_items:
            score = fuzz.partial_ratio(
                normalize(text),
                normalize(job_item)
            )
            best_score = max(best_score, score)

        if best_score >= threshold:
            scored.append((best_score, cert))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [cert for _, cert in scored[:max_items]]


def match_projects(projects, job_items, threshold=70, max_items=2):
    scored = []

    for project in projects:
        stack_text = " ".join(project.get("techStack", []))
        desc_text = project.get("description", "")
        combined = f"{stack_text} {desc_text}"

        best_score = 0
        for job_item in job_items:
            score = fuzz.partial_ratio(
                normalize(combined),
                normalize(job_item)
            )
            best_score = max(best_score, score)

        if best_score >= threshold:
            scored.append((best_score, project))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [proj for _, proj in scored[:max_items]]



def match_resume(cv, job):
    result = {}

    hs_score, hs_match = score_list(
        cv["skills"]["hard_skills"],
        job["hard_skills"]
    )

    tech_score, tech_match = score_list(
        cv["skills"]["technologies"],
        job["hard_skills"]
    )

    tools_score, tools_match = score_list(
        cv["skills"]["hard_skills"],
        job["tools"]
    )

    ss_score, ss_match = score_list(
        cv["skills"]["soft_skills"],
        job["soft_skills"]
    )

    matched_certs = score_certifications(
        cv.get("certifications", []),
        job["hard_skills"] + job["tools"]
    )

    matched_projects = match_projects(
        cv.get("projects", []),
        job["hard_skills"] + job["tools"]
    )

    result["title"] = job["title"]
    result["score"] = hs_score * 3 + tools_score * 2 + ss_score
    result["matched_hard_skills"] = hs_match
    result["matched_technologies"] = tech_match
    result["matched_tools"] = tools_match
    result["matched_soft_skills"] = ss_match
    result["matched_certifications"] = matched_certs
    result["matched_projects"] = matched_projects

    return result
