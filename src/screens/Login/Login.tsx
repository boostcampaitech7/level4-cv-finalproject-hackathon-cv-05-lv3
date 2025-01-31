import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Input } from "../../components/ui/input";

export const Login = (): JSX.Element => {
  const [ID, setID] = useState("");
  const [password, setPassword] = useState("");
  
  const navigate = useNavigate();

  function Login_checker() {
    if (ID == "test" && password == "1234") {
      console.log("로그인 성공");
      navigate("/Home", { replace: true });
    } else {
      console.log("로그인 실패");
    }
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
          함께 읽어가는 우리만의 챌린지
        </p>

        <Card className="w-full bg-transparent border-none shadow-none">
          <CardContent className="flex flex-col gap-4 items-center">
            <Input
              className="w-[200px] h-10 bg-[#c6c6c6] rounded-[20px] text-xl text-center text-black"
              placeholder="ID"
              value={ID}
              onChange={(e) => setID(e.target.value)}
            />

            <Input
              type="password"
              className="w-[200px] h-10 bg-[#c6c6c6] rounded-[20px] text-xl text-center text-black"
              placeholder="PASSWORD"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button className="w-[200px] h-10 bg-[#c6c6c6] rounded-[20px] text-xl text-black hover:bg-[#b4b4b4]"
              onClick={Login_checker}
              >
              ENTER
            </Button>
          </CardContent>
        </Card>
      </div>
    </main>
  );
};
