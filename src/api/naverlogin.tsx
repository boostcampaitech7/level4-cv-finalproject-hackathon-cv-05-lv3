import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const naverURL = 'https://nid.naver.com/oauth2.0/authorize';
const callbackUrl = 'http://localhost:3000/api/login/naverOAuth';

// 랜덤한 state 값 생성 함수
const generateState = (): string => {
  return Math.random().toString(36).substring(2, 15);
};

const CLIENT_ID = 'L8G4GvryZzm9JCEvmrHh';

export const NaverOAuth = ({ onLoginSuccess }: { onLoginSuccess: () => void }) => {
  const navigate = useNavigate();
  const [code, setCode] = useState<string | null>(null);
  
  // ✅ 로그인 요청 전에 state 값 저장 (CSRF 방지)
  const state_string = generateState();
  useEffect(() => {
    sessionStorage.setItem('naver_state', state_string);
  }, []);

  /** ✅ 네이버 로그인 요청 (GET 방식) */
  const authorize = () => {
    const authUrl = `${naverURL}?response_type=code&client_id=${CLIENT_ID}&state=${encodeURIComponent(state_string)}&redirect_uri=${encodeURIComponent(callbackUrl)}`;
    window.location.href = authUrl; // 네이버 로그인 페이지로 이동
  };

  /** ✅ 콜백 URL에서 code, state 값 가져오기 */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const receivedCode = params.get('code');
    const receivedState = params.get('state');

    const storedState = sessionStorage.getItem('naver_state');
    // if (!receivedCode || !receivedState || receivedState !== storedState) {
    //   console.error('⚠ CSRF 공격 가능성 있음!');
    //   return;
    // }

    setCode(receivedCode);
    exchangeToken(receivedCode, receivedState);
  }, []);

  /** ✅ 네이버 API에 인증 코드를 보내고 액세스 토큰 받기 */
  const exchangeToken = async (authCode: string, receivedState: string) => {
    try {
      const response = await axios.post("http://localhost:8000/api/naver/token", {
        code: authCode,
        state: receivedState,
      },
      { headers: { "Content-Type": "application/json" } }
    );
  
      console.log("🔑 Access Token:", response.data.access_token);
      console.log("🔑 expires_in:", response.data.expires_in);
      
      // ✅ 로그인 성공 시 콜백 실행
      onLoginSuccess();
      navigate('/Home', { replace: true });
    } catch (error) {
      console.error("❌ Error fetching token:", error);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <button onClick={authorize} className="px-4 py-2 bg-green-500 text-white rounded">
        네이버 로그인
      </button>
    </div>
  );
};

export default NaverOAuth;