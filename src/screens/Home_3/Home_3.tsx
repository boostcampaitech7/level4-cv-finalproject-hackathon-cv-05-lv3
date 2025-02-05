
import { Calendar } from "../../components/ui/calendar";
import { Card, CardContent } from "../../components/ui/card";
import { Vector } from "../../icons/Vector";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import {Question2Server} from "../../api/api";
import { useCallback, useEffect } from "react";
import NaviBar from "../../components/ui/navigationbar";

export const Home3 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();

  const { age, gender, question } = location.state || {};

  const fetchAndNavigate = useCallback(async () => {
    try {
      console.log(age, gender, question);
      const data = await Question2Server(age, gender, question);
      navigate("/Home_4", { state: { ...data } });
    } catch (error) {
      console.error("Error while fetching data:", error);
    }
  }, [age, gender, question, navigate]); // ✅ 필요한 의존성만 설정
  
  useEffect(() => {
    fetchAndNavigate();
  }, [fetchAndNavigate]); // ✅ useCallback을 통해 fetchAndNavigate가 변경되지 않도록 함

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <div className="absolute top-[180px] left-8 font-bold text-black text-base text-center tracking-[0] leading-[normal] whitespace-nowrap">
          클로바가 무슨 책을 추천할지 고민 중입니다...
        </div>

        <div className="inline-flex top-[125px] left-[165px] items-center gap-[15px] absolute">
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-2.5 h-2.5 bg-[#b38f00] rounded-[5px]" />
          <div className="relative w-[13px] h-[13px] bg-[#ffcc00] rounded-[6.5px]" />
        </div>

        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        <Card className="absolute w-[351px] top-[220px] left-[21px] border-none">
          <CardContent className="p-0">
            <img
              className="w-full h-[486px]"
              alt="Mini game display"
              src="./image_data/group-3@2x.png"
            />
          </CardContent>
        </Card>

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
