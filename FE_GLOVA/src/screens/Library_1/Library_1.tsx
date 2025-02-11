import { useState } from "react";
import { ChevronLeft, HelpCircle } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { PostReadFinished, PostBadgeMaker } from "../../api/api";
import NaviBar from "../../components/ui/navigationbar";
import { Nodata } from "../../dummy";

export const Library_1 = (): JSX.Element => {
  const location = useLocation();
  const navigate = useNavigate();
  const [nowloading, setLoading] = useState(false);
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);
  const [isLoadingModalOpen, setIsLoadingModalOpen] = useState(false);

  const book = location.state || {};

  const MakeBadge = async (recommendationId: number, bookId: number) => {
    setLoading(true); // 로딩 시작
    setIsLoadingModalOpen(true); // 로딩 모달 표시
    try {
      const response = await PostBadgeMaker(bookId);
      if (response.status === 200) {
        navigate("/Challenge", { replace: true });
      }
    } catch (error) {
      console.error("Badge creation failed:", error);
    } finally {
      setLoading(false); // 로딩 종료
      setIsLoadingModalOpen(false); // 로딩 모달 닫기
    }
  };

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

        <div className="absolute top-[443px] left-3.5 font-Freesentation text-black text-[18px] text-center">
          {book.date}
        </div>

        <img
          className="absolute w-[230px] h-[308px] top-[122px] left-[82px] object-cover"
          alt="Rectangle"
          src={book.bookImage}
        />

        <div className="absolute top-20 left-3.5 font-Freesentation text-black text-[20px] text-center">
          {book.bookTitle}
        </div>

        <div className="w-[361px] h-[170px] p-2.5 top-[476px] left-3.5 flex absolute">
          <div className="relative text-black text-base">
            {book.questionText}
          </div>
        </div>

        <button
          className="w-[48px] h-[30px] bg-gray-300 flex items-center left-4 gap-2.5 p-2.5 rounded-[20px] absolute top-[20px] left text-black text-lg"
          onClick={() => navigate('/Library', { replace: true })}
        >
          <ChevronLeft size={48} />
        </button>

        {Nodata[0].bookTitle !== book.bookTitle ? (
          <button
            className={`w-[361px] flex items-center justify-center p-2.5 rounded-[20px] absolute top-[693px] left-3.5 text-black text-lg active:scale-95 transition-transform duration-150 ${nowloading ? "bg-gray-400 cursor-not-allowed" : "bg-[#d9d9d9] hover:bg-[#d1d1d1]"
              }`}
            onClick={() => MakeBadge(book.recommendationId, book.bookId)}
            disabled={nowloading}
          >
            {nowloading ? "로딩 중..." : "완독!!"}
          </button>
        ) : null}


        {/* ✅ 로딩 모달 */}
        {isLoadingModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-30 z-50">
            <div className="bg-white p-5 rounded-lg w-[250px] shadow-lg text-center relative">
              <p className="text-xl font-Freesentation font-semibold">배지를 생성 중입니다...</p>
              <div className="flex justify-center items-center mt-4">
                <svg
                  className="animate-spin h-8 w-8 text-gray-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8H4z"
                  ></path>
                </svg>
              </div>
            </div>
          </div>
        )}

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative">
              <img
                src="../../image_data/Guide/Library.png"
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

        <NaviBar activeLabel="Library" />
      </div>
    </div>
  );
};
