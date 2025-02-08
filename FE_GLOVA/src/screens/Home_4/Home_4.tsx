
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from "react-router-dom";
import { SaveRecommand } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";

import { dummy_single } from "../../dummy";

export const Home4 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  
  {/*서버 통신 데이터*/}
  const data = location.state || {};

  {/*더미 데이터*/}
  // const data = dummy_single;

  return (
    <div className="flex justify-center w-full bg-white">
      <div className="relative w-[393px] h-[852px] bg-white">
        {/* Main Content */}
        <div className="flex flex-col items-center px-4">
          <h2 className="mt-[147px] text-lg font-bold text-center font-inter">
            이런 책은 어떠신가요?
          </h2>

          <Card className="mt-12 border-none">
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
            <h1 className="text-3xl font-bold text-center">{data.bookTitle}</h1>
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
              도서관에 저장하기
            </Button>
          </div>
        </div>

        <NaviBar activeLabel="Home"/>
      </div>
    </div>
  );
};
