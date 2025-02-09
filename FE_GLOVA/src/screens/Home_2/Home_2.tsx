import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import { HelpCircle } from "lucide-react";

import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import NaviBar from "../../components/ui/navigationbar";
  
export const Home2 = (): JSX.Element => {
  const location = useLocation();
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  
  const { age, gender} = location.state || {};

  const navigate = useNavigate();

  const [question, setQuestion] = React.useState<string>("");

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

        <div className="absolute top-[180px] left-[55px] font-bold text-black text-base text-center whitespace-nowrap [font-family:'Inter',Helvetica]">
          답변에 어울리는 책을 추천해 줄 거에요!
        </div>

        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
        </div>

        <div className="flex w-[285px] items-center gap-[9px] absolute top-[549px] left-[54px]">
          <Button className="flex w-[135px] items-center justify-center bg-[#d9d9d9] rounded-[20px_3px_3px_20px] text-black active:scale-95 transition-transform duration-150 hover:bg-[#c4c4c4]"
            onClick={() => navigate("/Home_1", { replace: true })}
          >
            이전
          </Button>
          
          <Button
            className={`flex w-[141px] items-center justify-center rounded-[3px_20px_20px_3px] text-black active:scale-95 transition-transform duration-150 ${
              question ? "bg-[#d9d9d9] hover:bg-[#c4c4c4]" : "bg-gray-300 opacity-50 cursor-not-allowed"
            }`}
            onClick={() => {
              if (question) {
                navigate("/Home_3", { replace: true, state: { age, gender, question } });
              }
            }}
            disabled={!question} // 입력값이 없으면 버튼 비활성화
          >
            제출
          </Button>
        </div>

        <Card className="flex flex-col w-[285px] absolute top-[220px] left-[54px] border-none">
          <CardContent className="flex h-[99px] items-center justify-center p-2.5 bg-neutral-800 rounded-[15px_15px_0px_0px] border-t-2 border-r-2 border-l-2 border-black">
            <div className="font-bold text-white text-[24px] text-center [font-family:'Inter',Helvetica]">
              무엇이든 얘기해보세요!
            </div>
          </CardContent>
          <CardContent className="flex flex-col h-[220px] gap-2.5 p-[11px] bg-white rounded-[0px_0px_15px_15px] border-r-2 border-b-2 border-l-2 border-black">
            <div className="relative w-full h-[197px] bg-[#e1e1e1] rounded-[15px]">
              <textarea
                className="absolute w-[240px] top-[11px] left-[9px] font-bold text-black text-[15px] bg-transparent border-none focus:outline-none resize-none overflow-auto h-[177px] max-h-[177px]"
                placeholder="TEXT INPUT"
                value={question} // 입력값을 상태로 연결
                onChange={(e) => setQuestion(e.target.value)} // 상태 업데이트
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement;
                  target.style.height = "auto"; // 높이를 초기화하여 동적 계산
                  target.style.height = `${Math.min(target.scrollHeight, 177)}px`; // 최대 높이로 제한
                }}
              />
            </div>
          </CardContent>
        </Card>

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img
                src="../../image_data/Guide/Home.png" 
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
