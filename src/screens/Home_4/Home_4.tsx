import {
  BookOpen,
  HomeIcon,
  TimerIcon,
  TrophyIcon,
} from "lucide-react";

  import { Vector } from "../../icons/Vector";  
  import { Button } from "../../components/ui/button";
  import { Card, CardContent } from "../../components/ui/card";
  import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
  import { Calendar2Server } from "../../api/api";
  
  
  const navigationItems = [
    { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
    { icon: HomeIcon, label: "HOME", href: "/Home", active: true },
    { icon: BookOpen  , label: "BOOKS", href: "/Library", active: false },
    { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
  ];
  
  export const Home4 = (): JSX.Element => {
    const location = useLocation();
    const navigate = useNavigate();
    
    const data = location.state || {};

    return (
      <div className="flex justify-center w-full bg-white">
        <div className="relative w-[393px] h-[852px] bg-white">
          {/* Top Bar */}
          <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

          {/* Main Content */}
          <div className="flex flex-col items-center px-4">
            <h2 className="mt-[147px] text-lg font-bold text-center font-inter">
              클로바가 이런 책을 추천해드려요!
            </h2>
  
            <Card className="mt-12 border-none">
              <CardContent className="flex flex-col items-center p-0">
                <img
                  className="w-[137px] h-[183px] object-cover"
                  alt="Book cover"
                  // src="./image_data/rectangle-15@2x.png"
                  src = {data.bookimage}
                />
              </CardContent>
            </Card>
  
            <div className="w-[299px] mt-4">
              <h1 className="text-3xl font-bold text-center">{data.bookTitle}</h1>
            </div>
  
            <div
              className="w-[325px] mt-4 bg-[#e1e1e1] rounded-md p-4 text-base font-normal overflow-auto max-h-[200px]"
            >
              <p>
                {data.description}
              </p>
            </div>
  
            <div className="flex w-[324px] gap-2 mt-4">
              <Button
                variant="secondary"
                className="flex-1 rounded-[20px_3px_3px_20px] bg-[#d9d9d9] hover:bg-[#c4c4c4]"
                onClick={() => navigate("/Home", { replace: true })}
              >
                처음으로 돌아가기
              </Button>
              <Button
                variant="secondary"
                className="flex-1 rounded-[3px_20px_20px_3px] bg-[#d9d9d9] hover:bg-[#c4c4c4]"
                onClick={() => {
                  Calendar2Server(data.question, data.bookimage, data.bookTitle);
                  navigate("/Calendar", { replace: true })
                  }
                }
              >
                캘린더에 저장하기
              </Button>
            </div>
          </div>
  
          {/* Bottom Navigation */}
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
  