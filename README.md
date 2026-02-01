# Gerador de Currículos ATS-Friendly
Projeto desenvolvido para gerar currículos otimizados para sistemas de triagem automática (ATS – Applicant Tracking Systems).
O objetivo é estruturar informações profissionais de forma clara, padronizada e compatível com os critérios mais comuns
utilizados por plataformas de recrutamento automatizadas com base nas suas skills e na vaga desejada.

---

## 🎯 Objetivo do Projeto
Automatizar a criação de currículos ATS-friendly, reduzindo problemas de leitura por sistemas automáticos,
melhorando a indexação de palavras-chave e facilitando a adaptação do currículo para diferentes vagas.

---

## 🚀 Funcionalidades
- Geração automática de currículos em formato estruturado
- Organização padronizada de dados profissionais
- Compatibilidade com ATS (sem tabelas, colunas ou elementos gráficos problemáticos)
- Estrutura simples e facilmente customizável
- Possibilidade de adaptação para diferentes áreas e vagas

---

## 🛠️ Tecnologias Utilizadas
- Python
- Manipulação de dados em JSON
- Estruturas de texto compatíveis com ATS (docx)

---

## 📂 Estrutura do Projeto
- Arquivos responsáveis pela coleta e organização dos dados do currículo (curriculo-exemplo.json)
- Scripts de geração e formatação do conteúdo
- Saída estruturada em DOCX

---

## ⚙️ Como Utilizar
1. Clone o repositório
2. Preencha os dados do currículo conforme o formato esperado e altere seu nome para "curriculo.json"
3. É necessário ter o python instalado
4. instale as dependências com:
`pip install -r requirements.txt`
5. No arquivo "llm_adapter.py" é utilizado o ollama CLI com o modelo llama3.1:8b é possível usar outro modelo/API, mas precisa de adaptação no código
6. Execute o script principal --> python generate_resume.py <url_vaga>
7. Uma pasta chamada curriculo será criada com um arquivo curriculo_<nome_vaga>.docx será gerado

---

## 📌 Observações Importantes
- Você poderá editar o curriculo
- Evite elementos visuais complexos no currículo final
- Priorize palavras-chave alinhadas à vaga desejada
- Revise o conteúdo gerado antes do envio

---

## 📄 Licença
Este projeto é de uso livre para fins educacionais e pessoais.
Sinta-se à vontade para adaptar, melhorar e expandir.

---

## 👤 Autor
Desenvolvido por Leonilso Fandres Wrublak
GitHub: https://github.com/leonilso
