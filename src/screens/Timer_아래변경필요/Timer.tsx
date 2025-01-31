import {
  BookOpen,
    HomeIcon,
    TimerIcon,
    TrophyIcon,
  } from "lucide-react";
  import { Vector } from "../../icons/Vector";
  import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
  
  const navigationItems = [
    { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
    { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
    { icon: BookOpen  , label: "BOOKS", href: "/Library", active: false },
    { icon: TimerIcon, label: "TIMER", href: "/Timer", active: true },
  ];
  
  export const Timer = (): JSX.Element => {
    const navigate = useNavigate();
    
    return (
      <div className="bg-white flex flex-row justify-center w-full">
        <div className="bg-white w-full max-w-[393px] h-[852px] relative">
          <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
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
  