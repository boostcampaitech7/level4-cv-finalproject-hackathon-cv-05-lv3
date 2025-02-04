import {
    BookOpen,
    HomeIcon,
    TimerIcon,
    TrophyIcon,
  } from "lucide-react";
  
  import React, { useState, useEffect } from "react";
  import { AnimatePresence, motion } from "framer-motion";
  import { Vector } from "../../icons/Vector";  
  import { Button } from "../../components/ui/button";
  import { Card, CardContent } from "../../components/ui/card";
  import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
  import { Calendar2Server } from "../../api/api";
  import { useSwipeable } from "react-swipeable";
  
  const navigationItems = [
    { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: false },
    { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
    { icon: BookOpen, label: "BOOKS", href: "/Library", active: false },
    { icon: TimerIcon, label: "TIMER", href: "/Timer", active: true },
  ];
  

const images = [
  "../../image_data/test1.png",
  "../../image_data/test2.png",
  "../../image_data/test3.jpg",
  "../../image_data/test4.jpg",
  "../../image_data/test5.png",
];

interface Post {
  bookImage: string;
  userName: string;
  userQuestion: string;
  chatCount: number;
}

export const Community: React.FC = () => {
    const navigate = useNavigate(); // useNavigate로 네비게이션 설정
    const [index, setIndex] = useState(0);
    const [posts, setPosts] = useState<Post[]>([
        {
        bookImage: "../../image_data/test1.png",
        userName: "User 1",
        userQuestion: "This is a sample question 1?",
        chatCount: 5,
        },
        {
        bookImage: "../../image_data/test2.png",
        userName: "User 2",
        userQuestion: "This is a sample question 2?",
        chatCount: 8,
        },
        {
        bookImage: "../../image_data/test3.jpg",
        userName: "User 3",
        userQuestion: "This is a sample question 3?",
        chatCount: 3,
        },
        {
            bookImage: "../../image_data/test4.jpg",
            userName: "User 4",
            userQuestion: "This is a sample question 4?",
            chatCount: 999,
        },
        {
        bookImage: "../../image_data/test5.png",
        userName: "User 5",
        userQuestion: "This is a sample question 5?",
        chatCount: 320808203820,
        },

    ]);

    const nextIndex = (index + 1) % images.length;
    const prevIndex = (index - 1 + images.length) % images.length;
    // 이미지 슬라이드 핸들러
    const handlers = useSwipeable({
        onSwipedLeft: () => setIndex(nextIndex),
        onSwipedRight: () => setIndex(prevIndex),
        // preventDefaultTouchmoveEvent: true,
        trackMouse: true,
    });

    // 데이터 로딩
    useEffect(() => {
        fetch("http://localhost:8000")
        .then((res) => res.json())
        .then((data) => setPosts(data))
        .catch((err) => console.error("Failed to fetch data:", err));
    }, []);

    return (
        <div className="bg-white flex flex-row justify-center w-full">
        <div className="bg-white w-[393px] h-[852px] relative">
            <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
            {/* 이미지 슬라이더 */}
            <div {...handlers} className="relative flex justify-center items-center h-[200px] mt-[60px] overflow-hidden">
            {/* 이전 이미지 (클릭 가능) */}
            <motion.img
            key={prevIndex}
            src={images[prevIndex]}
            alt="previous"
            className="absolute w-[100px] h-[140px] rounded-md left-[15%] opacity-60 cursor-pointer"
            initial={{ scale: 0.8, opacity: 0.5 }}
            animate={{ scale: 1, opacity: 0.6 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
            onClick={() => setIndex(prevIndex)}  // 이전 이미지 클릭 시 변경
            />

            {/* 다음 이미지 (클릭 가능) */}
            <motion.img
            key={nextIndex}
            src={images[nextIndex]}
            alt="next"
            className="absolute w-[100px] h-[140px] rounded-md right-[15%] opacity-60 cursor-pointer"
            initial={{ scale: 0.8, opacity: 0.5 }}
            animate={{ scale: 1, opacity: 0.6 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
            onClick={() => setIndex(nextIndex)}  // 다음 이미지 클릭 시 변경
            />

            {/* 중앙 이미지 */}
            <AnimatePresence mode="wait">
            <motion.img
                key={index}
                src={images[index]}
                alt="slider"
                className="absolute w-[140px] h-[200px] rounded-md"
                initial={{ opacity: 0, scale: 0.8, rotateY: 90 }}
                animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                exit={{ opacity: 0, scale: 0.8, rotateY: -90 }}
                transition={{ duration: 0.15, ease: "easeInOut" }}
            />
            </AnimatePresence>
            </div>

            <hr className="border-gray-300 my-2" />

            {/* 리스트 */}
            <div className="flex-1 overflow-y-auto px-4">
                {posts.map((post, i) => (
                <button key={i} className="w-full flex items-center bg-white p-4 rounded-lg shadow mb-3">
                    <img src={post.bookImage} alt="book" className="w-[60px] h-[60px] bg-gray-200 rounded-md mr-4" />
                    <div className="flex-1 flex flex-col items-start text-left">
                    <p className="font-semibold text-sm text-left">{post.userName}</p>
                    <p className="text-xs text-gray-600">{post.userQuestion}</p>
                    </div>
                    <div className="flex items-center text-gray-500 text-sm">
                    <span className="mr-1">💬</span>
                    {post.chatCount}
                    </div>
                </button>
                ))}
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

export default Community;
