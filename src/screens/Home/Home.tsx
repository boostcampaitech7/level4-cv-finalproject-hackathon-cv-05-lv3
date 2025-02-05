import React from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import { Avatar, AvatarImage } from "../../components/ui/avatar";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Vector } from "../../icons/Vector";
import { Separator } from "../../components/ui/separator";
import NaviBar from "../../components/ui/navigationbar";

export const Home = (): JSX.Element => {
  const navigate = useNavigate(); // useNavigate로 네비게이션 설정

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <Vector className="!absolute !w-9 !h-6 !top-[30px] !left-[332px]" />

        <div className="bg-white absolute w-[285px] top-[294px] left-1/2 -translate-x-1/2">
          <Card className="relative border shadow-[0px_2px_10px_#00000040] rounded-[15px] border-2 border-black">
            <CardContent className="p-5">
              <Avatar className="w-[61px] h-[61px] absolute -top-8 left-1/2 -translate-x-1/2">
                <AvatarImage
                  src="./image_data/ellipse-4@2x.png"
                  alt="Profile"
                />
              </Avatar>

              <div className="mt-8 text-center">
                <p className="font-bold text-xl mb-4">
                  클로바에게 <br /> 책을 추천받아 보세요!
                </p>
                <Button
                  variant="secondary"
                  className="w-full bg-[#e1e1e1] rounded-[15px] font-bold text-lg active:scale-95 transition-transform duration-150 hover:bg-[#d1d1d1]"
                  onClick={() => navigate("/Home_1", { replace: true })}
                >
                  시작하기!
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
