import pandas as pd
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nlp = spacy.load('en_core_web_lg')  # en_core_web_sm

passage = '''John went for a bike ride. He rode around the block. Then he met some girls he knew from school. 
They all rode to the field to play. John had a great time playing games with his friends.'''
input = "John went for a xxx ride."

doc = nlp(str(passage))
question = nlp(str(input))

sim = pd.DataFrame(columns=['SENTENCE', 'SCORE'])
for sentence in doc.sents:
    sim = sim.append({'SENTENCE': sentence.text, 'SCORE': sentence.similarity(question)}, ignore_index=True)
sim_max = sim.loc[sim['SCORE'].idxmax()]

# remove stop words
stop_words = set(stopwords.words('english'))
sim_max_lower = sim_max['SENTENCE'].lower()
input_lower = input.lower()

sentence_tokens = word_tokenize(sim_max_lower)
input_tokens = word_tokenize(input_lower)
filtered_sentence = [w for w in sentence_tokens if not w in stop_words]
filtered_input = [w for w in input_tokens if not w in stop_words]

# remove punctuation
filtered_sentence = [word for word in filtered_sentence if word.isalpha()]
filtered_input = [word for word in filtered_input if word.isalpha()]
sim_max_filtered = ' '.join(filtered_sentence)

missing_index = filtered_input.index('xxx')

if missing_index == len(filtered_input) - 1:
    missing = filtered_input[-3:-1]
elif missing_index == 0:
    missing = filtered_input[1:3]
else:
    missing = [filtered_input[missing_index - 1], filtered_input[missing_index + 1]]

missing_input = ' '.join(missing)
print(passage + "\n")
print("Q:" + str(question))
print("A:" + str(missing_input))
