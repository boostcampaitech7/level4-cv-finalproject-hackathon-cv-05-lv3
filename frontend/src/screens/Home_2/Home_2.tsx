import React from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";

import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import NaviBar from "../../components/ui/navigationbar";
  
export const Home2 = (): JSX.Element => {
  const location = useLocation();
  const { age, gender} = location.state || {};

  const navigate = useNavigate();

  const [question, setQuestion] = React.useState<string>("");

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <div className="absolute top-[180px] left-[104px] font-bold text-black text-base text-center whitespace-nowrap [font-family:'Inter',Helvetica]">
          클로바에게 질문해보세요!
        </div>

        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
        </div>

        <div className="flex w-[285px] items-center gap-[9px] absolute top-[549px] left-[54px]">
          <Button className="flex w-[135px] items-center justify-center bg-[#d9d9d9] rounded-[20px_3px_3px_20px] text-black hover:bg-[#c4c4c4]"
            onClick={() => navigate("/Home_1", { replace: true })}
          >
            이전
          </Button>
          <Button className="flex w-[141px] items-center justify-center bg-[#d9d9d9] rounded-[3px_20px_20px_3px] text-black hover:bg-[#c4c4c4]"
            onClick={() => {
              navigate("/Home_3", { replace: true, state: { age, gender, question } });
            }}
          >
            제출
          </Button>
        </div>

        <Card className="flex flex-col w-[285px] absolute top-[220px] left-[54px] border-none">
          <CardContent className="flex h-[99px] items-center justify-center p-2.5 bg-neutral-800 rounded-[15px_15px_0px_0px] border-t-2 border-r-2 border-l-2 border-black">
            <div className="font-bold text-white text-[25px] text-center [font-family:'Inter',Helvetica]">
              무엇이든 물어보세요!
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

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
