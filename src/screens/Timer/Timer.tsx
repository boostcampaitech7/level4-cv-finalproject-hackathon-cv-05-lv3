// import {
//   BookOpen,
//   HomeIcon,
//   TimerIcon,
//   TrophyIcon,
// } from "lucide-react";

// import React, { useState, useEffect } from "react";
// import { AnimatePresence, motion } from "framer-motion";
// import { Vector } from "../../icons/Vector";  
// import { Button } from "../../components/ui/button";
// import { Card, CardContent } from "../../components/ui/card";
// import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
// import { Calendar2Server } from "../../api/api";
// import { TimerModal } from "./TimerModal";

// const navigationItems = [
//   { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
//   { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
//   { icon: BookOpen, label: "BOOKS", href: "/Library", active: false },
//   { icon: TimerIcon, label: "TIMER", href: "/Timer", active: true },
// ];

// export const Timer = (): JSX.Element => {
//   const navigate = useNavigate();

//   const [time, setTime] = useState({ hours: 0, minutes: 0, seconds: 0 });
//   const [isRunning, setIsRunning] = useState(false);
//   const [progress, setProgress] = useState(100);
//   const [initialTimeMs, setInitialTimeMs] = useState(0); // ✅ 최초 설정된 전체 시간 (ms)
//   const [remainingTimeMs, setRemainingTimeMs] = useState(0); // ✅ 남은 시간 (ms)
//   const [showModal, setShowModal] = useState(false);
//   const [image, setImage] = useState("../../image_data/rectangle-15@2x.png");

//   useEffect(() => {
//     let animationFrame: number;
//     let startTime = Date.now();
//     let endTime = startTime + remainingTimeMs;

//     const updateTimer = () => {
//       const now = Date.now();
//       const remainingMs = Math.max(0, endTime - now);

//       if (remainingMs <= 0) {
//         setIsRunning(false);
//         setTime({ hours: 0, minutes: 0, seconds: 0 });
//         setProgress(0);
//         return;
//       }

//       // 남은 시간을 시간, 분, 초로 변환
//       setTime({
//         hours: Math.floor(remainingMs / 3600000),
//         minutes: Math.floor((remainingMs % 3600000) / 60000),
//         seconds: Math.floor((remainingMs % 60000) / 1000),
//       });

//       // 게이지 바가 일정하게 줄어들도록 설정
//       setProgress((remainingMs / initialTimeMs) * 100);
      
//       animationFrame = requestAnimationFrame(updateTimer);
//     };

//     if (isRunning) {
//       animationFrame = requestAnimationFrame(updateTimer);
//     }

//     return () => cancelAnimationFrame(animationFrame);
//   }, [isRunning, remainingTimeMs]);

//   const handleInputChange = (e) => {
//     if (isRunning) return;
//     const { name, value } = e.target;
//     let intValue = Math.max(0, Math.min(name === "hours" ? 12 : 59, parseInt(value) || 0));
//     setTime((prev) => ({ ...prev, [name]: intValue }));
//   };

//   const startTimer = () => {
//     const totalMs = (time.hours * 3600 + time.minutes * 60 + time.seconds) * 1000;
//     if (totalMs > 0) {
//       setInitialTimeMs(totalMs);
//       setRemainingTimeMs(totalMs);
//       setIsRunning(true);
//     }
//   };

//   return (
//     <div className="flex flex-col justify-between items-center w-full h-screen bg-white">
//       <div className="relative w-[393px] h-[852px] bg-white flex flex-col justify-center items-center">
//         {/* Top Bar */}
//         <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
        
//         {/* Main Content */}
//         <div className="relative mt-4">
//           <div className="w-48 h-48 relative">
//             <svg className="absolute top-0 left-0 w-full h-full" viewBox="0 0 100 100">
//               <circle cx="50" cy="50" r="45" stroke="#ddd" strokeWidth="10" fill="none" />
//               <motion.circle
//                 cx="50"
//                 cy="50"
//                 r="45"
//                 stroke="#ff6666"
//                 strokeWidth="10"
//                 fill="none"
//                 strokeDasharray="566"
//                 strokeDashoffset={(progress / 100) * 566}
//                 initial={{ strokeDashoffset: 566 }}
//                 animate={{ strokeDashoffset: (progress / 100) * 566 }}
//                 transition={{
//                   duration: initialTimeMs / 1000, // ✅ 전체 타이머 지속 시간과 동일한 애니메이션 속도
//                   ease: "linear", // ✅ 부드럽게 일정한 속도로 감소
//                 }}
//                 style={{
//                   transform: "rotate(-90deg)",
//                   transformOrigin: "50% 50%",
//                 }}
//               />
//             </svg>
//             <div className="absolute inset-0 flex items-center justify-center">
//               <img src={image} className="w-16 h-16 cursor-pointer" onClick={() => setShowModal(true)} />
//             </div>
//           </div>
//         </div>

//         {/* 시간 입력 */}
//         <div className="flex gap-2 mt-5">
//           <input type="number" name="hours" value={time.hours} onChange={handleInputChange} className="w-14 text-xl text-center " disabled={isRunning} />
//           <span>:</span>
//           <input type="number" name="minutes" value={time.minutes} onChange={handleInputChange} className="w-14 text-xl text-center" disabled={isRunning} />
//           <span>:</span>
//           <input type="number" name="seconds" value={time.seconds} onChange={handleInputChange} className="w-14 text-xl text-center" disabled={isRunning} />
//         </div>

//         {/* 타이머 버튼 */}
//         <div className="flex gap-4 mt-5">
//           <Button onClick={startTimer}>{isRunning ? "일시정지" : "타이머 시작"}</Button>
//           <Button
//             onClick={() => {
//               setTime({ hours: 0, minutes: 0, seconds: 0 });
//               setIsRunning(false);
//               setInitialTimeMs(0);
//               setRemainingTimeMs(0);
//               setProgress(100);
//             }}
//           >
//             초기화
//           </Button>
//         </div>

//         <TimerModal showModal={showModal} setShowModal={setShowModal} onBookSelect={setImage} />

//         {/* Bottom Navigation */}
//         <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
//           <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
//             {navigationItems.map((item) => (
//               <button
//                 key={item.label}
//                 onClick={() => navigate(item.href, { replace: true })} // replace 옵션으로 뒤로가기 방지
//                 className="flex flex-col items-center w-[82px] h-[75px] bg-transparent border-none"
//               >
//                 <item.icon
//                   className={`w-14 h-14 ${
//                     item.active ? "text-black" : "text-[#b3b3b3]"
//                   }`}
//                 />
//                 <span
//                   className={`font-['Koulen'] text-xl ${
//                     item.active ? "text-black" : "text-[#b3b3b3]"
//                   }`}
//                 >
//                   {item.label}
//                 </span>
//               </button>
//             ))}
//           </div>
//         </nav>
//       </div>
//     </div>
//   );
// };

import React, { useState, useRef } from "react";
import { toPng } from "html-to-image";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

export const Timer = (): JSX.Element => {
  const [text, setText] = useState("흠냐냐"); // 기본 텍스트
  const ref = useRef<HTMLDivElement>(null);

  const handleDownload = () => {
    if (ref.current) {
      toPng(ref.current)
        .then((dataUrl) => {
          const link = document.createElement("a");
          link.href = dataUrl;
          link.download = "generated-image.png";
          link.click();
        })
        .catch((err) => console.error("Error generating image:", err));
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="텍스트 입력"
        className="mb-4 p-2 border rounded"
      />
      <div ref={ref} className="relative w-80 h-48 bg-white rounded-lg shadow-lg flex flex-col items-center justify-center">
        <div className="absolute top-0 w-full bg-black text-white text-center py-2 rounded-t-lg">
          무엇이든 물어보세요!
        </div>
        <div className="mt-10 text-lg font-bold">{text}</div>
        <div className="absolute top-2 right-2 w-8 h-8 bg-gray-200 rounded-full"></div>
      </div>
      <Button onClick={handleDownload} className="mt-4">이미지 저장</Button>
    </div>
  );
};
