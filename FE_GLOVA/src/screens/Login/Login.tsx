import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";

export const Login = (): JSX.Element => {
  const navigate = useNavigate();

  // ✅ 네이버 로그인 버튼 클릭 시 OAuth 요청
  const handleNaverLogin = () => {
    console.log("🚀 네이버 로그인 시작!");
    window.open("http://223.195.111.52:8080/login/naver", "_self"); // 기존 창에서 이동
  };

  useEffect(() => {
    // URL에서 code와 state 추출
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const state = urlParams.get("state");

    if (code && state) {
      console.log("🔍 OAuth Callback URL 감지됨!", { code, state });

      fetch(`http://223.195.111.52:8080/api/login/naverOAuth?code=${code}&state=${state}`, {
        method: "GET",
        credentials: "include" // 쿠키 포함
      })
        .then(response => response.json())
        .then(data => {
          console.log("✅ 로그인 성공 응답:", data);
          if (data.redirect_url) {
            navigate(data.redirect_url); // 리액트 라우터를 사용하여 리디렉션
          }
        })
        .catch(error => console.error("🚨 네이버 OAuth 로그인 에러:", error));
    }
  }, []);

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

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Button onClick={handleNaverLogin} className="px-4 py-2 bg-green-500 text-white rounded active:scale-95 transition-transform duration-150 hover:bg-green-600">
              네이버 로그인
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
