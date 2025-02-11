import apiClient, { cookies_saver, cookie_loader, cookie_remover} from "./cookies";

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
export const SaveUserdata = async (id: string, password:string, birth:number, gender:string) => {
  try {
    const response = await apiClient.post("/api/regiseter", {
      id: id,
      user_pw: password,
      birth: birth,
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
      user_pw: password
    });

    return response;
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

// *서버한테 데이터 저장하라고 하기
export const SaveRecommand = async (question: string, bookimage: string, bookTitle: string) => {
  const now = new Date();
  try {
    const id = cookie_loader();

    // 서버에 데이터를 전송합니다.
    const response = await apiClient.post("/api/save_books", {
      // id: id, // 개인 사용자 구별
      date: now.toISOString().split("T")[0], // YYYY-MM-DD 형식의 날짜
      time: now.toTimeString().split(" ")[0], // HH:mm:ss 형식의 시간
      question: question,
      bookimage: bookimage,
      bookTitle: bookTitle,
    });

    // 서버 응답 데이터 반환
    console.log(response.data.message); // "Book_data saved Successfully" 출력
    return response.data; // 서버에서 반환된 데이터를 호출자에게 전달
  } catch (error) {
    console.error("Error sending data:", error);
    throw error; // 호출자에게 예외를 전달
  }
};


// *추천받은 책 정보 전부 가져오기
export const GetRecommandBooks = async (): Promise<Book[]> => {
  try {
    // 개인 사용자 구별
    // const id = cookie_loader();
    // const response = await apiClient.post("/api/recommand_books", {id: id});

    const response = await apiClient.post("/api/recommand_books");

    return response.data; // Axios는 자동으로 JSON 파싱을 수행하므로 response.data를 반환
  } catch (error) {
    console.error("Error fetching books:", error);
    return []; // 오류 발생 시 빈 배열 반환
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


// *뱃지 생성 요청
export const PostBadgeMaker = async (bookTitle: string) => {
  try {
    // 개인 사용자 구별
    // const id = cookie_loader();

    const response = await apiClient.post("/api/badge_create",
      {
        // id: id,
        bookTitle: bookTitle,
      }
    );

    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// *뱃지 가져오기
export const GetBadges = async (): Promise<Badge[]> => {
  try {
    // 개인 사용자 구별
    // const id = cookie_loader();
    // const response = await apiClient.post("/api/badge", { id: id });

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


// *후기 받아오기
export const GetReviews = async (bookTitle: string) => {
  try {
    // 개인 사용자 구별
    // const id = cookie_loader();

    const response = await apiClient.post("/api/get_reviews",
      {
        // id: id,
        bookTitle: bookTitle,
      }
    );
    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error get data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};

// *후기 업로드 하기
export const UploadReview = async (bookTitle: string, review: string) => {
  try {
    // 개인 사용자 구별
    // const id = cookie_loader();
    const response = await apiClient.post("/api/upload_review",
      {
        // id: id,
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