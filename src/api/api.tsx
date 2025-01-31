import axios from 'axios';

// Axios 기본 설정
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // 서버의 기본 URL
  withCredentials: true, // 세션 쿠키 포함
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Calendar_Data {
  date: string; // YYYY-MM-DD 형식
  time: string; // HH:mm 형식
  bookTitle: string;
  bookimage: string;
  question: string;
}

export interface Book {
  date: string;
  time: string;
  bookTitle: string;
  bookimage: string;
  question: string;
}

export interface Badge {
  createAt: string;
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
export const Calendar2Server = async (question: string, bookimage: string, bookTitle: string) => {
  const now = new Date();
  try {
    // 서버에 데이터를 전송합니다.
    const response = await apiClient.post("/api/save_books", {
      "date": now.toISOString().split("T")[0], // YYYY-MM-DD 형식의 날짜
      "time": now.toTimeString().split(" ")[0], // HH:mm:ss 형식의 시간
      "question": question,
      "bookimage": bookimage,
      "bookTitle": bookTitle,
    });

    // 서버 응답 데이터 반환
    console.log(response.data.message); // "Book_data saved Successfully" 출력
    return response.data; // 서버에서 반환된 데이터를 호출자에게 전달
  } catch (error) {
    console.error("Error sending data:", error);
    throw error; // 호출자에게 예외를 전달
  }
};

// 당일 날짜의 데이터 목록 가져오기기
// export const Server2Calendar = async (date: string): Promise<Calendar_Data[]> => {
//   try {
//     const response =await apiClient.post("/api/calendar",
//       { 
//       "date": date 
//       }
//     );

//     if (response.status !== 200) {
//       throw new Error(`Failed to fetch events: ${response.statusText}`);
//     }

//     const data: Calendar_Data[] = response.data;
//     return data;
//   }
//   catch (error) {
//     console.error("Error fetching events:", error);
//     throw error; // 호출한 쪽에서 에러를 처리하도록 전달
//   }
// };

// 책 정보 전부 가져오기
export const Server2Books = async (): Promise<Book[]> => {
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
export const Badge2Server = async () => {
  try {
    const response = await apiClient.post("/api/badge_create");

    return response.data; // 서버에서 받은 데이터를 반환

  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // 호출한 측에서 에러를 처리할 수 있도록 던짐
  }
};


export const Server2Badge = async (): Promise<Badge[]> => {
  try {
    const response = await apiClient.get("/api/badge");

    if (response.status !== 200) {
      throw new Error(`서버 오류: ${response.status}`);
    }

    return response.data; // Axios는 자동으로 JSON 파싱을 수행하므로 response.data를 반환
  } catch (error) {
    console.error("Error fetching books:", error);
    return []; // 오류 발생 시 빈 배열 반환
  }
};