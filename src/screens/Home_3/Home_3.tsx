import {
  BookOpen,
  HomeIcon,
  TimerIcon,
  TrophyIcon,
} from "lucide-react";

import { Calendar } from "../../components/ui/calendar";
import { Card, CardContent } from "../../components/ui/card";
import { Vector } from "../../icons/Vector";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import {Question2Server} from "../../api/api";
import { useEffect } from "react";

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: true },
  { icon: BookOpen  , label: "BOOKS", href: "/Library", active: false },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
];
export const Home3 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  const { age, gender, question } = location.state || {};

  useEffect(() => {
    const fetchAndNavigate = async () => {
      try {
        console.log(age, gender, question);
  
        // 새로 만든 fetchData 함수를 호출
        const data = await Question2Server(age, gender, question);
  
        // 데이터를 Home_4로 전달하며 페이지 이동
        navigate("/Home_4", { state: { ...data } });
      } catch (error) {
        console.error("Error while fetching data:", error);
      }
    };

    fetchAndNavigate();
  }, [navigate]);

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <div className="absolute top-[180px] left-8 font-bold text-black text-base text-center tracking-[0] leading-[normal] whitespace-nowrap">
          클로바가 무슨 책을 추천할지 고민 중입니다...
        </div>

        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]" />
        </div>

        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        <Card className="absolute w-[351px] top-[220px] left-[21px] border-none">
          <CardContent className="p-0">
            <img
              className="w-full h-[486px]"
              alt="Mini game display"
              src="./image_data/group-3@2x.png"
            />
          </CardContent>
        </Card>

        {/* Navigation Bar */}
        <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
          <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
            {navigationItems.map((item) => (
              <button
                key={item.label}
                onClick={() => navigate(item.href, { replace: true })} // replace 옵션으로 뒤로가기 방지
                className="flex flex-col items-center w-[82px] h-[75px] bg-transparent border-none"
              >
                <item.icon
                  className={`w-14 h-14 ${
                    item.active ? "text-black" : "text-[#b3b3b3]"
                  }`}
                />
                <span
                  className={`font-['Koulen'] text-xl ${
                    item.active ? "text-black" : "text-[#b3b3b3]"
                  }`}
                >
                  {item.label}
                </span>
              </button>
            ))}
          </div>
        </nav>
      </div>
    </div>
  );
};
