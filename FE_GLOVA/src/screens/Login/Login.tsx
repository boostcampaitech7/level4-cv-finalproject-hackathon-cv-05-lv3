import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Local_login } from "../../api/api";
import { cookie_loader, cookies_saver } from "../../api/cookies";

export const Login = (): JSX.Element => {
  const navigate = useNavigate();
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // // ✅ 네이버 로그인 버튼 클릭 시 OAuth 요청
  // const handleNaverLogin = () => {
  //   console.log("🚀 네이버 로그인 시작!");
  //   window.open("http://localhost:8000/login/naver", "_self"); // 기존 창에서 이동
  // };

  // useEffect(() => {
  //   // URL에서 code와 state 추출
  //   const urlParams = new URLSearchParams(window.location.search);
  //   const code = urlParams.get("code");
  //   const state = urlParams.get("state");

  //   if (code && state) {
  //     console.log("🔍 OAuth Callback URL 감지됨!", { code, state });

  //     fetch(`http://localhost:8000/api/login/naverOAuth?code=${code}&state=${state}`, {
  //       method: "GET",
  //       credentials: "include" // 쿠키 포함
  //     })
  //       .then(response => response.json())
  //       .then(data => {
  //         console.log("✅ 로그인 성공 응답:", data);
  //         if (data.redirect_url) {
  //           navigate(data.redirect_url); // 리액트 라우터를 사용하여 리디렉션
  //         }
  //       })
  //       .catch(error => console.error("🚨 네이버 OAuth 로그인 에러:", error));
  //   }
  // }, []);

  const LoginClickHandler = async () => {
    if (isLoading) return; // 중복 요청 방지
  
    setIsLoading(true);
    setError("");
    try {
      const response = await Local_login(userId, password);
  
      if (response.status === "success") {
        cookies_saver(userId);
        navigate("/Home", { replace: true });
      } else {
        setError("로그인 실패. 다시 시도해주세요.");
      }

    } catch (error) {
      console.error("🚨 로그인 에러:", error);

    } finally {
      setIsLoading(false);
    }
  };
  


  return (
    <main className="flex justify-center items-center min-h-screen bg-whit">
     <div className="w-[393px] flex flex-col items-center px-4 bg-white">
        {/* <img className="w-[250px] h-[148px] mb-4 object-cover" alt="Logo" src="./image_data/rectangle-4@2x.png" /> */}
        <p className="text-[40px] text-center text-green-500 font-SBAggroB">
          Hi Book
        </p>
        <p className="text-[60px] text-center text-black font-SBAggroB mb-5">
          GLOVA
        </p>

        <p className="text-xl text-center text-black font-SBAggroB mb-12">
          함께 읽어가는 우리들의 챌린지
        </p>

        {/* <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Button onClick={handleNaverLogin} className="px-4 py-2 bg-green-500 text-white rounded active:scale-95 transition-transform duration-150 hover:bg-green-600">
              네이버 로그인
            </Button>
          </CardContent>
        </Card> */}
        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <input
              type="text"
              placeholder="User ID"
              className="w-[250px] p-2 border rounded-md focus:outline-none focus:ring focus:ring-green-300"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="w-[250px] p-2 border rounded-md focus:outline-none focus:ring focus:ring-green-300"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <Button
              className={`w-[250px] px-4 py-3 rounded active:scale-95 transition-transform duration-150 ${
                isLoading ? "bg-green-900 cursor-not-allowed" : "bg-green-500 hover:bg-green-600"
              }`}
              onClick={LoginClickHandler}
              disabled={isLoading}
            >
              {isLoading ? "로그인 중..." : "로그인"}
            </Button>
          </CardContent>
        </Card>

        <Button onClick={() => navigate("/Regi", {replace: true})} className="px-2 py-3 h-[10px] bg-green-500 text-white rounded active:scale-95 transition-transform duration-150 hover:bg-green-600">
          회원가입
        </Button>
      </div>
    </main>
  );
};
