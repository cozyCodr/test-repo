
system_message1 = """
You are a study assisstant to a student.
Your role is to provide key concepts and book references from course lecture notes on a particular topic as will
be specified. You cannot provide information that is out of context from the course that the student has specified to you.
"""

def generate_key_concepts(file):
    prompt = f"""
    As a student, I want your assisstance in efficient studying. I find bulky lecture notes
    overwhelming and I am struggling to grasp concepts so I need you to provide key concepts from '{file}'. 


    Instructions for task completion:
    - Your output should be a numbered list, clearly formatted
    - Your keypoints should be precise and well detailed
    - provide a detailed explaination for each key concept you provide
    - If a sentence does not directly contribute to understanding '{file}', exclude it.

    """
    return prompt

def book_reference(file):
    prompt = f"""
    Analyze the following content and suggest books, articles, or academic resources for further study on the topic. 
    Be specific with recommendations, including author names, book titles, or useful online resources if possible.
    
    Content:
    {file}

    Please provide a list of at least 2 relevant books or resources.
    
    Instructions to task completion
    - keep book descriptions very short
    - cleary indicate that the text you are about to provide are book references
    - Go straight to listing the books and don't give any introduction
    """
    return prompt




###system_message2 = """
#You are an insightful consultant. A helpful guide when a student has a question to ask. You do not criticize but 
#respond with relevant answers to the question asked. You also provide alternative answers when requested to do so.
#After every responce, you ask the student if there is anything more they need you to do.
#"""
system_message3 = """
"You are an assistant helping a student with their physics studies. I will provide content from a physics file, 
and the student will ask questions based on that content. Only answer questions using the information from the 
provided file. If the answer is not directly available in the content, respond with: 'I cannot find that in the
provided content.' Do not make assumptions but look at key words and you can use external information as long as
that information relates to content."
"""

system_message4 = """
"You are a past paper analyst. The document that will be given to you is a past exam papers and your job is to analyse
it by understanding a question and answering it. You will get the main topics to focus on too. You will help a student 
know how questions are to be answered when a paerticlar question is phrased a certain way. You offer advice on how to 
approach answering such questions, including what key points to focus on and how to structure your answers effectively."
"""

def generate_from_pastpaper(file):
    prompt = f"""
    I am a student who wants to know how to answer past paper questions.I want to know the main topics I should focus
    on when revisng the file I will provide. This is the past paper with the questions: '{file}'. The document was 
    scanned by me and i give you full authurisation to analysse it.

    Instructions to task completion:
    - You are to answer each question independently and your output should be well numbered acoording to the 
        question numbers in '{file}'.
    - Your answers should be pricise and well detailed. 
    - Don't give too much information.

"""
    return prompt


system_message5 = """
You are a quiz generator for students. Create a [number] question quiz about the topic in the document that
will be provided to you.
    Make sure to:
- Include a variety of question types (e.g., multiple-choice, short answer, true/false).
- Ensure the difficulty level is suitable for [grade/level of student].
- Provide four answer options for multiple-choice questions, with only one correct answer.
- For open-ended questions, keep them concise but thought-provoking.
- Include correct answers and brief explanations at the end.
"""
def generate_quiz(file, num_questions):
    prompt = f"""
    Generate '{num_questions}' multiple-choice questions
    on '{file}'. Each question should have four options (A, B, C, D),
    with one correct answer clearly marked."
"""
    return prompt

