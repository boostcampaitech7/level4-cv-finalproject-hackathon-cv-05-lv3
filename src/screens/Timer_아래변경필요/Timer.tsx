import {
  BookOpen,
  HomeIcon,
  TimerIcon,
  TrophyIcon,
} from "lucide-react";

import React, { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";

import { Vector } from "../../icons/Vector";  
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import { Calendar2Server } from "../../api/api";


const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
  { icon: BookOpen  , label: "BOOKS", href: "/Library", active: false },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: true },
];

export const Timer = (): JSX.Element => {
  const navigate = useNavigate();

  const [time, setTime] = useState({ hours: 0, minutes: 0, seconds: 0 });
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(100);
  const [showModal, setShowModal] = useState(false);
  const totalSeconds = time.hours * 3600 + time.minutes * 60 + time.seconds;

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isRunning && totalSeconds > 0) {
      timer = setInterval(() => {
        setTime((prevTime) => {
          const total = prevTime.hours * 3600 + prevTime.minutes * 60 + prevTime.seconds - 1;
          if (total <= 0) {
            clearInterval(timer);
            setIsRunning(false);
            return { hours: 0, minutes: 0, seconds: 0 };
          }
          setProgress((total / (time.hours * 3600 + time.minutes * 60 + time.seconds)) * 100);
          return {
            hours: Math.floor(total / 3600),
            minutes: Math.floor((total % 3600) / 60),
            seconds: total % 60,
          };
        });
      }, 1000);
    } else {
      clearInterval(timer);
    }
    return () => clearInterval(timer);
  }, [isRunning, totalSeconds]);

  const handleInputChange = (e) => {
    if (isRunning) return;
    const { name, value } = e.target;
    let intValue = Math.max(0, Math.min(name === "hours" ? 12 : 59, parseInt(value) || 0));
    setTime((prev) => ({ ...prev, [name]: intValue }));
  };

  return (
    <div className="flex justify-center w-full bg-white">
      <div className="relative w-[393px] h-[852px] bg-white">
        {/* Top Bar */}
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        {/* Main Content */}
        <div className="flex flex-col items-center justify-center w-full">
          <h2 className="text-3xl font-bold">시간 : 분 : 초</h2>
            <div className="relative mt-4">
              <div className="w-48 h-48 relative">
                <svg className="absolute top-0 left-0 w-full h-full" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="45" stroke="#ddd" strokeWidth="10" fill="none" />
                  <circle cx="50" cy="50" r="45" stroke="#ff6666" strokeWidth="10" fill="none" strokeDasharray="283" strokeDashoffset={(progress / 100) * 283} />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <img src="/mnt/data/image.png" alt="Timer Icon" className="w-16 h-16 cursor-pointer" onClick={() => setShowModal(true)} />
                </div>
              </div>
            </div>
            <div className="flex gap-2 mt-5">
              <input type="number" name="hours" value={time.hours} onChange={handleInputChange} className="w-14 text-center border" disabled={isRunning} />
              <span>:</span>
              <input type="number" name="minutes" value={time.minutes} onChange={handleInputChange} className="w-14 text-center border" disabled={isRunning} />
              <span>:</span>
              <input type="number" name="seconds" value={time.seconds} onChange={handleInputChange} className="w-14 text-center border" disabled={isRunning} />
            </div>
            <div className="flex gap-4 mt-5">
              <Button onClick={() => setIsRunning((prev) => !prev)}>{isRunning ? "일시정지" : "타이머 시작"}</Button>
              <Button onClick={() => { setTime({ hours: 0, minutes: 0, seconds: 0 }); setIsRunning(false); setProgress(100); }}>초기화</Button>
            </div>
          
          <AnimatePresence>
            {showModal && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="w-4/5 h-2/3 bg-white rounded-xl p-5 shadow-lg">
                  <h2 className="text-xl font-bold">모달 창</h2>
                  <p>타이머 관련 추가 설정을 여기에 배치하세요.</p>
                  <Button onClick={() => setShowModal(false)}>닫기</Button>
                </div>
              </div>
            )}
          </AnimatePresence>
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
