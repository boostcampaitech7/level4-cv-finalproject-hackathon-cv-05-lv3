import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { NaverOAuth } from "../../api/naverlogin"

export const Login = (): JSX.Element => {
  const navigate = useNavigate();

  function handleLoginSuccess() {
    navigate("/Home", { replace: true });
  }

  return (
    <main className="flex justify-center items-center min-h-screen bg-white">
      <div className="w-[393px] flex flex-col items-center px-4">
        <img
          className="w-[250px] h-[148px] mb-4 object-cover"
          alt="Logo"
          src="./image_data/rectangle-4@2x.png"
        />

        <p className="text-xl text-center text-black font-normal mb-8">
          오늘은 또 무슨일이 생길까 피카츄 라이츄 파이리 꼬부기 버터풀 라이츄 디지몬 친구들~
        </p>

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <NaverOAuth onLoginSuccess={handleLoginSuccess} />
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
