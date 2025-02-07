import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { SaveCookie } from "../../api/cookies";

export const Login = (): JSX.Element => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const userInfo = searchParams.get("user");

  // 네이버 로그인 버튼 클릭 시 OAuth 요청
  const handleNaverLogin = () => {
    window.location.href = "http://localhost:8000/login/naver";
  };

  useEffect(() => {
    // FastAPI에서 리디렉트된 사용자 정보를 저장
    if (userInfo) {
      try {
        const parsedUser = JSON.parse(decodeURIComponent(userInfo));
        console.log("네이버 사용자 정보:", parsedUser);

        // ✅ 사용자 정보 쿠키 저장
        // SaveCookie("naver_user", JSON.stringify(parsedUser), 1);

        // ✅ 로그인 성공 후 홈으로 이동
        navigate("/");
      } catch (error) {
        console.error("사용자 정보 파싱 오류:", error);
      }
    }
  }, [userInfo, navigate]);

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
