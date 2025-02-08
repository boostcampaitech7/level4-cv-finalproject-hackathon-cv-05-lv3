import Cookies from "js-cookie";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

// Axios 기본 설정
const apiClient = axios.create({
    baseURL: 'http://localhost:8000', // 서버의 기본 URL
    withCredentials: true, // 세션 쿠키 포함
    headers: {
      'Content-Type': 'application/json',
    },
});

// JWT token 양식
interface DecodedToken {
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
  }

// 쿠키 저장
export const SaveCookie = (jwtToken:string) => {
    const decodedToken : DecodedToken = jwtDecode(jwtToken);
    
    const expires = new Date(new Date().getTime() + decodedToken.expires_in * 1000);
    Cookies.set("access_token", decodedToken.access_token, { expires, secure: true, sameSite: "Strict" });
    Cookies.set("refresh_token", decodedToken.refresh_token, { expires, secure: true, sameSite: "Strict" });
    Cookies.set("token_type", decodedToken.token_type, { expires, secure: true, sameSite: "Strict" });

    console.log("🔐 토큰이 쿠키에 저장되었습니다.");
};

// 쿠키에서 토큰 가져오기
export const GetCookie = () => {
    return {
        access_token: Cookies.get("access_token"),
        refresh_token: Cookies.get("refresh_token"),
        token_type: Cookies.get("token_type"),
    };
};

// 쿠키 삭제
export const RemoveCookie = () => {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    Cookies.remove("token_type");

    console.log("🗑️ 토큰이 삭제되었습니다.");
};

// 토큰 갱신 함수 (refresh_token을 사용하여 새 access_token 요청)
export const RefreshToken = async () => {
    const refresh_token = Cookies.get("refresh_token");

    if (!refresh_token) {
        console.warn("⚠️ 갱신할 refresh_token이 없습니다.");
        return;
    }

    try {
        const response = await apiClient.post("/login/refresh", {
            refresh_token
        });

        const { access_token, refresh_token: new_refresh_token, token_type, expires_in } = response.data;

        // 새 토큰 저장
        SaveCookie(access_token, new_refresh_token, token_type, expires_in);
        console.log("🔄 토큰이 갱신되었습니다.");

        // 새 만료 시간 기준으로 다시 갱신 스케줄 설정
        ScheduleTokenRefresh(expires_in);
    } catch (error) {
        console.error("❌ 토큰 갱신 실패:", error);
        RemoveCookie();
    }
};

// **동적 갱신 스케줄링 (setTimeout 사용)**
let refreshTimeout: NodeJS.Timeout | null = null;

export const ScheduleTokenRefresh = (expires_in: number) => {
    if (refreshTimeout) {
        clearTimeout(refreshTimeout); // 기존 타이머 제거 (중복 방지)
    }

    const refreshTime = (expires_in - 300) * 1000; // 만료 5분 전 (300초) 갱신

    console.log(`🔄 ${refreshTime / 1000}초 후에 토큰을 자동 갱신합니다.`);

    refreshTimeout = setTimeout(() => {
        RefreshToken();
    }, refreshTime);
};

// 앱 시작 시 자동으로 갱신 스케줄 실행
export const StartTokenRefresh = () => {
    const tokenInfo = GetCookie();

    if (!tokenInfo.access_token) {
        console.warn("❌ access_token이 없어 자동 갱신을 시작할 수 없습니다.");
        return;
    }

    const expiresInSeconds = 3600; // API에서 받은 expires_in 값 (예: 1시간)
    ScheduleTokenRefresh(expiresInSeconds);
};

// 앱이 종료될 때 인터벌 제거**
export const StopTokenRefresh = () => {
    if (refreshTimeout) {
        clearTimeout(refreshTimeout);
        refreshTimeout = null;
        console.log("⏹️ 자동 토큰 갱신이 중지되었습니다.");
    }
};
