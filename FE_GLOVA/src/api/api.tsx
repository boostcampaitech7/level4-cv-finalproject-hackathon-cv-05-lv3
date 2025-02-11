import apiClient, { cookies_saver, cookie_loader, cookie_remover } from "./cookies";

export interface Reviews {
  user_id: string;
  text: string;
}

export interface Book {
  recommendationId: number;
  date: string;
  time: string;
  bookId: number;
  bookTitle: string;
  bookImage: string;
  questionText: string;
}

export interface Badge {
  createdAt: string;
  badgeImage: string;
  bookTitle: string;
}



// *회원가입 중복검사
export const DuplicateCheck = async (id: string) => {
  try {
    const response = await apiClient.post("/api/dupli_check", {
      id: id
    });

    return response;
  }
  catch (error) {
    console.error("Error duplication data: ", error);
    throw error;
  }
};


// *회원가입 데이터 저장
export const SaveUserdata = async (id: string, password: string, birth: number, gender: string) => {
  try {
    const response = await apiClient.post("/db/users", {
      user_id: id,
      user_pw: password,
      birth_year: birth,
      gender: gender
    });

    return response;
  }
  catch (error) {
    console.error("Error register data: ", error);
    throw error;
  }
};


//* 로그인하기
export const Local_login = async (id: string, password: string) => {
  try {
    const response = await apiClient.post("/api/local_login", {
      id: id,
      password: password
    });

    return response.data;
  }
  catch (error) {
    console.error("Error login data: ", error);
    throw error;
  }
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
    const id = cookie_loader();

    const requestData = {
      id: id,
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
export const GetRecommandBooks = async () => {
  try {
    const id = cookie_loader();
    const response = await apiClient.get("/api/recommended_books");
    console.log("✅ 추천 도서 데이터:", response.data);
    return response.data.response_body;  // ❗ 'response_body' 내부 데이터만 반환
  } catch (error) {
    console.error("❌ Error fetching recommended books:", error);
    throw error;
  }
};


// *책 정보 전부 가져오기
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

export const PostReadFinished = async (recommendationId: number, speak: string) => {
  try {
    const response = await apiClient.post("/api/notify_read_finished", {
      recommendationId: recommendationId
    });

    console.log(speak, response.data);
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// 뱃지 생성 요청
export const PostBadgeMaker = async (bookId: number) => {
  const now = new Date();
  // 날짜를 KST(한국 표준시)로 변환
  const date = now.toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' })
    .replace(/. /g, '-').replace('.', ''); // YYYY-MM-DD 포맷
  try {
    // 개인 사용자 구별
    const id = cookie_loader();

    const response = await apiClient.post("/api/badge_create",
      {
        date: date,
        time: now.toTimeString().split(" ")[0], // HH:mm:ss
        bookId: bookId,
      }
    );

    return response; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// *뱃지 가져오기
export const GetBadges = async (): Promise<Badge[]> => {
  try {
    // 개인 사용자 구별
    const id = cookie_loader();
    const response = await apiClient.get("/api/badge");

    // const response = await apiClient.post("/api/badge");

    if (response.status !== 200) {
      throw new Error(`서버 오류: ${response.status}`);
    }
    console.log(response.data)
    return response.data; // ✅ 서버에서 받은 뱃지 데이터 반환
  } catch (error) {
    console.error("❌ Error fetching badges:", error);
    return []; // 오류 발생 시 빈 배열 반환
  }
};


// *후기 받아오기
export const GetReviews = async (bookId: number) => {
  try {
    // 개인 사용자 구별
    const id = cookie_loader();

    const response = await apiClient.post("/api/get_reviews",
      {
        id: id,
        bookId: bookId,
      }
    );
    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error get data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// *후기 업로드 하기
export const UploadReview = async (bookId: number, review: string) => {
  try {
    // 개인 사용자 구별
    const id = cookie_loader();
    const response = await apiClient.post("/api/upload_review",
      {
        id: id,
        bookId: bookId,
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