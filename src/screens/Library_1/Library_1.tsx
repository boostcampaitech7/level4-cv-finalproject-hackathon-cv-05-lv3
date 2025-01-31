import { useEffect, useState } from "react";
import { BookOpen, HomeIcon, TimerIcon, TrophyIcon } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { Vector } from "../../icons/Vector";
import { useNavigate, useLocation } from "react-router-dom";
import { Badge2Server } from "../../api/api";

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
  { icon: BookOpen, label: "BOOKS", href: "/Library", active: true },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
];

export const Library_1 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  const books = location.state || {};

  const MakeBadge = async () => {
    Badge2Server();
    navigate("/Challenge", { replace: true });
  };

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
        <img
          className="top-[95px] left-3.5 absolute w-[365px] h-px object-cover"
          alt="Line"
          src="../../image_data/line-4.svg"
        />

        <img
          className="top-[425px] left-2.5 absolute w-[365px] h-px object-cover"
          alt="Line"
          src="../../image_data/line-4.svg"
        />

        <div className="absolute top-[428px] left-3.5 [font-family:'Koulen',Helvetica] font-normal text-black text-xl text-center tracking-[0] leading-[normal]">
          {books.date}
        </div>

        <img
          className="absolute w-[230px] h-[308px] top-[107px] left-[82px] object-cover"
          alt="Rectangle"
          src = {books.bookimage}
        />

        <div className="absolute top-14 left-3.5 [font-family:'Koulen',Helvetica] font-normal text-black text-xl text-center tracking-[0] leading-[normal]">
          {books.bookTitle}
        </div>

        <div className="w-[361px] h-[170px] items-start gap-2.5 p-2.5 top-[476px] left-3.5 flex absolute">
          <div className="relative w-fit mt-[-1.00px] [font-family:'Koulen',Helvetica] font-normal text-black text-base text-left tracking-[0] leading-[normal]">
            {books.question}
          </div>
        </div>

        <button
          className="w-[361px] flex items-center justify-center gap-2.5 p-2.5 bg-[#d9d9d9] rounded-[20px] absolute top-[678px] left-3.5 text-black text-lg font-normal [font-family:'Inter',Helvetica]"
          onClick={() => MakeBadge()}
        >
          완독 버튼
        </button>

        {/* Bottom Navigation */}
        <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
          <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
            {navigationItems.map((item) => (
              <button
                key={item.label}
                onClick={() => navigate(item.href, { replace: true })}
                className="flex flex-col items-center w-[82px] h-[75px] bg-transparent border-none"
              >
                <item.icon
                  className={`w-14 h-14 ${item.active ? "text-black" : "text-[#b3b3b3]"}`}
                />
                <span
                  className={`font-['Koulen'] text-xl ${item.active ? "text-black" : "text-[#b3b3b3]"}`}
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
