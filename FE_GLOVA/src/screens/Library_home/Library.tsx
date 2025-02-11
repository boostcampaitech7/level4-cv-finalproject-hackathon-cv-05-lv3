import { useState, useEffect } from "react";
import { HelpCircle, Search } from "lucide-react";
import { Card, CardContent } from "../../components/ui/card";
import { useNavigate } from "react-router-dom";
import NaviBar from "../../components/ui/navigationbar";
import { GetRecommandBooks } from "../../api/api";
import { Nodata } from "../../dummy";

const pastelColors = [
  "bg-pink-200", "bg-blue-200", "bg-green-200",
  "bg-yellow-200", "bg-purple-200", "bg-red-200", "bg-indigo-200"
];

interface Book {
  bookTitle: string;
  bookImage: string;
  questionText: string;
}

export const Library_home = (): JSX.Element => {
  const navigate = useNavigate();
  const [books, setBooks] = useState(Nodata);
  const [flipped, setFlipped] = useState<{ [key: string]: boolean }>({});
  const [zoomed, setZoomed] = useState<{ [key: string]: boolean }>({});
  const [isInfoModalOpen, setIsInfoModalOpen] = useState(false);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await GetRecommandBooks();  // ✅ response는 이미 response_body 데이터만 반환

        console.log("📌 서버 응답:", response);

        if (response && Array.isArray(response)) {  // ✅ response가 배열인지 체크
          const transformedBooks = response.map((item: any) => ({
            date: item.date,
            time: item.time,
            bookTitle: item.book?.title || "책을 추천받아 보세요!",
            bookImage: item.book?.image || "../../image_data/Library_sample.png",
            questionText: item.question?.text || "추천 받은 책에 대한 후기를 다른 사람들과 공유할 수 있어요!",
          }));

          setBooks(transformedBooks);
        } else {
          console.warn("🚨 서버 응답이 예상한 배열 형식이 아닙니다.", response);
        }
      } catch (error) {
        console.error("❌ 서버 통신 실패:", error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div className="bg-gray-500 flex flex-row justify-center w-full min-h-screen overflow-y-auto relative">
      <div className="bg-white w-[393px] min-h-screen relative pb-16">
        {/* 상단 아이콘 */}
        <button
          className="absolute top-[20px] right-[20px] p-2 bg-gray-200 rounded-full hover:bg-gray-300"
          onClick={() => setIsInfoModalOpen(true)}
        >
          <HelpCircle size={24} />
        </button>

        {/* 타이틀 */}
        <div className="inline-flex items-center justify-center w-full mt-[70px]">
          <h1 className="text-[40px] font-SBAggroB text-black text-center">『 나만의 도서관 』</h1>
        </div>
        <hr className="border-t border-2 border-gray-300 mt-8 mx-4 mb-4" />

        {/* 도서 목록 */}
        <div className="grid grid-cols-3 gap-0 px-0 mt-0 w-full relative pb-[45px]">
          {books.map((book) => {
            const randomColor = pastelColors[Math.floor(Math.random() * pastelColors.length)];

            return (
              <Card key={book.bookTitle} className="border-none w-full">
                <CardContent className="p-0 flex flex-col items-center">
                  <div
                    className={`relative w-full aspect-[3/4] transform transition-all duration-300 ease-in-out 
                    ${flipped[book.bookTitle] ? "rotate-y-180" : ""} 
                    ${zoomed[book.bookTitle] ? "scale-150 z-50" : "z-10"}`}
                    onClick={() => setFlipped((prev) => ({ ...prev, [book.bookTitle]: !prev[book.bookTitle] }))}
                    onMouseDown={() => setZoomed((prev) => ({ ...prev, [book.bookTitle]: true }))}
                    onMouseUp={() => setZoomed((prev) => ({ ...prev, [book.bookTitle]: false }))}
                  >
                    {/* 앞면: 원래 책 이미지 */}
                    <img
                      className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 
                      ${flipped[book.bookTitle] ? "opacity-0" : "opacity-100"}`}
                      alt={book.bookTitle}
                      src={book.bookImage}
                    />

                    {/* 뒷면: 질문 카드 */}
                    <div
                      className={`absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center p-4 rounded-lg shadow-lg transition-opacity duration-500 
                      ${flipped[book.bookTitle] ? "opacity-100" : "opacity-0"} ${randomColor}`}
                    >
                      <div className="w-full h-5 bg-neutral-800 text-white flex items-center justify-center rounded-t-lg text-[7px]">
                        무엇이든 얘기해보세요!
                      </div>
                      <div className="w-full flex items-center justify-center bg-white text-black p-1 rounded-b-lg text-center text-[10px]">
                        {book.questionText}
                      </div>
                    </div>

                    {/* 상세 보기 버튼 */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("/Library_detail", { replace: true, state: book });
                      }}
                      className="absolute top-2 right-2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 z-50 pointer-events-auto"
                    >
                      <Search className="w-4 h-4 text-gray-600" />
                    </button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* ✅ 정보 모달 */}
        {isInfoModalOpen && (
          <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-5 rounded-lg w-[350px] shadow-lg text-center relative flex flex-col justify-center items-center">
              <img
                src="../../image_data/Guide/Library_home.png"
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

        {/* 하단 네비게이션 바 */}
        <div className="fixed bottom-0 left-0 w-full bg-white shadow-md z-50">
          <NaviBar activeLabel="Library" />
        </div>
      </div>
    </div>
  );
};
