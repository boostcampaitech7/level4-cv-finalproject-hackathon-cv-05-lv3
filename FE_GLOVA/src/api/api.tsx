import apiClient from "./cookies";

export interface Reviews {
  name: string;
  text: string;
}

export interface Book {
  date: string;
  time: string;
  bookTitle: string;
  bookimage: string;
  question: string;
}

export interface Badge {
  createdAt: string;
  badgeImage: string;
  bookTitle: string;
}

// 서버와 묻고 답하기
export const Question2Server = async (age: string, gender: string, question: string) => {
  try {
    const response = await apiClient.post(`/api/home`, {
      age,
      gender,
      question,
    });

    return response.data; // 서버에서 받은 데이터를 반환
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// 서버한테 데이터 저장하라고 하기
export const SaveRecommand = async (data: any) => {
  const now = new Date();
  // 날짜를 KST(한국 표준시)로 변환
  const date = now.toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' })
    .replace(/. /g, '-').replace('.', ''); // YYYY-MM-DD 포맷
  try {

    const requestData = {
      date: date, // YYYY-MM-DD
      time: now.toTimeString().split(" ")[0], // HH:mm:ss
      data: data, // ✅ JSON 구조 그대로 전송
    };

    console.log("🔹 전송 데이터:", JSON.stringify(requestData, null, 2));

    const response = await apiClient.post("/api/save_books", requestData);
    console.log("✅ 추천 도서 저장 성공:", response.data);
  } catch (error) {
    console.error("추천 도서 저장 실패:", error);
  }
};



// 추천받은 책 정보 전부 가져오기
export const GetRecommandBooks = async (): Promise<Book[]> => {
  try {
    const response = await apiClient.post("/api/recommand_books");

    return response.data; // Axios는 자동으로 JSON 파싱을 수행하므로 response.data를 반환
  } catch (error) {
    console.error("Error fetching books:", error);
    return []; // 오류 발생 시 빈 배열 반환
  }
};


// 책 정보 전부 가져오기
export const GetBooks = async (): Promise<Book[]> => {
  try {
    const response = await apiClient.get("/api/get_books");

    if (response.status !== 200) {
      throw new Error(`서버 오류: ${response.status}`);
    }

    return response.data; // Axios는 자동으로 JSON 파싱을 수행하므로 response.data를 반환
  } catch (error) {
    console.error("Error fetching books:", error);
    return []; // 오류 발생 시 빈 배열 반환
  }
};


// 뱃지 생성 요청
export const PostBadgeMaker = async (bookTitle: string, speak: string) => {
  try {
    const response = await apiClient.post("/api/badge_create",
      {
        bookTitle: bookTitle,
        speak: speak,
      }
    );

    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// 뱃지 가져오기
export const GetBadges = async (): Promise<Badge[]> => {
  try {
    const response = await apiClient.post("/api/badge");

    if (response.status !== 200) {
      throw new Error(`서버 오류: ${response.status}`);
    }

    return response.data; // Axios는 자동으로 JSON 파싱을 수행하므로 response.data를 반환
  } catch (error) {
    console.error("Error fetching books:", error);
    return []; // 오류 발생 시 빈 배열 반환
  }
};


//뱃지 mp3 가져오기
// export const GetAudioFile = async () => {
//   try {
//     const response = await fetch("http://localhost:8000/api/get_audio");
//     if (!response.ok) {
//       throw new Error("Failed to fetch audio");
//     }
//     const arrayBuffer = await response.arrayBuffer();
//     const blob = new Blob([arrayBuffer], { type: "audio/mp3" });
//     return URL.createObjectURL(blob);
//   } catch (error) {
//     console.error("Error fetching audio:", error);
//     throw error;
//   }
// };

export const GetAudioFile = async () => {
  try {
    const response = await apiClient.get('/api/get_audio', {
      responseType: 'blob', // MP3 파일을 Blob으로 받기
    });
    const blob = new Blob([response.data], { type: 'audio/mp3' });
    return URL.createObjectURL(blob); // Blob을 URL로 변환하여 반환
  } catch (error) {
    console.error('Error fetching audio:', error);
    throw error;
  }
};


// 후기 받아오기
export const GetReviews = async (bookTitle: string) => {
  try {
    const response = await apiClient.post("/api/get_reviews",
      {
        bookTitle: bookTitle,
      }
    );
    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error get data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// 후기 업로드 하기
export const UploadReview = async (bookTitle: string, review: string) => {
  try {
    const response = await apiClient.post("/api/upload_review",
      {
        bookTitle: bookTitle,
        review: review
      }
    )

    return response.data;
  }
  catch (error) {
    console.error("Error upload data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};