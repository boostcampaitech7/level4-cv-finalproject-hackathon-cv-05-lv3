import {
  BookOpen,
  HomeIcon,
  TimerIcon,
  TrophyIcon,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
  { icon: BookOpen, label: "BOOKS", href: "/Library", active: false },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: true },
];

export const Timer = (): JSX.Element => {
  const navigate = useNavigate();

  const [hours, setHours] = useState(0);
  const [minutes, setMinutes] = useState(25);
  const [seconds, setSeconds] = useState(0);
  const [timeLeft, setTimeLeft] = useState((hours * 3600) + (minutes * 60) + seconds);
  const [isRunning, setIsRunning] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const radius = 90;
  const circumference = 2 * Math.PI * radius;

  useEffect(() => {
    if (!isRunning) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setShowModal(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isRunning]);

  useEffect(() => {
    setTimeLeft((hours * 3600) + (minutes * 60) + seconds);
  }, [hours, minutes, seconds]);

  const handleTimeChange = (setter: React.Dispatch<React.SetStateAction<number>>, value: string) => {
    let newValue = parseInt(value, 10);
    if (isNaN(newValue) || newValue < 0) newValue = 0;
    if (setter === setHours && newValue > 12) newValue = 12;
    if (setter === setMinutes && newValue > 59) newValue = 59;
    if (setter === setSeconds && newValue > 59) newValue = 59;
    setter(newValue);
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTimeLeft((hours * 3600) + (minutes * 60) + seconds);
  };

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${String(hrs).padStart(2, "0")}:${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  };

  const progress = timeLeft / ((hours * 3600) + (minutes * 60) + seconds);
  const gaugeColor = "#FF5733";

  return (
    <div className="bg-white flex flex-col items-center w-full min-h-screen p-6">
      <div className="w-full max-w-[393px] h-[852px] flex flex-col items-center justify-center">
        <div className="flex gap-2 mb-4">
          <input type="number" value={hours} onChange={(e) => handleTimeChange(setHours, e.target.value)} disabled={isRunning} className="border border-gray-300 rounded-md p-2 text-center w-16" />
          <span>:</span>
          <input type="number" value={minutes} onChange={(e) => handleTimeChange(setMinutes, e.target.value)} disabled={isRunning} className="border border-gray-300 rounded-md p-2 text-center w-16" />
          <span>:</span>
          <input type="number" value={seconds} onChange={(e) => handleTimeChange(setSeconds, e.target.value)} disabled={isRunning} className="border border-gray-300 rounded-md p-2 text-center w-16" />
        </div>

        <div className="relative w-[200px] h-[200px]">
          <svg width="200" height="200" viewBox="0 0 200 200">
            <circle cx="100" cy="100" r={radius} stroke="#E0E0E0" strokeWidth="10" fill="none" />
            <circle
              cx="100"
              cy="100"
              r={radius}
              stroke={gaugeColor}
              strokeWidth="10"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={circumference * (1 - progress)}
              strokeLinecap="round"
              transform="rotate(-90 100 100) scale(-1,1)"
            />
          </svg>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-3xl font-bold">
            {formatTime(timeLeft)}
          </div>
        </div>

        <div className="flex gap-4 mt-6">
          <button onClick={() => setIsRunning(!isRunning)} className="px-6 py-3 bg-blue-500 text-white rounded-lg text-lg">
            {isRunning ? "일시정지" : "시작"}
          </button>
          <button onClick={resetTimer} className="px-6 py-3 bg-gray-400 text-white rounded-lg text-lg">초기화</button>
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
  );
};