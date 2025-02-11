import { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import { Avatar, AvatarImage } from "../../components/ui/avatar";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { HelpCircle } from "lucide-react";
import NaviBar from "../../components/ui/navigationbar";
import apiClient from "../../api/cookies"; // ✅ Axios 설정 가져오기
import { cookie_loader, cookie_remover } from "../../api/cookies";
import Cookies from "js-cookie";

export const Home = (): JSX.Element => {
  const navigate = useNavigate();
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    // ✅ 1. 쿠키에서 id 가져오기
    const userIdFromCookie = cookie_loader();

    if (!userIdFromCookie) {
      console.warn("⚠️ 인증 실패! 쿠키가 없음. 로그인 페이지로 이동 (쿠키 생성 실패 또는 쿠키 유효시간 만료)");
      cookie_remover();
      navigate("/", { replace: true });
      return; // 함수 종료
    }
    
  }, [navigate]);

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
        {/* 상단 아이콘 */}
        <button
          className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
          onClick={() => setIsInfoModalOpen(true)}
        >
          <HelpCircle size={24} />
        </button>

        <div className="bg-white absolute w-[285px] top-[294px] left-1/2 -translate-x-1/2">
          <Card className="relative border shadow-[0px_2px_10px_#00000040] rounded-[15px] border-2 border-black">
            <CardContent className="p-5">
              {/* 프로필 아바타 */}
              <Avatar className="w-[61px] h-[61px] absolute -top-8 left-1/2 -translate-x-1/2 border border-black">
                <AvatarImage
                  src="./image_data/Symbol_clova.jpg"
                  alt="Profile"
                />
              </Avatar>

              <div className="mt-8 text-center">
                <p className="text-[20px] mb-4 font-extrabold tracking-wide style={{ fontFamily: 'Freesentation'}}">
                  클로바에게 <br /> 책을 추천받아 보세요!
                </p>
                <Button
                  variant="secondary"
                  className="w-full bg-[#e1e1e1] rounded-[15px] style={{ fontFamily: 'Freesentation'}} font-black text-xl active:scale-95 transition-transform duration-150 hover:bg-[#d1d1d1]"
                  onClick={() => navigate("/Home_1", { replace: true })}
                >
                  시작하기!
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img
                src="../../image_data/Guide/Home.png"
                alt="도움말 이미지"
                className="w-full h-auto rounded-md"
              />
              <button
                className="mt-4 px-4 py-2 bg-gray-500 text-white rounded-lg font-Freesentation"
                onClick={() => setIsInfoModalOpen(false)}
              >
                닫기
              </button>
            </div>
          </div>
        )}

        <NaviBar activeLabel="Home" />
      </div>
    </div>
  );
};

export default Home;
