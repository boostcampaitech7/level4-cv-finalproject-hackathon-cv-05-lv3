import { useEffect, useState } from "react";
import { ChevronLeft } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { useNavigate, useLocation } from "react-router-dom";
import { Book, PostBadgeMaker } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";


export const Library_1 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const book = location.state || {};
  
  const [speak, setSpeak] = useState<string>("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const MakeBadge = async () => {
    console.log(speak);
    PostBadgeMaker(book.bookTitle, speak);
    navigate("/Challenge", { replace: true });
  };

  return (
    <div className="bg-white flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] h-[852px] relative">
        <img
          className="top-[110px] left-3.5 absolute w-[365px] h-px object-cover"
          alt="Line"
          src="../../image_data/line-4.svg"
        />

        <img
          className="top-[440px] left-2.5 absolute w-[365px] h-px object-cover"
          alt="Line"
          src="../../image_data/line-4.svg"
        />

        <div className="absolute top-[443px] left-3.5 [font-family:'Koulen',Helvetica] font-normal text-black text-xl text-center tracking-[0] leading-[normal]">
          {book.date}
        </div>

        <img
          className="absolute w-[230px] h-[308px] top-[122px] left-[82px] object-cover"
          alt="Rectangle"
          src = {book.bookimage}
        />

        <div className="absolute top-20 left-3.5 [font-family:'Koulen',Helvetica] font-normal text-black text-xl text-center tracking-[0] leading-[normal]">
          {book.bookTitle}
        </div>

        <div className="w-[361px] h-[170px] items-start gap-2.5 p-2.5 top-[476px] left-3.5 flex absolute">
          <div className="relative w-fit mt-[-1.00px] [font-family:'Koulen',Helvetica] font-normal text-black text-base text-left tracking-[0] leading-[normal]">
            {book.question}
          </div>
        </div>

        <button
          className="w-[48px] h-[30px] bg-gray-300 flex items-center justify-left gap-2.5 p-2.5 rounded-[20px] absolute top-[20px] left text-black text-lg font-normal [font-family:'Inter',Helvetica]"
          onClick={() => navigate('/Library', {replace:true})}
        >
          <ChevronLeft size={48}/>
        </button>

        <button
          className="w-[361px] flex items-center justify-center gap-2.5 p-2.5 bg-[#d9d9d9] rounded-[20px] absolute top-[693px] left-3.5 text-black text-lg font-normal [font-family:'Inter',Helvetica]"
          onClick={() => setIsModalOpen(true)}
        >
          완독 버튼
        </button>
        
        {/* ✅ Modal (이미지 클릭 시 표시) */}
        {isModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[300px] shadow-lg text-center relative">
              <h2 className="text-lg font-bold">인상 깊었던 내용을 적어주세요!</h2>
              {/* ✅ 텍스트 박스 */}
              <textarea
                className="w-full h-[177px] max-h-[177px] p-2 border border-gray-300 rounded-md focus:outline-none resize-none overflow-auto text-black text-[15px] font-bold"
                placeholder="TEXT INPUT"
                value={speak} // 입력값을 상태로 연결
                maxLength={50} // 50자 제한
                onChange={(e) => setSpeak(e.target.value)} // 상태 업데이트
              />
              
              {/* ✅ 제출 버튼 */}
              <button
                className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg"
                onClick={() => {
                  if (speak.trim() === "") {
                    setSpeak(book.bookTitle); // 비어있으면 기본 값 설정
                  }
                  MakeBadge(); // 비어있지 않으면 제출 함수 실행
                  }}
              >
                제출
              </button>
            </div>
          </div>
        )}


        <NaviBar activeLabel="Library"/>
      </div>
    </div>


  );
};
