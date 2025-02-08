import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";

import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader } from "../../components/ui/card";
import NaviBar from "../../components/ui/navigationbar";

export const Home1 = (): JSX.Element => {
  const navigate = useNavigate();

  const [gender, setGender] = useState<string>("남자");
  const [age, setAge] = useState<string>(""); // 나이 입력값

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        {/* 진행 바 */}
        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <div className="relative w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
        </div>

        {/* 제목 */}
        <h1 className="absolute top-[180px] left-1/2 transform -translate-x-1/2 font-bold text-black text-base text-center">
          나이와 성별을 알려주세요!
        </h1>

        {/* 메인 카드 */}
        <div className="absolute top-[220px] left-1/2 transform -translate-x-1/2 w-[285px]">
          <Card className="shadow-md rounded-[15px] overflow-hidden border-2 border-black">
            {/* 카드 헤더 */}
            <CardHeader className="bg-black text-center text-white bg-neutral-800">
              <h2 className="text-[28px] font-bold">저는...</h2>
            </CardHeader>
            {/* 카드 내용 */}
            <CardContent className="bg-white px-6 py-8">
              {/* 나이 입력 */}
              <div className="flex items-center justify-center gap-2 mb-6">
                <input
                  type="number"
                  className="text-[45px] font-bold text-center border-b-2 border-black w-[100px] focus:outline-none [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                  placeholder="나이"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                />
                <span className="text-3xl font-bold">살</span>
              </div>
              {/* 성별 선택 */}
              <div className="flex justify-center gap-4 mb-6">
                <Button
                  variant={gender === "남자" ? "default" : "outline"}
                  className={`w-[80px] h-[40px] rounded-md ${
                    gender === "남자" ? "bg-black text-white" : "bg-[#e1e1e1]"
                  }`}
                  onClick={() => setGender("남자")}
                >
                  남자
                </Button>
                <Button
                  variant={gender === "여자" ? "default" : "outline"}
                  className={`w-[80px] h-[40px] rounded-md ${
                    gender === "여자" ? "bg-black text-white" : "bg-[#e1e1e1]"
                  }`}
                  onClick={() => setGender("여자")}
                >
                  여자
                </Button>
              </div>
              {/* 텍스트 */}
              <div className="text-3xl font-bold text-center">입니다.</div>
            </CardContent>
          </Card>

          {/* 다음 버튼 */}
          <div className="flex justify-end mt-4">
            <Button
              variant="secondary"
              className="w-[141px] rounded-[20px] bg-[#d9d9d9] text-lg active:scale-95 transition-transform duration-150 hover:bg-[#c4c4c4]"
              onClick={() => navigate("/Home_2", { replace: true, state: {age, gender}})}
            >
              다음
            </Button>
          </div>
        </div>

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
