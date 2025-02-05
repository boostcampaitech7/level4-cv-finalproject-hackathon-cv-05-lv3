import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import NaviBar from "../../components/ui/navigationbar";

const Page1: React.FC = () => {
    const [titles, setTitles] = useState(["Title 1", "Title 2"]);
    const [search, setSearch] = useState("");
    const carouselRef = useRef<HTMLDivElement>(null);
    let interval = useRef<NodeJS.Timeout | null>(null);
    let isDragging = useRef(false);
    let startX = useRef(0);
    let scrollLeft = useRef(0);

    const images = [
      "../../image_data/test1.png",
      "../../image_data/test2.png",
      "../../image_data/test3.jpg",
      "../../image_data/test4.jpg",
      "../../image_data/test5.png",
    ];

    useEffect(() => {
        startAutoScroll();
        return () => {
            if (interval.current) clearInterval(interval.current);
        };
    }, []);

    const startAutoScroll = () => {
        if (!carouselRef.current) return;
        interval.current = setInterval(() => {
            if (!isDragging.current && carouselRef.current) {
                carouselRef.current.scrollLeft += 1;
                if (carouselRef.current.scrollLeft >= carouselRef.current.scrollWidth / 2) {
                    carouselRef.current.style.scrollBehavior = "auto";
                    carouselRef.current.scrollLeft = 0;
                    carouselRef.current.style.scrollBehavior = "smooth";
                }
            }
        }, 20);
    };

    const handleMouseDown = (e: React.MouseEvent) => {
        isDragging.current = true;
        startX.current = e.pageX - (carouselRef.current?.offsetLeft || 0);
        scrollLeft.current = carouselRef.current?.scrollLeft || 0;
    };

    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isDragging.current || !carouselRef.current) return;
        const x = e.pageX - carouselRef.current.offsetLeft;
        const walk = (x - startX.current) * 2;
        carouselRef.current.scrollLeft = scrollLeft.current - walk;
    };

    const handleMouseUp = () => {
        isDragging.current = false;
    };

    return (
        <div className="p-4">
            {/* 이미지 슬라이드 */}
            <div
                ref={carouselRef}
                className="flex overflow-x-scroll scroll-smooth space-x-4 p-4 cursor-grab"
                style={{ scrollbarWidth: "none" }}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
            >
                {[...images, ...images].map((src, index) => (
                    <motion.div key={index} className="w-[100px] h-[133px] bg-gray-400 flex-shrink-0" whileTap={{ scale: 0.95 }}>
                        <img src={src} alt={`img-${index}`} className="w-full h-full object-cover rounded-lg cursor-pointer" />
                    </motion.div>
                ))}
            </div>

            {/* 검색창 */}
            <Input
                type="text"
                placeholder="Search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="border p-2 w-full"
            />

            {/* 동적 Title 리스트 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-2">
                {titles.map((title, index) => (
                    <Card key={index} className="flex items-center p-2 bg-gray-200 cursor-pointer">
                        <div className="w-8 h-8 bg-gray-300 mr-2"></div>
                        {title}
                    </Card>
                ))}
            </div>
        </div>
    );
};

const Page2: React.FC = () => {
    const [search, setSearch] = useState("");
    const [images, setImages] = useState(Array(20).fill("../../image_data/test3.jpg")); // 더미 이미지 (3:4 비율)

    const handleImageClick = (index: number) => {
        alert(`이미지 ${index + 1} 클릭됨!`); // 여기에 원하는 동작 추가
    };

    return (
        <div className="flex flex-col w-full h-full">
            {/* 검색창 & 전체 검색 문구 */}
            <div className="p-4">
                <h2 className="text-lg font-bold text-left mb-2">전체 검색</h2>
                <Input
                    type="text"
                    placeholder="Search"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="border p-2 w-full"
                />
            </div>

            {/* 이미지 리스트 (스크롤 가능) */}
            <div className="flex-1 overflow-y-auto px-4">
                <div className="grid grid-cols-3 gap-4">
                    {images.map((src, index) => (
                        <div
                            key={index}
                            className="w-full aspect-[3/4] bg-gray-300 flex items-center justify-center text-xs cursor-pointer rounded-lg"
                            onClick={() => handleImageClick(index)}
                        >
                            <img src={src} alt={`img-${index}`} className="w-full h-full object-cover rounded-lg" />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};



export const Community: React.FC = () => {
    const [page, setPage] = useState(1);

    return (
        <div className="bg-white flex flex-row justify-center w-full">
            <div className="bg-white w-[393px] h-[852px] relative">

                {/* 페이지 전환 버튼 */}
                <div className="flex justify-center p-2 bg-gray-300">
                    <Button onClick={() => setPage(1)} className={page === 1 ? "font-bold" : "text-gray-400"}>
                        1페이지
                    </Button>
                    <Button onClick={() => setPage(2)} className={page === 2 ? "font-bold" : "text-gray-400"}>
                        2페이지
                    </Button>
                </div>

                {/* 페이지 렌더링 */}
                {page === 1 ? <Page1 /> : <Page2 />}

                <NaviBar activeLabel="Community" />
            </div>
        </div>
    );
};
