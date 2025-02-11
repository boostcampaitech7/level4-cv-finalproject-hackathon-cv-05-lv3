import { Button } from "../../components/ui/button";
import { useState } from "react";
import { HelpCircle } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { useNavigate, useLocation } from "react-router-dom";
import { SaveRecommand } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";

export const Home4 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // 서버에서 받은 데이터
  const response = location.state || {};
  const data = response.status === "success" ? response.data : null;

  const handleClick = () => {
    setIsLoading(true); // 버튼 비활성화

    SaveRecommand(data);

    setTimeout(() => {
      navigate("/Library", { replace: true });
      setIsLoading(false); // 1초 후 다시 활성화
    }, 1000);
  };

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full">
      <div className="bg-white w-[393px] min-h-screen relative flex flex-col">
        {/* 상단 도움말 아이콘 */}
        <button
          className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
          onClick={() => setIsInfoModalOpen(true)}
        >
          <HelpCircle size={24} />
        </button>

        {/* 추천 결과 */}
        <div className="flex flex-col items-center px-4">
          <h2 className="mt-[125px] text-lg font-bold text-center text-gray-800 font-Freesentation">
            이런 책은 어떠신가요?
          </h2>

          <Card className="mt-4 border-none">
            <CardContent className="flex flex-col items-center p-0">
              <img
                className="w-[137px] h-[183px] object-cover"
                alt="Book cover"
                src={data.book_info?.image || "../../image_data/default_book.png"} // 기본 이미지 설정
              />
            </CardContent>
          </Card>

          {/* 책 제목 */}
          <div className="w-[299px] mt-4">
            <h1 className="text-2xl font-Freesentation text-center">{data.book_info?.title || "제목 없음"}</h1>
          </div>

          {/* 추천 이유 */}
          <div className="w-[325px] mt-4 bg-[#e1e1e1] rounded-md p-4 text-base font-normal overflow-auto max-h-[200px]">
            <p>
              {data.answer_text?.text || "추천 이유가 없습니다."}
            </p>
          </div>

          {/* 버튼 영역 */}
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
              onClick={handleClick}
              disabled={isLoading} // 버튼 비활성화
            >
              {isLoading ? "저장 중..." : "추천도서 저장하기"}
            </Button>
          </div>
        </div>

        {/* 도움말 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img src="../../image_data/Guide/Home4.png" alt="도움말 이미지" className="w-full h-auto rounded-md" />
              <button className="mt-4 px-4 py-2 bg-gray-500 text-white rounded-lg" onClick={() => setIsInfoModalOpen(false)}>
                닫기
              </button>
            </div>
          </div>
        )}

        <NaviBar activeLabel="Home" />
      </div>
    </div>
  );
};
