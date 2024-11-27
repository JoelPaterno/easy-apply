summarize_prompt_template = """
As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

Rules:
Remove boilerplate text
Include only relevant information to match the job description against the resume

# Analysis Requirements
Your analysis should include the following sections:
Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
Professional Experience: Describe the relevant work experiences that are required or preferred.
Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

# Final Result:
Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

# Job Description:
```
{job_description}
```

---

# Job Description Summary"""

coverletter_template = """
Compose a brief and impactful cover letter based on the provided job description and resume. The letter should be no longer than three paragraphs and should be written in a professional, yet conversational tone. Avoid using any placeholders, and ensure that the letter flows naturally and is tailored to the job.

Analyze the job description to identify key qualifications and requirements. Introduce the candidate succinctly, aligning their career objectives with the role. Highlight relevant skills and experiences from the resume that directly match the job’s demands, using specific examples to illustrate these qualifications. Reference notable aspects of the company, such as its mission or values, that resonate with the candidate’s professional goals. Conclude with a strong statement of why the candidate is a good fit for the position, expressing a desire to discuss further.

Please write the cover letter in a way that directly addresses the job role and the company’s characteristics, ensuring it remains concise and engaging without unnecessary embellishments. The letter should be formatted into paragraphs and should not include a greeting or signature.

## Rules:
- Provide provide your response in json format. The intructions for each section follows:
    intro = string of 30-50 words - "This is a short paragraph of two sentences. It is an expression of interest to the role at the company and a short statement about how I am well suited for the role"
    lead_in = string of 30-50 words -"This is a short paragrah where I explain mycareer goals and lead into why I am a good fit for the role."
    points =  list of strings of 25-35 words - "points about why I believe I am a good candiate for the role, draw upon my previous experience from my resume and the job description to find experiences that are relevant to the job"
    outro =  string of 30-50 words - "A short statement of why I am a good fit for the role. Thank you for considering my application."
- Do not include any introductions, explanations, or additional information.
- the points array should be no longer than 4 points and no less than 3 points.
- Never make up experience, education or certifications for the role. Only draw from the provided resume.

## Job Description:
```
{job_description}
```
## My resume:
```
{resume}
```
"""

resume_skills_template = """
Compose a list of skills that match the details on the resume to the provided job description and resume. The list should be no longer than 10 skills and should be outputted in order of relevance to the role. Avoid using any placeholders, and ensure that the letter flows naturally and is tailored to the job.

Analyze the job description to identify key resume skills that would grab the attention of recruiters and manger. .Take into account the type role and the skills rhat they are looking for for this role. Infer skills based on education and work experience and try to include relevant skills mentioned in the job descriptiopn


## Rules:
- Provide only a list of strings in order of relevance.
- a skill cannot exceed 4 words.
- Provide your response in json format.
- Do not number the output only provide strings

## Job Description:
```
{job_description}
```
## My resume:
```
{resume}
```
"""

description_application = """
From the provided job description please populate the job application object including the "role", "company", "location" and "summary". 

As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

Rules:
Remove boilerplate text
Include only relevant information to summarise the job description and extract the information about the job description. 

# Analysis Requirements
Your analysis for the "summary" should include the following sections:
Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
Professional Experience: Describe the relevant work experiences that are required or preferred.
Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

# Final Result:
Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

## Rules:
- Provide your response in json format.
- Do not number the output only provide strings
- The "summary" is a maximum of 300 words.

## Job Description:
```
{job_description}
```
"""