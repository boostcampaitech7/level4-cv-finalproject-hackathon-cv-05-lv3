from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load the uploaded file
file_path = 'processed_books_data.csv'
books = pd.read_csv(file_path)

# Extract the "제목" (title) and "서브 카테고리" (sub-category) from the book dataset
book_titles = books['제목'].tolist()
book_recommends = books['사서의 추천 글'].tolist()
book_sentences = books['책 속 한 문장'].tolist()

# Combine book titles and subcategories for better matching
book_data_combined = [
    f"{title} {recommend} {sentence}" for title, recommend, sentence in zip(book_titles, book_recommends, book_sentences)
]
print(book_data_combined[0])

# Combine the user's questions into one list for TF-IDF analysis
user_questions = [
    "오랜 친구와의 관계가 어색해진 것 같아요.",
    "앞으로 뭘 해야 할지 몰라 막막해. 내 길을 어떻게 찾아야 할까?",
    "요즘은 내가 뭘 원하는지조차 잘 모르겠어. 답답하다.",
    "밤이 되면 이유 없이 마음이 헛헛하고 외로워.",
    "언제부턴가 아무것도 하고 싶지 않아졌어. 이 무기력함에서 벗어나고 싶어.",
    "사람들에게 자꾸만 맞춰주는 나 자신이 싫어.",
    "매번 실패를 반복하는 내 자신이 너무 한심해 보여.",
    "주변 사람들의 말에 너무 흔들리게 돼요.",
    "살면서 정말 중요한 게 뭘까? 요즘 이 질문이 계속 머릿속을 맴돌아.",
    "변화를 두려워하는 내 자신을 어떻게 받아들여야 할지 모르겠어.",
    "사람들과 잘 어울리고 싶지만 그게 너무 어렵게 느껴져.",
    "자꾸만 과거의 후회에 발목이 잡혀. 이걸 어떻게 떨쳐낼 수 있을까?",
    "도전하고 싶은 일이 있는데 겁부터 나. 용기를 내고 싶어.",
    "작은 일에도 너무 쉽게 상처받는 내가 싫어. 강해지고 싶어.",
    "자꾸만 남들과 비교하는 내가 미워.",
    "하루하루가 똑같이 느껴져. 지루해. 재미도 없고 기쁨도 없어.",
    "사람들이 나를 어떻게 볼지 신경 쓰여서 계속 눈치가 보여.",
    "오랜만에 친구들과 여행을 떠나기로 했어. 더 특별하게 만들 방법이 있을까?",
    "새로운 취미를 시작하게 되었는데 너무 재밌어.",
    "새 프로젝트를 맡게 되었는데, 어떤 주제로 창의적으로 접근해야 할까?",
    "오늘 하늘이 맑고 날씨가 좋네. 어디 나갈 생각 있어?",
    "요즘 사소한 것에서 행복을 느끼고 있어.",
    "느낌 좋은 카페 추천해줘.",
    "점심시간이 다가오는데 뭘 먹어야 할지 아직 결정하지 못했어. 추천해 줘.",
    "오늘 출근길 지하철이 엄청 혼잡하지 않았어?",
    "요즘 날씨가 조금 애매해서 옷을 어떻게 입어야 할까 고민돼.",
    "트라우마 극복 방법",
    "꿈을 접으려 할 때 어떤 마음가짐이 필요할까요?",
    "내가 남들보다 뒤쳐졌다는 생각이 들 때 어떻게 헤쳐나가요?",
    "7년이란 시간동안 하던 일에 슬럼프가 왔는데, 극복하고 싶은데 어떻게 해야할까요?",
    "남자친구를 1년 동안 연락도 못하고 만나지도 못하는데 이게 맞나요,,",
    "바쁜건지 연락을 며칠 안하는데 어떻게 생각하세요?",
    "술마시고 연락하는 심리가 뭘까요?",
    "전남친한테 자꾸 연락이 와요. 마음이 없는데 어떻게 해야 할까요?",
    "버티다가 한계가 왔을 때 포기해요, 아니면 계속 노력해요?",
    "편한게 불안한 건 왜일까요,,?",
    "아는게 힘 vs 모르는게 약",
    "자존감이 떨어질 때 어떻게 해야할까요?",
    "방황의 시기가 길면 길수록 도착지를 찾았을 때의 기쁨이 클까요?",
    "익숙함에 자꾸 속아버려요. 주어진 모든 상황을 당연시 여기지 않으려면 어떻게 변해야 할까요?",
    "사랑한다는 말이 없어지면 어떤 말로 표현할 것 같나요?",
    "출근할 때 무슨 생각 하시나요",
    "제 여친이 어디있는지 알려주세요",
    "수업 내용을 이해 못하는 학부생을 보는 교수님의 심정",
    "대학원생은 여자친구 어떻게 만드나요",
    "간절히 바라면 이루어진다는 말을 믿으시나요?",
    "저는 인생에 간절한 게 있었던 적이 없었던 것도 같아요. 이런 사람들에게는 어떤 말을 해주고 싶으신가요?",
    "정말 이루고 싶은 꿈이 있는데 그만큼 노력을 안하는 것 같아요.",
    "사무실 잇템을 알려주세요!",
    "당장 내일 죽는다면 할 1가지",
    "내가 싫어하는 행동을 하는 친구 거리를 둔다 vs 싫다고 말한다",
    "목표가 없어서 방황 중이라면 뭐부터 하면 좋을까요?"
]

# Perform TF-IDF vectorization to find the most relevant matches
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(user_questions + book_data_combined)

# Compute cosine similarity between user questions and books
question_vectors = tfidf_matrix[:len(user_questions)]
book_vectors = tfidf_matrix[len(user_questions):]

cosine_similarities = cosine_similarity(question_vectors, book_vectors)

# Find the most relevant book for each question
matched_books = []
for idx, question in enumerate(user_questions):
    # Get the index of the highest similarity score for this question
    best_match_idx = cosine_similarities[idx].argmax()
    matched_books.append({
        "Text": question,
        "Completion": book_titles[best_match_idx],
    })

# Convert matched books to a DataFrame and display
matched_books_df = pd.DataFrame(matched_books)
matched_books_df.to_csv('matching_output_ver3.csv', index=False, encoding='utf-8')