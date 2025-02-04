import { useEffect, useState } from "react";
import { BookOpen, HomeIcon, TimerIcon, TrophyIcon } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { Vector } from "../../icons/Vector";
import { useNavigate } from "react-router-dom";
import { Badge, Server2Badge, Server2AudioFile } from "../../api/api"; // ✅ Badge 인터페이스 사용

const navigationItems = [
  { icon: TrophyIcon, label: "CHALLENGE", href: "/Challenge", active: true },
  { icon: HomeIcon, label: "HOME", href: "/Home", active: false },
  { icon: BookOpen, label: "BOOKS", href: "/Library", active: false },
  { icon: TimerIcon, label: "TIMER", href: "/Timer", active: false },
];


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
    const fetchData = async () => {
      const data = await Server2Badge(); // ✅ API 호출
      setBadges(data);
    };
    fetchData();
  }, []);

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
      const mp3URL = await Server2AudioFile();
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
    <div className="bg-white flex flex-row justify-center w-full h-screen overflow-y-auto">
      <div className="bg-white w-[393px] h-[852px] relative">
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-4xl font-normal text-black text-center">독서의 전당</h1>
        </div>

        <Separator className="mx-5 mt-8" />

        {/* ✅ Badge List */}
        <div className="grid grid-cols-4 gap-3 px-5 mt-5">
          {badges.map((badge, index) => (
            <Card key={index} className="border-none">
              <CardContent className="p-2.5 flex flex-col items-center">
                <img
                  className="w-[100px] h-[100px] object-cover cursor-pointer"
                  alt="badge image"
                  src={base64ToImageUrl(badge.badgeImage)}
                  // onClick={() => openModal(badge)} // ✅ 클릭 시 모달 오픈
                  onClick = {() => openAudio(badge)}
                />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* ✅ Modal (이미지 클릭 시 표시) */}
        {/* {isModalOpen && selectedBadge && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-5 rounded-lg w-[300px] shadow-lg text-center">
              <h2 className="text-lg font-bold">{selectedBadge.bookTitle}</h2>
              <img
                className="w-[150px] h-[150px] object-cover mx-auto mt-3"
                src={base64ToImageUrl(selectedBadge.badgeImage)} // ✅ Base64 이미지 URL로 변환
                alt="badge image"
              />
              <p className="text-sm text-gray-500 mt-2">
                획득 날짜: {new Date(selectedBadge.createdAt).toLocaleDateString()}
              </p>
              <button
                className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg"
                onClick={closeModal} // ✅ 닫기 버튼
              >
                닫기
              </button>
            </div>
          </div>
        )} */}

        {/* ✅ Bottom Navigation */}
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
