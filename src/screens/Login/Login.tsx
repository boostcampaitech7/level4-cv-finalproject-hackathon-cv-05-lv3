import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { SaveCookie } from "../../api/cookies";

const CLIENT_ID = "L8G4GvryZzm9JCEvmrHh";
const NAVER_AUTH_URL = "https://nid.naver.com/oauth2.0/authorize";
const CALLBACK_URL = "http://localhost:3000/api/login/naverOAuth"; // 백엔드에서 처리하도록 함

export const Login = (): JSX.Element => {
  const navigate = useNavigate();
  const [code, setCode] = useState<string | null>(null);

  // 네이버 로그인 버튼 클릭 시 OAuth 요청
  const handleNaverLogin = () => {
    const state = Math.random().toString(36).substring(2, 15);
    sessionStorage.setItem("naver_state", state);
    window.location.href = `${NAVER_AUTH_URL}?response_type=code&client_id=${CLIENT_ID}&state=${state}&redirect_uri=${encodeURIComponent(CALLBACK_URL)}`;
  };

  // 로그인 후 콜백 URL에서 인증 코드 추출 및 토큰 요청
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const authCode = params.get("code");
    const receivedState = params.get("state");
    const storedState = sessionStorage.getItem("naver_state");

    if (authCode && receivedState === storedState) {
      setCode(authCode);
      exchangeToken(authCode, receivedState);
    }
  }, []);

  // 서버에 인증 코드를 보내고 액세스 토큰 받기
  const exchangeToken = async (authCode: string, receivedState: string) => {
    try {
      const response = await axios.post("http://localhost:8000/api/naver/token", {
        code: authCode,
        state: receivedState,
      });

      SaveCookie(
        response.data.access_token,
        response.data.refresh_token,
        response.data.token_type,
        response.data.expires_in
      )

      console.log("🔑 Access Token:", response.data.access_token);
      console.log("🔑 expires_in:", response.data.expires_in);

      // 로그인 성공 후 Home으로 이동
      navigate("/Home", { replace: true });
    } catch (error) {
      console.error("네이버 로그인 토큰 요청 실패:", error);
    }
  };

  return (
    <main className="flex justify-center items-center min-h-screen bg-white">
      <div className="w-[393px] flex flex-col items-center px-4">
        <img className="w-[250px] h-[148px] mb-4 object-cover" alt="Logo" src="./image_data/rectangle-4@2x.png" />
        <p className="text-xl text-center text-black font-normal mb-8">
          오늘은 또 무슨일이 생길까 피카츄 라이츄 파이리 꼬부기 버터풀 라이츄 디지몬 친구들~
        </p>

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Button onClick={handleNaverLogin} className="px-4 py-2 bg-green-500 text-white rounded">
              네이버 로그인
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
