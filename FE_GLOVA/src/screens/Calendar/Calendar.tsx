import { useState } from "react";
import { Calendar } from "react-calendar";
import { useNavigate } from "react-router-dom";
import { Vector } from "../../icons/Vector";
import { Server2Calendar, Calendar_Data } from "../../api/api"; // API 함수 import
import "react-calendar/dist/Calendar.css";
import styles from "./styles/Calendar.module.css";
import classNames from "classnames";
import {
  CalendarIcon,
  HomeIcon,
  TimerIcon,
  TrophyIcon,
} from "lucide-react";

const navigationItems = [
  { icon: TrophyIcon, label: "Challenge", href: "/Challenge", active: false },
  { icon: HomeIcon, label: "Home", href: "/Home", active: false },
  { icon: CalendarIcon, label: "Calendar", href: "/Calendar", active: true },
  { icon: TimerIcon, label: "Timer", href: "/Timer", active: false },
];

export const Calendar_main = (): JSX.Element => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [events, setEvents] = useState<Calendar_Data[]>([]);
  const [overlay, setOverlay] = useState<{ isVisible: boolean; event: Calendar_Data | null }>({
    isVisible: false,
    event: null,
  });
  const navigate = useNavigate();

  const handleDateChange = async (date: Date) => {
    setSelectedDate(date);

    const formattedDate = date.toISOString().split("T")[0]; // YYYY-MM-DD 형식
    try {
      const fetchedEvents = await Server2Calendar(formattedDate);
      setEvents(fetchedEvents);
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  const handleEventClick = (event: Calendar_Data) => {
    setOverlay({ isVisible: true, event });
  };

  const closeOverlay = () => {
    setOverlay({ isVisible: false, event: null });
  };

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-full max-w-[393px] h-[852px] relative">
        {/* 상단 아이콘 */}
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        {/* 캘린더 */}
        <div className={classNames("react-calendar")}>
          <Calendar onChange={handleDateChange} value={selectedDate} />
        </div>

        {/* 선택된 날짜 표시 */}
        <p>
          {`${selectedDate.getFullYear()}년 ${
            selectedDate.getMonth() + 1
          }월 ${selectedDate.getDate()}일`}
        </p>

        {/* 서버에서 받은 이벤트 목록 */}
        <div className="event-list">
          {events.length > 0 ? (
            events.map((event, index) => (
              <div
                key={index}
                className={styles.eventCard}
                onClick={() => handleEventClick(event)}
              >
                <img src={event.bookimage} alt={event.bookTitle} />
                <h3>{event.bookTitle}</h3>
                <p>{event.time}</p>
              </div>
            ))
          ) : (
            <p>해당 날짜에 대한 이벤트가 없습니다.</p>
          )}
        </div>

        {/* 오버레이 */}
        {overlay.isVisible && overlay.event && (
          <div className={styles.overlay} onClick={closeOverlay}>
            <div className={styles.overlayContent}>
              <img
                src={overlay.event.bookimage}
                alt={overlay.event.bookTitle}
                className={styles.overlayImage}
              />
              <h3>{overlay.event.bookTitle}</h3>
              <p>시간: {overlay.event.time}</p>
              <p>질문: {overlay.event.question}</p>
            </div>
          </div>
        )}

        {/* 네비게이션 바 */}
        <nav className="fixed bottom-0 left-0 right-0 max-w-[393px] mx-auto">
          <div className="flex items-center justify-center gap-[15px] px-[5px] py-0 h-[100px] bg-white shadow-[0px_-2px_10px_#00000040]">
            {navigationItems.map((item) => (
              <button
                key={item.label}
                onClick={() => navigate(item.href, { replace: true })}
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
