import Cookies from "js-cookie";
import axios from "axios";

// ✅ Axios 기본 설정 (쿠키 포함)
const apiClient = axios.create({
    baseURL: "http://223.195.111.52:8080",
    withCredentials: true, // ✅ 쿠키 자동 포함
    headers: {
        "Content-Type": "application/json",
    },
});

// ✅ 쿠키 삭제 함수
export const RemoveCookie = () => {
    Cookies.remove("access_token", { path: "/" });
    console.log("🗑️ Access Token이 삭제되었습니다.");
};

// ✅ Access Token 자동 갱신 함수
const refreshAccessToken = async () => {
    try {
        console.log("🔄 Access Token 갱신 시도 중...");
        const response = await axios.get("http://223.195.111.52:8080/api/refresh-token", {
            withCredentials: true, // ✅ 쿠키 포함하여 요청
        });

        console.log("✅ Access Token 갱신 완료:", response.data);
        return response.data; // 새로운 Access Token 반환
    } catch (error) {
        console.error("🚨 Access Token 갱신 실패:", error);
        RemoveCookie(); // 실패 시 쿠키 삭제
        window.location.href = "/"; // 로그인 페이지로 이동
        throw error;
    }
};

// ✅ Axios 응답 인터셉터 추가 (401 에러 발생 시 처리)
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response && error.response.status === 401) {
            console.warn("🔒 Unauthorized - Access Token 만료! 자동 갱신 실행");

            try {
                const newToken = await refreshAccessToken(); // 🔄 새 Access Token 요청
                console.log("🔄 새로운 Access Token:", newToken);

                // ✅ 자동으로 실패한 요청을 다시 보냄
                return apiClient(error.config);
            } catch (refreshError) {
                console.error("❌ Access Token 갱신 실패:", refreshError);
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
