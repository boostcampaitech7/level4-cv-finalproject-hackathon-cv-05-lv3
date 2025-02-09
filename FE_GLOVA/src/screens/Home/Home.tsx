import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Avatar, AvatarImage } from "../../components/ui/avatar";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { HelpCircle } from "lucide-react";
import NaviBar from "../../components/ui/navigationbar";
import { RemoveCookie } from "../../api/cookies"; // ✅ 쿠키 삭제 함수 가져오기
import apiClient from "../../api/cookies"; // ✅ Axios 설정 가져오기

export const Home = (): JSX.Element => {
  const navigate = useNavigate();
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  // ✅ 로그인 여부 확인 (useEffect 실행)
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        console.log("🔍 인증 상태 확인 중...");
        const response = await apiClient.get("/api/check-auth");

        if (response.data.user_id) {
          console.log("✅ 로그인된 사용자 ID:", response.data.user_id);
          setUserId(response.data.user_id);
        } else {
          console.warn("⚠️ 인증 실패! 로그인 페이지로 이동");
          RemoveCookie();
          navigate("/", { replace: true });
        }
      } catch (error) {
        console.error("🚨 인증 확인 요청 실패:", error);
        RemoveCookie();
        navigate("/", { replace: true });
      }
    };

    checkAuth();
  }, [navigate]);

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        {/* 상단 도움말 아이콘 */}
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
                <AvatarImage src="./image_data/Symbol_clova.jpg" alt="Profile" />
              </Avatar>

              <div className="mt-8 text-center">
                <p className="font-bold text-xl mb-4">
                  클로바에게 <br /> 책을 추천받아 보세요!
                </p>
                <Button
                  variant="secondary"
                  className="w-full bg-[#e1e1e1] rounded-[15px] font-bold text-lg active:scale-95 transition-transform duration-150 hover:bg-[#d1d1d1]"
                  onClick={() => navigate("/Home_1", { replace: true })}
                >
                  시작하기!
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <NaviBar activeLabel="Home" />
      </div>
    </div>
  );
};

export default Home;