
import { Button } from "../../components/ui/button";
import { useState } from "react";
import { HelpCircle } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import { SaveRecommand } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";

import { dummy_Home4 } from "../../dummy";

export const Home4 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  
  {/*서버 통신 데이터*/}
  const data = location.state || {};

  {/*더미 데이터*/}
  // const data = dummy_Home4;

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
        {/* 상단 아이콘 */}
        <button
          className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
          onClick={() => setIsInfoModalOpen(true)}
        >
          <HelpCircle size={24} />
        </button>

        {/* Main Content */}
        <div className="flex flex-col items-center px-4">
          <h2 className="mt-[147px] text-xl font-bold text-center text-gray-800 font-Freesentation">
            이런 책은 어떠신가요?
          </h2>

          <Card className="mt-4 border-none">
            <CardContent className="flex flex-col items-center p-0">
              <img
                className="w-[137px] h-[183px] object-cover"
                alt="Book cover"
                // src="./image_data/rectangle-15@2x.png"
                src = {data.bookimage}
              />
            </CardContent>
          </Card>

          <div className="w-[299px] mt-4">
            <h1 className="text-4xl font-bold text-center text-black font-Freesentation">{data.bookTitle}</h1>
          </div>

          <div
            className="w-[325px] mt-4 bg-[#e1e1e1] rounded-md p-4 text-base font-normal overflow-auto max-h-[200px]"
          >
            <p>
              {data.description}
            </p>
          </div>

          <div className="flex w-[324px] gap-2 mt-4">
            <Button
              variant="secondary"
              className="flex-1 rounded-[20px_3px_3px_20px] bg-[#d9d9d9] active:scale-95 transition-transform duration-150 hover:bg-[#c4c4c4]"
              onClick={() => navigate("/Home", { replace: true })}
            >
              처음으로 돌아가기
            </Button>
            <Button
              variant="secondary"
              className="flex-1 rounded-[3px_20px_20px_3px] bg-[#d9d9d9] active:scale-95 transition-transform duration-150 hover:bg-[#c4c4c4]"
              onClick={() => {
                SaveRecommand(data.question, data.bookimage, data.bookTitle);
                navigate("/Library", { replace: true })
                }
              }
            >
              추천도서 저장하기
            </Button>
          </div>
        </div>

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img
                src="../../image_data/Guide/Home4.png" 
                alt="도움말 이미지"
                className="w-full h-auto rounded-md"
              />
              <button
                className="mt-4 px-4 py-2 bg-gray-500 text-white rounded-lg"
                onClick={() => setIsInfoModalOpen(false)}
              >
                닫기
              </button>
            </div>
          </div>
        )}

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
