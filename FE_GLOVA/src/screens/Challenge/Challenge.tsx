import { useEffect, useState } from "react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import { Badge, GetBadges, GetAudioFile } from "../../api/api"; // ✅ Badge 인터페이스 사용
import { dummyBadges } from "../../dummy";

import NaviBar from "../../components/ui/navigationbar";

// Base64 이미지를 img URL로 변환하는 함수
export const base64ToImageUrl = (base64: string): string => {
  try {
    const mimeTypeMatch = base64.match(/^data:(image\/\w+);base64,/);
    if (!mimeTypeMatch) {
      throw new Error("Invalid base64 format");
    }

    const mimeType = mimeTypeMatch[1]; // MIME 타입 추출
    const base64Data = base64.replace(/^data:image\/\w+;base64,/, ""); // Base64 데이터만 추출
    const byteCharacters = atob(base64Data); // Base64 디코딩
    const byteNumbers = new Uint8Array(byteCharacters.length);

    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }

    const blob = new Blob([byteNumbers], { type: mimeType }); // Blob 생성
    return URL.createObjectURL(blob); // Blob URL 반환
  } catch (error) {
    console.error("Error decoding base64 image:", error);
    return ""; // 에러 발생 시 빈 문자열 반환
  }
};


export const Challenge = (): JSX.Element => {
  const navigate = useNavigate();
  const [badges, setBadges] = useState<Badge[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBadge, setSelectedBadge] = useState<Badge | null>(null);
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    setBadges(dummyBadges);
  }, []);

  // {/*서버 통신 버전*/}
  // useEffect(() => {
  //   const fetchData = async () => {
  //     const data = await GetBadges(); // ✅ API 호출
  //     setBadges(data);
  //   };
  //   fetchData();
  // }, []);

  // ✅ 모달 열기 함수
  const openModal = (badge: Badge) => {
    setSelectedBadge(badge);
    setIsModalOpen(true);
  };

  // ✅ 모달 닫기 함수
  const closeModal = () => {
    setSelectedBadge(null);
    setIsModalOpen(false);
  };

  const openAudio = async (badge: Badge): Promise<void> => {
    setSelectedBadge(badge);
    try{
      const mp3URL = await GetAudioFile();
      if (audioElement) {
        audioElement.pause();
      }
      const newAudioElement = new Audio(mp3URL);
      setAudioElement(newAudioElement);
      newAudioElement.play();
    } catch (error) {
      console.error("Error fetching audio:", error);
    }
  };

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full h-screen overflow-y-auto">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-[40px] font-SBAggroB text-black text-center ">『 독서의 전당 』</h1>
        </div>

        <hr className="border-t border-2 border-gray-300 my-8, mx-4" />

        {/* ✅ Badge List */}
        <div className="grid grid-cols-4 gap-3 px-5 mt-5">
          {badges.map((badge, index) => (
            <Card key={index} className="border-none shadow-none justify-center items-center flex">
              <CardContent className="p-2.5 flex flex-col items-center shadow-none border-none">
                <motion.img
                  className="w-[100px] h-[100px] object-cover cursor-pointer"
                  alt="badge image"
                  // src={base64ToImageUrl(badge.badgeImage)}
                  src = {badge.badgeImage}
                  onClick={() => {openModal(badge), openAudio(badge)}} // ✅ 클릭 시 모달 오픈
                  // onClick = {() => openAudio(badge)}
                  whileTap={{ scale: 0.85 }} // 클릭 시 0.85배 크기로 줄어듦
                  transition={{ type: "spring", stiffness: 400, damping: 10 }} // 부드러운 반응
                />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* ✅ Modal (이미지 클릭 시 표시) */}
        {isModalOpen && selectedBadge && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-5 rounded-lg w-[300px] shadow-lg text-center">
              <h2 className="text-lg font-bold">{selectedBadge.bookTitle}</h2>
              <img
                className="w-[150px] h-[150px] object-cover mx-auto mt-3"
                // src={base64ToImageUrl(selectedBadge.badgeImage)} // ✅ Base64 이미지 URL로 변환
                src = {selectedBadge.badgeImage}
                alt="badge image"
              />
              <p className="text-sm text-gray-500 mt-2">
                획득 날짜: {new Date(selectedBadge.createdAt).toLocaleDateString()}
              </p>
              <button
                className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg active:scale-95 transition-transform duration-150"
                onClick={closeModal} // ✅ 닫기 버튼
              >
                닫기
              </button>
            </div>
          </div>
        )}

        <NaviBar activeLabel="Challenge" />
      </div>
    </div>
  );
};
